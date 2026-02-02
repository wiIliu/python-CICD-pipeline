from fastapi import FastAPI
from .api.v1 import orders, health

def create_app():
    app = FastAPI(
    title="Orders Service",
    description="Microservice 1",
    version="1.0.0",
    )
    @app.get("/")
    async def root():
        return {"message": "Hello World"} 

    app.include_router(orders.router)
    app.include_router(health.router)

    return app

app = create_app()
