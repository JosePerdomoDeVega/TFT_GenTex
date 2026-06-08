from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    db_driver: str = Field(default="ODBC Driver 18 for SQL Server", alias="DB_DRIVER")
    db_server: str = Field(default="", alias="DB_SERVER")
    db_database: str = Field(default="", alias="DB_DATABASE")
    db_user: str = Field(default="", alias="DB_USER")
    db_password: str = Field(default="", alias="DB_PASSWORD")

    azure_openai_api_key: str = Field(default="", alias="AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: str = Field(default="", alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_deployment: str = Field(default="gpt-4-jlp", alias="AZURE_OPENAI_DEPLOYMENT")
    azure_openai_api_version: str = Field(default="2025-01-01-preview", alias="AZURE_OPENAI_API_VERSION")

    llm_temperature: float = Field(default=0.7, alias="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=4096, alias="LLM_MAX_TOKENS")
    llm_timeout: float = Field(default=60.0, alias="LLM_TIMEOUT")

    @property
    def connection_string(self) -> str:
        return f"DRIVER={{{self.db_driver}}};" f"SERVER={self.db_server};" \
               f"DATABASE={self.db_database};" f"UID={self.db_user};" f"PWD={self.db_password};"

    @property
    def chat_completions_url(self) -> str:
        base = self.azure_openai_endpoint.rstrip("/")
        return (
            f"{base}/openai/deployments/{self.azure_openai_deployment}"
            f"/chat/completions?api-version={self.azure_openai_api_version}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
