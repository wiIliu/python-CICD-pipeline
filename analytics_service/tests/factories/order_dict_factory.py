from faker import Faker

fake = Faker()

def make_order(**overrides) -> dict:
    count = overrides.pop("count", fake.random_int(min=1, max=10))
    price = overrides.pop("price", round(fake.pyfloat(min_value=1, max_value=200, right_digits=2), 2))
    total = overrides.pop("total", round(count * price, 2))
    return {
        "id": overrides.pop("id", fake.random_int(min=1, max=9999)),
        "name": overrides.pop("name", fake.name()),
        "product": overrides.pop("product", fake.word()),
        "count": count,
        "price": price,
        "total": total,
        "created_at": overrides.pop("created_at", fake.date_time_this_year().isoformat()),
        **overrides,
    }

def make_orders(n: int = 3, **overrides) -> dict:
    items = [make_order(**overrides) for _ in range(n)]
    return {"items": items, "total": len(items)}
