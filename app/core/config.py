from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str
    version: str
    debug: bool
    api_v1_prefix: str
    database_url: str
    redis_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    # for loading environment variables
    class Config:
        env_file = Path(__file__).resolve().parents[2] / ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


settings = Settings()
# print(settings.database_url
