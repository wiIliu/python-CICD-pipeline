from sqlalchemy.engine import URL
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    class Config:
        env_file = ".env"


print(Settings().model_dump())
settings = Settings()

# url = URL.create( #postgresql:///localhost/CICD_db
#     drivername="postgresql+psycopg",
#     username="postgres",
#     password='postgres',
#     host="localhost",
#     port=5432,
#     database="CICD-db"
# )
