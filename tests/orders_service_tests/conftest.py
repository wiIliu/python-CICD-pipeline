import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://test1:test1@localhost:5432/orders_TEST"
)

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from orders_service.app.main import create_app
from ..factories.order_factory import OrderFactory
from orders_service.app.core.config import settings
from orders_service.app.dependencies.db import get_db


#TODO: path change - alembic.ini
@pytest.fixture(scope="session", autouse=True)
def migrate_db():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    yield

#TODO: put in function?
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
