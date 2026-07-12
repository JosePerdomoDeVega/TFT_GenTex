import asyncio
from domain.interfaces import PharmacyRepository, TextGenerationAgent
from domain.models import ConclusionRequest, ConclusionResponse, Indicator, IndicatorReport, ValidationRequest
from domain.prompts.manager_1.prompt_manager import PromptManager1


class ConclusionService:

    def __init__(self, repository: PharmacyRepository, agent: TextGenerationAgent, prompt_manager: PromptManager1 | None = None):
        self._repository = repository
        self._agent = agent
        self._prompts = prompt_manager or PromptManager1()


    async def _report_for(self, ax_id: str, indicator: Indicator, period) -> IndicatorReport:
        data = self._repository.get_indicator_data(ax_id, indicator, period)
        text = await self._agent.write_report(prompt=self._prompts.get_prompt(indicator=indicator.value), data=data.data)

        return IndicatorReport(indicator=indicator, text=text)


    async def generate(self, request: ConclusionRequest) -> ConclusionResponse:
        period = self._repository.get_analysis_period(request.ax_id)

        reports = await asyncio.gather(*(self._report_for(request.ax_id, ind, period) for ind in request.indicators))

        indicators_text = "\n".join(report.text for report in reports)

        conclusion = await self._agent.write_report(self._prompts.get_prompt("conclusion"), indicators_text)

        return ConclusionResponse(ax_id=request.ax_id, reports=list(reports), conclusion=conclusion)


    def validate(self, request: ValidationRequest) -> None:
        for report in request.reports:
            self._repository.save_text(request.ax_id, report.indicator.value, report.text)

        self._repository.save_text(request.ax_id, "usuarios_estadisticas", request.conclusion, ambito="CONCLUSIONES")
