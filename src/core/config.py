from logging import config as logging_config
from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

env_file = ".env"


class Postgres(BaseSettings):
    database: str = Field(default="test_database", env="POSTGRES_DB")
    user: str = Field(default="app", env="POSTGRES_USER")
    password: str = Field(default="123qwe", env="POSTGRES_PASSWORD")
    host: str = Field(default="127.0.0.1", env="POSTGRES_HOST")
    port: int = Field(default=5432, env="POSTGRES_PORT")
    echo: bool = Field(default=False, env="POSTGRES_ECHO")

    def dsn(self):
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    class Config:
        env_file = env_file


class Settings(BaseSettings):
    service_name: str = Field(default="service_factories", env="SERVICE_NAME")

    postgres: Postgres = Postgres()

    class Config:
        env_file = env_file


settings = Settings()
