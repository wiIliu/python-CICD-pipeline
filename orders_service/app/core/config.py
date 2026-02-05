from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    class Config:
        env_file = ".env"


print(Settings().model_dump())
settings = Settings()

