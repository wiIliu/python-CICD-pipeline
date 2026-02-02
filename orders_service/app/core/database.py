from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from .config import url

engine = create_engine(url, echo=True, pool_pre_ping=True)

Session = sessionmaker(
    bind=engine,
    autocommit=False, 
    autoflush=False,
    )

Base = declarative_base()
