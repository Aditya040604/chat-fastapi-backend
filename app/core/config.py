from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded form environment variables.
    """

    # Database Configuration
    database_url: str
    database_sync_url: str

    # JWT Authentication
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 20

    # Application Settings
    project_name: str = "Chat Backend API"
    version: str = "1.0.0"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    environment: str = "development"

    # CORS Settings
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    allowed_hosts: str = "localhost,127.0.0.1"

    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    redis_password: str = ""

    # File Upload Settings
    max_upload_size: int = 10485760
    upload_dir: str = "./uploads"
    allowed_image_extensions: str = "jpg,jpeg,jpg,png,gif,webp"
    allowed_file_extensions: str = "pdf,doc,docx,txt,zip"

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    @property
    def cors_origin(self) -> List[str]:
        """Parse allowed_origins into a list"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    @property
    def allowed_hosts_list(self) -> List[str]:
        """Parse allowed_hosts into a list"""
        return [host.strip() for host in self.allowed_hosts.split(",")]

    @property
    def image_extensions_list(self) -> List[str]:
        """Parse allowed_image_extensions into a list"""
        return [ext.strip() for ext in self.allowed_image_extensions.split(",")]

    @property
    def file_extensions_list(self) -> List[str]:
        """Parse allowed_file_extensions_list into a list"""
        return [ext.strip() for ext in self.allowed_file_extensions.split(",")]


# Create a single instance to be imported throughout the app
settings = Settings()
