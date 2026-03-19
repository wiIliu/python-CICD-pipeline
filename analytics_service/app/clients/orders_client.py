from cachetools import TTLCache
import requests as r

cache = TTLCache(maxsize=1, ttl=60)

def get_orders():

    if "orders" in cache:
        return cache["orders"]

    print("Fetching orders from Orders Service...")
    response = r.get("http://orders_service/orders")
    response.raise_for_status()

    data = response.json()
    cache["orders"] = data

    return data
