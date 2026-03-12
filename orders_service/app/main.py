from fastapi import FastAPI
from .api.v1 import orders, health


def create_app():
    fastapi_app = FastAPI(
    title="Orders Service",
    description="Microservice 1",
    version="1.0.0",
    )
    @fastapi_app.get("/")
    async def root():
        return {"message": "Hello World"}

    fastapi_app.include_router(orders.router)
    fastapi_app.include_router(health.router)

    return fastapi_app

app = create_app()
