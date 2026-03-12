#!/bin/bash
set -e

echo "ENV = $ENV"

if [ "$ENV" = "DEV" ]; then
    echo "Running dev"
    exec uvicorn orders_service.app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload
elif [ "$ENV" = "TEST" ]; then
    echo "Running tests"
    exec pytest /app/orders_service/tests --rootdir=/app

    # exec pytest -v --cov=orders_service
elif [ "$ENV" = "PROD" ]; then
    echo "PROD ENVIRONMENT"
    exec uvicorn orders_service.app.main:app \
    --host 0.0.0.0 \
    --port 8000
else
    echo "No env provided - stopped"
    exit 1
fi