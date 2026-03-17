from fastapi import FastAPI
from .api.v1 import health, stats


def create_app():
    fastapi_app = FastAPI(
    title="Analytics Service",
    description="Microservice 2",
    version="1.0.0",
    )
    @fastapi_app.get("/")
    async def root():
        return {"message": "analytics_service"}

    fastapi_app.include_router(stats.router)
    fastapi_app.include_router(health.router)

    return fastapi_app

app = create_app()
