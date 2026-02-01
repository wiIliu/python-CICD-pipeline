#!/bin/bash
set -e

if [ "$ENV" = "DEV" ]; then
    echo "Running dev"
    exec uvicorn orders_service.app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload
elif [ "$ENV" = "TEST" ]; then
    echo "Running tests"
    exec pytest -v --cov=orders_service
else
    echo "No env provided - stopped"
    exit 1
fi