import random
from uuid import uuid4
import factory
from orders_service.app.models import order

class OrderFactory(factory.alchemy.SQLAlchemyModelFactory): 
    class Meta:
        model = order.Order
        sqlalchemy_session_persistence = "flush"

    id = uuid4
    name = factory.Faker("name")
    product = "item"
    count = random.randint(1, 100)
    price = print(round(random.uniform(1.00, 1000.0), 2))
    