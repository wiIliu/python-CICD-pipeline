FROM python:3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pytest.ini .
COPY orders_service ./orders_service
COPY tests ./tests/
COPY docker-entrypoint.sh .


RUN chmod +x docker-entrypoint.sh

ENV PYTHONPATH=/app

ENTRYPOINT ["./docker-entrypoint.sh"]

# CMD [ "docker-entrypoint.sh"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

