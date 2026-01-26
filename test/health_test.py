from fastapi.testclient import TestClient
from orders_service.main import app


client = TestClient(app)


def test_placeholder():
    assert 1 == 1


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


