
import os

from pydantic_settings import BaseSettings

ENV = os.getenv("ENV", "env")

class CommonSettings(BaseSettings):

    DATABASE_URL: str
    REDIS_URL: str

    class Config:
        env_prefix = "PROJECT_"

