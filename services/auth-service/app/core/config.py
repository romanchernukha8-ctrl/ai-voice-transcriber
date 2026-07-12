from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "AI Voice Transcriber Auth Service"
    version: str = "0.1.0"

    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str

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