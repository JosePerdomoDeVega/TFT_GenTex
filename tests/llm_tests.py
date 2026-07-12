import asyncio
import json
import re
import statistics
import warnings
import httpx
from applications.conclusion import ConclusionService
from applications.dependencies import get_pharmacy_repository, get_text_agent
from domain.models import ConclusionRequest, ConclusionResponse, Indicator
from domain.prompts.manager_1.prompt_manager import PromptManager1
from domain.prompts.manager_2.prompt_manager import PromptManager2
from domain.prompts.manager_3.prompt_manager import PromptManager3

warnings.filterwarnings("ignore")

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
LM_STUDIO_MODEL = "openai/gpt-oss-20b"

CRITERIA = ("general", "datos", "estilo")

JUDGE_SYSTEM_PROMPT = """
Eres un evaluador de similitud de contenido entre dos textos en español.

NO evalúas cuál texto es mejor: solo evalúas si el TEXTO B (generado) reproduce fielmente el contenido del TEXTO A (real).

Debes asignar TRES puntuaciones independientes, de 1 a 10:

1. GENERAL
Evalúa si ambos textos transmiten la misma información global:
- mismos hechos
- mismas conclusiones
- mismos usuarios, productos o elementos relevantes
- misma interpretación de los datos

No penalices diferencias de orden, longitud o redacción.

2. DATOS
Evalúa únicamente la fidelidad de los datos numéricos:
- importes
- cantidades
- porcentajes
- fechas
- identificadores
- valores concretos

Si el texto B inventa, modifica, omite o contradice cifras relevantes del texto A, esta puntuación debe ser baja, aunque el resto del texto sea parecido.

3. ESTILO
Evalúa únicamente la similitud del estilo de redacción:
- tono
- estructura
- organización
- forma de presentar la información

Ignora el contenido para esta puntuación.

IMPORTANTE:
- Un texto puede estar redactado de forma distinta y seguir obteniendo una puntuación alta en GENERAL y DATOS.
- Penaliza especialmente cuando el texto B llega a conclusiones distintas a las del texto A, aunque utilice las mismas cifras.
- No evalúes cuál está mejor escrito; únicamente cuánto se parece B a A.

Responde EXCLUSIVAMENTE con este formato, sin explicaciones adicionales:

GENERAL: <n>
DATOS: <n>
ESTILO: <n>

donde <n> es un número entero entre 1 y 10.
"""

JUDGE_USER_TEMPLATE = """TEXTO A (real):
{text_a}

TEXTO B (generado):
{text_b}

Puntúa GENERAL, DATOS y ESTILO según las instrucciones."""

_CRITERIA_RE = {
    criterio: re.compile(rf"{criterio.upper()}\s*:\s*(10|[1-9])", re.IGNORECASE)
    for criterio in CRITERIA
}


async def judge_similarity(text_a: str, text_b: str, client: httpx.AsyncClient) -> dict[str, float]:
    payload = {
        "model": LM_STUDIO_MODEL,
        "messages": [
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": JUDGE_USER_TEMPLATE.format(text_a=text_a, text_b=text_b)},
        ],
        "temperature": 0,
        "max_tokens": -1,
        "stream": False,
    }
    response = await client.post(LM_STUDIO_URL, json=payload, timeout=120.0)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]

    scores = {}
    for criterio, pattern in _CRITERIA_RE.items():
        match = pattern.search(content)
        if not match:
            raise ValueError(f"No se pudo extraer la puntuación '{criterio}' de: {content!r}")
        scores[criterio] = float(match.group(1))
    return scores


def get_paired_text(report: ConclusionResponse, indicator: Indicator, reference_texts: dict) -> tuple[str, str] | None:
    reference = reference_texts.get(indicator.value)
    if reference is None or not report.reports:
        return None
    return report.reports[0].text, reference


async def llm_score_case(
    report: ConclusionResponse, indicator: Indicator, reference_texts: dict, client: httpx.AsyncClient
) -> dict[str, float] | None:
    pair = get_paired_text(report, indicator, reference_texts)
    if pair is None:
        return None
    candidate, reference = pair

    scores = await judge_similarity(reference, candidate, client)

    print(f"AX_ID: {report.ax_id}  INDICATOR: {indicator.value}")
    print(
        f"{indicator.value:20s} "
        f"General={scores['general']:.1f}  Datos={scores['datos']:.1f}  Estilo={scores['estilo']:.1f}"
    )
    print("-" * 60)

    return scores


def get_real_reports(ax_id, sql) -> dict:
    return sql.get_indicator_texts(ax_id)


async def generate_report(ax_id, indicator, sql, prompt_manager) -> ConclusionResponse:
    service = ConclusionService(sql, get_text_agent(), prompt_manager)
    return await service.generate(ConclusionRequest(ax_id=ax_id, indicators=[indicator]))


def summarize(cases: list[tuple[str, Indicator]], all_scores: list[dict[str, float] | None]) -> None:
    total_samples = sum(1 for s in all_scores if s is not None)
    print("=" * 60)
    print(f"RESUMEN ({total_samples} casos)")
    print("=" * 60)

    global_by_criterio: dict[str, list[float]] = {criterio: [] for criterio in CRITERIA}

    for i, ((ax_id, indicator), scores) in enumerate(zip(cases, all_scores)):
        if scores is None:
            print(f"Case {i} ({ax_id}, {indicator.value})  sin texto de referencia")
            continue

        for criterio in CRITERIA:
            global_by_criterio[criterio].append(scores[criterio])

        parts = [f"{criterio.capitalize()}={scores[criterio]:.1f}" for criterio in CRITERIA]
        print(f"Case {i} ({ax_id}, {indicator.value}) " + "  ".join(parts))

    print("-" * 60)
    parts = []
    for criterio in CRITERIA:
        values = global_by_criterio[criterio]
        std = statistics.stdev(values) if len(values) > 1 else 0.0
        parts.append(f"{criterio.capitalize()}={statistics.mean(values):.2f}±{std:.2f}")
    n_global = len(global_by_criterio[CRITERIA[0]])
    print(f"{'GLOBAL':20s} " + "  ".join(parts) + f"  (n={n_global})")


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


async def run_llm_test(cases):
    sql = get_pharmacy_repository()
    all_texts = {}

    async with httpx.AsyncClient() as client:
        for name, prompt_manager in [("Generic", PromptManager3()), ("Zero-Shots", PromptManager2()), ("Few-Shots", PromptManager1())]:
            print(f"PROMPT_MANAGER: {name}")

            all_scores: list[dict[str, float] | None] = []
            for ax_id, indicator in cases:
                report = await generate_report(ax_id, indicator, sql, prompt_manager)
                reference_texts = get_real_reports(ax_id, sql)
                all_texts[f"{name}-{ax_id}-{indicator.value}"] = {
                    ax_id: {"reports": report.reports, "texts": reference_texts}
                }
                scores = await llm_score_case(report, indicator, reference_texts, client)
                all_scores.append(scores)

            summarize(cases, all_scores)
    print(json.dumps(all_texts))


if __name__ == "__main__":
    asyncio.run(run_llm_test(cases=cases))
