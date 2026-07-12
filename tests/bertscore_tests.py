import asyncio
import statistics
from bert_score import scorer
import warnings
from applications.conclusion import ConclusionService
from applications.dependencies import get_pharmacy_repository, get_text_agent
from domain.models import ConclusionRequest, ConclusionResponse, Indicator
from domain.prompts.manager_1.prompt_manager import PromptManager1
from domain.prompts.manager_2.prompt_manager import PromptManager2
from domain.prompts.manager_3.prompt_manager import PromptManager3

warnings.filterwarnings('ignore')


def get_paired_text(report: ConclusionResponse, indicator: Indicator, reference_texts: dict) -> tuple[str, str] | None:
    reference = reference_texts.get(indicator.value)
    if reference is None or not report.reports:
        return None
    return report.reports[0].text, reference


def bertscore_case(report: ConclusionResponse, indicator: Indicator, reference_texts: dict) -> tuple[float, float, float] | None:
    pair = get_paired_text(report, indicator, reference_texts)
    if pair is None:
        return None
    candidate, reference = pair

    P, R, F1 = scorer.BERTScorer(lang="es").score([candidate], [reference])
    p, r, f1 = P.item(), R.item(), F1.item()

    print(f"AX_ID: {report.ax_id}  INDICATOR: {indicator.value}")
    print(f"{indicator.value:20s} P={p:.4f}  R={r:.4f}  F1={f1:.4f}")
    print("-" * 60)

    return p, r, f1


def get_real_reports(ax_id, sql) -> dict:
    reports = sql.get_indicator_texts(ax_id)
    return reports


async def generate_report(ax_id, indicator, sql, prompt_manager) -> ConclusionResponse:
    service = ConclusionService(sql, get_text_agent(), prompt_manager)
    reports = await service.generate(ConclusionRequest(ax_id=ax_id, indicators=[indicator]))
    return reports


def summarize(cases: list[tuple[str, Indicator]], all_scores: list[tuple[float, float, float] | None]) -> None:
    total_samples = sum(1 for s in all_scores if s is not None)
    print("=" * 60)
    print(f"RESUMEN ({total_samples} casos)")
    print("=" * 60)

    global_p, global_r, global_f1 = [], [], []

    for i, ((ax_id, indicator), scores) in enumerate(zip(cases, all_scores)):
        if scores is None:
            print(f"Case {i} ({ax_id}, {indicator.value})  sin texto de referencia")
            continue

        p, r, f1 = scores
        global_p.append(p)
        global_r.append(r)
        global_f1.append(f1)

        print(
            f"Case {i} ({ax_id}, {indicator.value}) "
            f"P={p:.4f}  R={r:.4f}  F1={f1:.4f}"
        )

    print("-" * 60)
    global_p_std = statistics.stdev(global_p) if len(global_p) > 1 else 0.0
    global_r_std = statistics.stdev(global_r) if len(global_r) > 1 else 0.0
    global_f1_std = statistics.stdev(global_f1) if len(global_f1) > 1 else 0.0
    print(
        f"{'GLOBAL':20s} "
        f"P={statistics.mean(global_p):.4f}±{global_p_std:.4f}  "
        f"R={statistics.mean(global_r):.4f}±{global_r_std:.4f}  "
        f"F1={statistics.mean(global_f1):.4f}±{global_f1_std:.4f}  "
        f"(n={len(global_f1)})"
    )


cases: list[tuple[str, Indicator]] = [
    ('OF00022_1', Indicator.deuda),
    ('OF00022_2', Indicator.deuda),
    ('OF00022_3', Indicator.deuda),
    ('OF00022_4', Indicator.deuda),
    ('OF00053_1', Indicator.codigos_propios),
    ('OF00053_2', Indicator.deuda),
    ('OF00053_4', Indicator.deuda),
    ('OF00054_4', Indicator.deuda),
    ('OF00054_4', Indicator.codigos_propios),
    ('OF00054_5', Indicator.deuda),
    ('OF00054_5', Indicator.codigos_propios),
    ('OF00054_6', Indicator.deuda),
    ('OF00054_6', Indicator.codigos_propios),

]


async def run_bertscore_test(cases):
    sql = get_pharmacy_repository()

    for name, prompt_manager in [("Generic", PromptManager3()), ("Zero-Shots", PromptManager2()), ("Few-Shots", PromptManager1())]:
        print(f"PROMPT_MANAGER: {name}")

        all_scores: list[tuple[float, float, float] | None] = []
        for ax_id, indicator in cases:
            report = await generate_report(ax_id, indicator, sql, prompt_manager)
            real = get_real_reports(ax_id, sql)
            print(report)
            print("--------------------------------------------------")
            print(real)
            scores = bertscore_case(report, indicator, real)
            all_scores.append(scores)

        summarize(cases, all_scores)


if __name__ == "__main__":
    asyncio.run(run_bertscore_test(cases=cases))
