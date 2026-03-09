import random
from uuid import uuid4
import factory
from orders_service.app.models import order

class OrderFactory(factory.alchemy.SQLAlchemyModelFactory): 
    class Meta:
        model = order.Order
        sqlalchemy_session_persistence = "flush"

    # id = factory.LazyFunction(uuid4)
    name = factory.Faker("name")
    product = factory.Sequence(lambda n: 'item %d' % n)
    count = factory.Faker("random_int", min=1, max=100)
    price = factory.Faker("pyfloat", left_digits=3, right_digits=2, positive=True)
    