from sqlalchemy.engine import URL

url = URL.create( #postgresql:///localhost/CICD_db
    drivername="postgresql+psycopg",
    username="postgres",
    password='postgres',
    host="localhost",
    port=5432,
    database="CICD-db"
)
