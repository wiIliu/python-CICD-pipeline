from orders_service.app.core.database import Session

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
