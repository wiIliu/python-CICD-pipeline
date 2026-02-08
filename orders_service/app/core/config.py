import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    class Config:
        env_file = os.getenv("ENV_FILE", ".env")


settings = Settings()
