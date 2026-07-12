from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    project_name: str = "AI Voice Transcriber File Service"
    version: str = "0.1.0"

    database_host: str
    database_port: int
    database_name: str = Field(validation_alias="FILE_DATABASE_NAME")
    database_user: str
    database_password: str

    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str
    minio_secure: bool

    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_user: str
    rabbitmq_password: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/"
            f"{self.database_name}"
        )

    @property
    def alembic_database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/"
            f"{self.database_name}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()