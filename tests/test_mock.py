from fastapi.testclient import TestClient
from applications.dependencies import get_pharmacy_repository, get_text_agent
from domain.interfaces import PharmacyRepository, TextGenerationAgent
from domain.models import AnalysisPeriod, Indicator, IndicatorData
from main import app


class MockPharmacyRepository(PharmacyRepository):
    def get_analysis_period(self, ax_id: str) -> AnalysisPeriod:
        return AnalysisPeriod(start="2025-01-01", end="2025-01-31")

    def get_indicator_data(self, ax_id, indicator, period) -> IndicatorData:
        return IndicatorData(ax_id=ax_id, indicator=indicator, data={"ok": True})

    def save_text(self, ax_id, indicator, text, ambito="ANALISIS_IX") -> None:
        return None

    def get_indicator_texts(self, ax_id: str) -> str:
        return "texto de prueba"


class MockTextAgent(TextGenerationAgent):
    async def write_report(self, prompt: str, data: object) -> str:
        return "informe simulado"


def test_mock_always_true():
    repository = MockPharmacyRepository()
    agent = MockTextAgent()

    app.dependency_overrides[get_pharmacy_repository] = lambda: repository
    app.dependency_overrides[get_text_agent] = lambda: agent
    try:
        client = TestClient(app)
        response = client.post("/conclusions", json={"ax_id": "OF00000_1", "indicators": [Indicator.stock.value]},)
        assert response.status_code == 200
        body = response.json()
        assert body["conclusion"] == "informe simulado"
        assert (body is not None) is True
    finally:
        app.dependency_overrides.clear()
