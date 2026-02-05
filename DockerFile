FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pytest.ini .
COPY orders_service ./orders_service
COPY tests ./tests/
COPY alembic.ini .
COPY alembic ./alembic
COPY docker-entrypoint.sh .


RUN chmod +x docker-entrypoint.sh

ENV PYTHONPATH=/app

ENTRYPOINT ["./docker-entrypoint.sh"]
