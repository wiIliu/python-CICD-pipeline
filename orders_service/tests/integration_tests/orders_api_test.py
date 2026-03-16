from fastapi import status
from orders_service.tests.factories.order_factory import OrderFactory

# def test_isolation(client): ?


def test_post_order_success(client):
    response = client.post("/orders", json={
        "name": "test user",
        "product": "test product",
        "count": 2,
        "price": 10.0
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "test user"
    assert response.json()["total"] == 20.0

def test_post_order_invalid_payload(client):
    response = client.post("/orders", json={
        "name": "test"
    })

    assert response.status_code == 422



def test_get_all(client):
    OrderFactory.create_batch(2)

    response = client.get("/orders")
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) == 2

def test_get_all_empty(client):
    response = client.get("/orders")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["items"] == []

def test_get_by_name(client):
    OrderFactory()
    OrderFactory.create_batch(3, name="user")

    response = client.get("/orders/?name=user")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data["items"], list)
    assert len(data["items"]) == 3
    assert all(order["name"] == "user" for order in data["items"])


def test_get_by_product(client):
    OrderFactory()
    OrderFactory.create_batch(2, product="product")

    response = client.get("/orders?product=product")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data["items"], list)
    assert len(data["items"]) == 2
    assert all(order["product"] == "product" for order in data["items"])

def test_get_by_all_filters(client):
    target_name="target_customer"
    target_product="target_product"
    OrderFactory.create_batch(5, name="temp customer", product="temp product")
    OrderFactory.create_batch(10, name=target_name, product="temp product 2")
    OrderFactory.create_batch(12, name="temp customer 2", product=target_product)
    OrderFactory.create_batch(6, name=target_name, product=target_product)

    response = client.get(f"/orders?name={target_name}&product={target_product}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data["items"], list)
    assert len(data["items"]) == 6
    assert all(order["name"] == target_name for order in data["items"])
    assert all(order["product"] == target_product for order in data["items"])

def test_get_by_filters_no_match(client):
    target_name = "target_customer"
    target_product = "target_product"

    OrderFactory.create_batch(5, name="temp customer", product="temp product")
    OrderFactory.create_batch(10, name=target_name, product="temp product 2")
    OrderFactory.create_batch(12, name="temp customer 2", product=target_product)

    response = client.get(f"/orders?name={target_name}&product={target_product}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data["items"], list)
    assert len(data["items"]) == 0

def test_get_by_id(client, fixture_order):
    response = client.get(f"/orders/{fixture_order.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['id'] == fixture_order.id

def test_get_by_id_invalid_id(client, fixture_order):
    response = client.get(f"/orders/{fixture_order.id + 1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND



def test_put_success(client, fixture_order):
    response = client.put(f"/orders/{fixture_order.id}", json={"name": "new name"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "new name"

def test_put_invalid_id(client, fixture_order):
    response = client.put(f"/orders/{fixture_order.id + 1}", json={"name": "new name"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_put_invalid_data(client, fixture_order):
    response = client.put(f"/orders/{fixture_order.id}", json={"name": "x"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT



def test_delete_success(client, fixture_order):
    response = client.delete(f"/orders/{fixture_order.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_persists(client, fixture_order):
    client.delete(f"/orders/{fixture_order.id}")

    response = client.get(f"/orders/{fixture_order.id}")
    assert response.status_code == 404

def test_delete_invalid(client, fixture_order):
    response = client.delete(f"/orders/{fixture_order.id+1}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
