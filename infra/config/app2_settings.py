# app2/settings.py
from pydantic_settings import BaseSettings

class App2Settings(BaseSettings):
    API_KEY: str
    TIMEOUT: int = 30

    class Config:
        env_prefix = "APP2_"
