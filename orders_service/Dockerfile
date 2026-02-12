FROM python:3.11-slim

WORKDIR /app/orders_service

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# COPY pytest.ini .
COPY app ./app
# COPY tests ./tests/
COPY alembic.ini .
COPY alembic ./alembic
COPY docker-entrypoint.sh .


RUN chmod +x docker-entrypoint.sh

ENV PYTHONPATH=/app

ENTRYPOINT ["./docker-entrypoint.sh"]
