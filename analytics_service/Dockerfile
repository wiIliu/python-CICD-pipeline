FROM python:3.11-slim AS base

WORKDIR /app/analytics_service

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY app ./app

COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

ENV PYTHONPATH=/app

ENTRYPOINT ["./docker-entrypoint.sh"]

FROM base AS dev

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

ENV ENV=DEV

# TEST
FROM dev AS test

# COPY pytest.ini .
COPY tests ./tests/

RUN pip install --no-cache-dir pytest-cov
ENV ENV=TEST

# ---------- production ----------
FROM base AS prod

ENV ENV=PROD
