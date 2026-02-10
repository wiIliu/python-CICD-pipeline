from fastapi import status



def test_root_endpoint(client):
    """Test the root endpoint returns the expected response."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # assert "app" in data
    assert "message" in data
    # assert data["app"] == "Databricks FastAPI Example"

def test_isolation(client):
    client.post("/order", json={
        "id": 1,
        "name": "A",
        "product": "B",
        "count": 1,
        "price": 10.0
    })

def test_no_leak(client):
    response = client.get("/order/1")
    assert response.status_code == 404
    