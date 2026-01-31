from pydantic_settings import BaseSettings

class App1Settings(BaseSettings):
    JWT_SECRET: str
    WORKER_COUNT: int = 4

    class Config:
        env_prefix = "APP1_"