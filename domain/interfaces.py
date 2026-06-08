from abc import ABC, abstractmethod
from domain.models import AnalysisPeriod, Indicator, IndicatorData


class PharmacyRepository(ABC):

    @abstractmethod
    def get_analysis_period(self, ax_id: str) -> AnalysisPeriod:
        pass

    @abstractmethod
    def get_indicator_data(self, ax_id: str, indicator: Indicator, period: AnalysisPeriod) -> IndicatorData:
        pass

    @abstractmethod
    def save_text(self, ax_id: str, indicator: str, text: str, ambito: str = "ANALISIS_IX") -> None:
        pass

    @abstractmethod
    def get_indicator_texts(self, ax_id: str) -> str:
        pass


class TextGenerationAgent(ABC):

    @abstractmethod
    async def write_report(self, prompt: str, data: object) -> str:
        pass
