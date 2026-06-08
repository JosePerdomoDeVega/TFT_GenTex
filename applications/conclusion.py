import asyncio
from domain.interfaces import PharmacyRepository, TextGenerationAgent
from domain.models import ConclusionRequest, ConclusionResponse, Indicator, IndicatorReport
from domain.prompts.prompt_manager import PromptManager


class ConclusionService:

    def __init__(self, repository: PharmacyRepository, agent: TextGenerationAgent, prompt_manager: PromptManager | None = None):
        self._repository = repository
        self._agent = agent
        self._prompts = prompt_manager or PromptManager()


    async def _report_for(self, ax_id: str, indicator: Indicator, period) -> IndicatorReport:
        data = self._repository.get_indicator_data(ax_id, indicator, period)
        text = await self._agent.write_report(self._prompts.get_prompt(indicator.value), data.data)

        self._repository.save_text(ax_id, indicator.value, text)

        return IndicatorReport(indicator=indicator, text=text)


    async def generate(self, request: ConclusionRequest) -> ConclusionResponse:
        period = self._repository.get_analysis_period(request.ax_id)

        reports = await asyncio.gather(*(self._report_for(request.ax_id, ind, period) for ind in request.indicators))

        indicators_text = "\n".join(report.text for report in reports)

        conclusion = await self._agent.write_report(self._prompts.get_prompt("conclusion"), indicators_text)
        self._repository.save_text(request.ax_id, "usuarios_estadisticas", conclusion, ambito="CONCLUSIONES")

        return ConclusionResponse(ax_id=request.ax_id, reports=list(reports), conclusion=conclusion)
