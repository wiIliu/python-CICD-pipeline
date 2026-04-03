from cachetools import TTLCache
from fastapi import HTTPException
import requests as r

cache = TTLCache(maxsize=1, ttl=300)

ORDERS_URL = "http://orders_service/orders"
PAGE_SIZE = 100

def get_orders() -> dict:
    if "orders" in cache:
        return cache["orders"]

    print("Fetching orders from Orders Service...")

    all_items = []
    offset = 0

    try:
        while True:
            response = r.get(ORDERS_URL, params={"limit": PAGE_SIZE, "offset": offset})
            response.raise_for_status()
            data = response.json()

            all_items.extend(data["items"])
            offset += len(data["items"])

            if offset >= data["total"] or not data["items"]:
                break
    except r.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Orders service unavailable")

    result = {"items": all_items, "total": len(all_items)}
    cache["orders"] = result
    return result
