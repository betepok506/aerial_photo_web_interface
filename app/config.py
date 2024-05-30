from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """App settings."""

    API_V1_STR: str = "/api/v1"

    PROJECT_NAME: str = "aerial-photography-web"
    debug: bool = False
    # ENVIRONMENT: str = "local"

    SERVER_URI: str = os.getenv("SERVER_URI", 'http://localhost')
    SERVER_PORT: str = os.getenv("SERVER_PORT", '8001')
    SERVER_URL: str = f'{SERVER_URI}:{SERVER_PORT}'

    class ConfigDict:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
