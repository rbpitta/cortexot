from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "CortexOT — Industrial AI Advisor"
    service_name: str = "cortexot-backend"
    environment: str = "development"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    database_url: str = "postgresql://cortexot:cortexot@localhost:5432/cortexot"
    database_connect_timeout_seconds: int = 5

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"

    mcp_base_url: str = "http://localhost:8001"
    simulator_base_url: str = "http://localhost:8080"


@lru_cache
def get_settings() -> Settings:
    return Settings()
