#!/bin/bash
set -e

echo "ENV = $ENV"

if [ "$ENV" = "DEV" ]; then
    echo "Running dev"
    exec uvicorn analytics_service.app.main:app \
    --host 0.0.0.0 \
    --port 8001 \
    --reload
elif [ "$ENV" = "TEST" ]; then
    echo "Running tests"
    exec pytest /app/analytics_service --rootdir=/app
    # exec pytest -v --cov=orders_service
elif [ "$ENV" = "PROD" ]; then
    echo "PROD ENVIRONMENT"
    exec uvicorn analytics_service.app.main:app \
      --host 0.0.0.0 \
      --port 8001
    exec uvicorn analytics_service.app.main:app \
    --host 0.0.0.0 \
    --port 8001
else
    echo "No env provided - stopped"
    exit 1
fi