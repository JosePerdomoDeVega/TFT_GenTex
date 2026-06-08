from functools import lru_cache
from domain.interfaces import PharmacyRepository, TextGenerationAgent
from domain.settings import Settings, get_settings
from services.azure_agent import AzureOpenAITextAgent
from services.sql_repository import SqlServerPharmacyRepository


def get_app_settings() -> Settings:
    return get_settings()


@lru_cache
def get_pharmacy_repository() -> PharmacyRepository:
    return SqlServerPharmacyRepository(get_settings())


@lru_cache
def get_text_agent() -> TextGenerationAgent:
    return AzureOpenAITextAgent(get_settings())
