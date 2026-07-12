import asyncio
import csv
import json
import statistics
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
import httpx
from applications.dependencies import get_pharmacy_repository
from domain.models import Indicator
from domain.prompts.manager_1.prompt_manager import PromptManager1
from domain.settings import get_settings
import warnings

warnings.filterwarnings("ignore")

OUTPUT_CSV = Path(__file__).parent / "performance_results.csv"
OUTPUT_JSON = Path(__file__).parent / "performance_results.json"

REPEATS = 3


@dataclass
class PhaseTiming:
    phase: str
    seconds: float
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass
class RunResult:
    ax_id: str
    mode: str
    repeat: int
    total_seconds: float
    phases: list[PhaseTiming] = field(default_factory=list)

    @property
    def prompt_tokens(self) -> int:
        return sum(p.prompt_tokens for p in self.phases)

    @property
    def completion_tokens(self) -> int:
        return sum(p.completion_tokens for p in self.phases)

    @property
    def total_tokens(self) -> int:
        return sum(p.total_tokens for p in self.phases)


class Stopwatch:
    def __init__(self):
        self.seconds = 0.0

    @contextmanager
    def measure(self):
        start = time.perf_counter()
        try:
            yield
        finally:
            self.seconds = time.perf_counter() - start


@contextmanager
def timed_phase(collector: list[PhaseTiming], phase: str, usage: dict | None = None):
    watch = Stopwatch()
    with watch.measure():
        yield watch
    prompt_tokens = usage.get("prompt_tokens", 0) if usage else 0
    completion_tokens = usage.get("completion_tokens", 0) if usage else 0
    total_tokens = usage.get("total_tokens", 0) if usage else 0
    collector.append(
        PhaseTiming(phase, watch.seconds, prompt_tokens, completion_tokens, total_tokens)
    )


class InstrumentedTextAgent:
    def __init__(self, settings):
        self._url = settings.chat_completions_url
        self._api_key = settings.azure_openai_api_key
        self._temperature = settings.llm_temperature
        self._max_tokens = settings.llm_max_tokens
        self._timeout = settings.llm_timeout

    async def write_report_with_usage(self, prompt: str, data: object, client: httpx.AsyncClient) -> tuple[str, dict]:
        headers = {"Content-Type": "application/json", "api-key": self._api_key}
        payload = {
            "messages": [
                {"role": "system", "content": "Eres un experto en análisis farmacéutico."},
                {"role": "user", "content": f"{prompt}\n{data}"},
            ],
            "temperature": self._temperature,
            "max_tokens": self._max_tokens,
        }
        response = await client.post(self._url, headers=headers, json=payload, timeout=self._timeout)
        response.raise_for_status()
        body = response.json()
        return body["choices"][0]["message"]["content"], body.get("usage", {})


async def run_parallel(ax_id: str, sql, agent: InstrumentedTextAgent, prompt_manager, client: httpx.AsyncClient) -> RunResult:
    phases: list[PhaseTiming] = []
    overall = Stopwatch()

    with overall.measure():
        with timed_phase(phases, "get_analysis_period"):
            period = sql.get_analysis_period(ax_id)

        with timed_phase(phases, "get_indicator_data_all"):
            data_by_indicator = {
                indicator: sql.get_indicator_data(ax_id, indicator, period)
                for indicator in Indicator
            }

        async def report_for(indicator: Indicator) -> tuple[Indicator, str, dict]:
            prompt = prompt_manager.get_prompt(indicator.value)
            text, usage = await agent.write_report_with_usage(prompt, data_by_indicator[indicator].data, client)
            return indicator, text, usage

        watch = Stopwatch()
        with watch.measure():
            results = await asyncio.gather(*(report_for(indicator) for indicator in Indicator))
        for indicator, _, usage in results:
            phases.append(
                PhaseTiming(
                    f"write_report[{indicator.value}]",
                    watch.seconds / len(results),
                    usage.get("prompt_tokens", 0),
                    usage.get("completion_tokens", 0),
                    usage.get("total_tokens", 0),
                )
            )

        indicators_text = "\n".join(text for _, text, _ in results)

        with timed_phase(phases, "write_conclusion") as watch_conclusion:
            conclusion_text, conclusion_usage = await agent.write_report_with_usage(
                prompt_manager.get_prompt("conclusion"), indicators_text, client
            )
        phases[-1].prompt_tokens = conclusion_usage.get("prompt_tokens", 0)
        phases[-1].completion_tokens = conclusion_usage.get("completion_tokens", 0)
        phases[-1].total_tokens = conclusion_usage.get("total_tokens", 0)

    return RunResult(ax_id=ax_id, mode="parallel", repeat=0, total_seconds=overall.seconds, phases=phases)


async def run_sequential(ax_id: str, sql, agent: InstrumentedTextAgent, prompt_manager, client: httpx.AsyncClient) -> RunResult:
    phases: list[PhaseTiming] = []
    overall = Stopwatch()

    with overall.measure():
        with timed_phase(phases, "get_analysis_period"):
            period = sql.get_analysis_period(ax_id)

        texts: list[str] = []
        for indicator in Indicator:
            with timed_phase(phases, f"get_indicator_data[{indicator.value}]"):
                data = sql.get_indicator_data(ax_id, indicator, period)

            prompt = prompt_manager.get_prompt(indicator.value)
            with timed_phase(phases, f"write_report[{indicator.value}]") as watch:
                text, usage = await agent.write_report_with_usage(prompt, data.data, client)
            phases[-1].prompt_tokens = usage.get("prompt_tokens", 0)
            phases[-1].completion_tokens = usage.get("completion_tokens", 0)
            phases[-1].total_tokens = usage.get("total_tokens", 0)
            texts.append(text)

        indicators_text = "\n".join(texts)

        with timed_phase(phases, "write_conclusion") as watch_conclusion:
            conclusion_text, conclusion_usage = await agent.write_report_with_usage(
                prompt_manager.get_prompt("conclusion"), indicators_text, client
            )
        phases[-1].prompt_tokens = conclusion_usage.get("prompt_tokens", 0)
        phases[-1].completion_tokens = conclusion_usage.get("completion_tokens", 0)
        phases[-1].total_tokens = conclusion_usage.get("total_tokens", 0)

    return RunResult(ax_id=ax_id, mode="sequential", repeat=0, total_seconds=overall.seconds, phases=phases)


def summarize(results: list[RunResult]) -> None:
    by_key: dict[tuple[str, str], list[RunResult]] = {}
    for result in results:
        by_key.setdefault((result.ax_id, result.mode), []).append(result)

    print("=" * 70)
    print(f"RESUMEN ({len(results)} ejecuciones, {REPEATS} repeticiones por caso)")
    print("=" * 70)

    for (ax_id, mode), runs in by_key.items():
        totals = [r.total_seconds for r in runs]
        tokens = [r.total_tokens for r in runs]
        total_std = statistics.stdev(totals) if len(totals) > 1 else 0.0
        tokens_std = statistics.stdev(tokens) if len(tokens) > 1 else 0.0
        print(
            f"{ax_id:15s} {mode:10s} "
            f"tiempo={statistics.mean(totals):.3f}s±{total_std:.3f}s  "
            f"tokens={statistics.mean(tokens):.0f}±{tokens_std:.0f}  "
            f"(n={len(runs)})"
        )

    print("-" * 70)
    all_totals = [r.total_seconds for r in results]
    all_tokens = [r.total_tokens for r in results]
    print(
        f"{'GLOBAL':15s} {'':10s} "
        f"tiempo={statistics.mean(all_totals):.3f}s±{statistics.stdev(all_totals) if len(all_totals) > 1 else 0.0:.3f}s  "
        f"tokens={statistics.mean(all_tokens):.0f}±{statistics.stdev(all_tokens) if len(all_tokens) > 1 else 0.0:.0f}  "
        f"(n={len(results)})"
    )


def dump_csv(results: list[RunResult], path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ax_id", "mode", "repeat", "phase", "seconds",
            "prompt_tokens", "completion_tokens", "total_tokens",
        ])
        for result in results:
            for phase in result.phases:
                writer.writerow([
                    result.ax_id, result.mode, result.repeat, phase.phase,
                    f"{phase.seconds:.6f}", phase.prompt_tokens,
                    phase.completion_tokens, phase.total_tokens,
                ])
            writer.writerow([
                result.ax_id, result.mode, result.repeat, "TOTAL",
                f"{result.total_seconds:.6f}", result.prompt_tokens,
                result.completion_tokens, result.total_tokens,
            ])


def dump_json(results: list[RunResult], path: Path) -> None:
    payload = [
        {
            "ax_id": r.ax_id,
            "mode": r.mode,
            "repeat": r.repeat,
            "total_seconds": r.total_seconds,
            "prompt_tokens": r.prompt_tokens,
            "completion_tokens": r.completion_tokens,
            "total_tokens": r.total_tokens,
            "phases": [
                {
                    "phase": p.phase,
                    "seconds": p.seconds,
                    "prompt_tokens": p.prompt_tokens,
                    "completion_tokens": p.completion_tokens,
                    "total_tokens": p.total_tokens,
                }
                for p in r.phases
            ],
        }
        for r in results
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


axs = ["OF00002_14", "OF00002_13"]


async def run_performance_tests(axs: list[str]):
    sql = get_pharmacy_repository()
    settings = get_settings()
    agent = InstrumentedTextAgent(settings)
    prompt_manager = PromptManager1()

    results: list[RunResult] = []

    async with httpx.AsyncClient() as client:
        for ax_id in axs:
            for repeat in range(1, REPEATS + 1):
                result = await run_sequential(ax_id, sql, agent, prompt_manager, client)
                result.repeat = repeat
                results.append(result)
                print(f"[sequential] {ax_id} repeat={repeat} -> {result.total_seconds:.3f}s, {result.total_tokens} tokens")

            for repeat in range(1, REPEATS + 1):
                result = await run_parallel(ax_id, sql, agent, prompt_manager, client)
                result.repeat = repeat
                results.append(result)
                print(f"[parallel]   {ax_id} repeat={repeat} -> {result.total_seconds:.3f}s, {result.total_tokens} tokens")

    summarize(results)
    dump_csv(results, OUTPUT_CSV)
    dump_json(results, OUTPUT_JSON)
    print(f"CSV  -> {OUTPUT_CSV}")
    print(f"JSON -> {OUTPUT_JSON}")


if __name__ == "__main__":
    asyncio.run(run_performance_tests(axs=axs))
