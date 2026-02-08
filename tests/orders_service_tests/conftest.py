import pytest
# from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from orders_service.app.main import create_app
from ..factories.order_factory import OrderFactory
from orders_service.app.core.config import settings
from orders_service.app.dependencies.db import get_db

# load_dotenv(".env.test",override=True)


engine = create_engine(settings.DATABASE_URL)
TestingSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@pytest.fixture
def client(db: Session):
    app = create_app()
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as tc:
        yield tc
    app.dependency_overrides.clear()

@pytest.fixture(scope="function", autouse=True)
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSession(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(autouse=True)
def set_session_for_factories(db: Session):
    OrderFactory._meta.sqlalchemy_session = db
