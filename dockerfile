FROM python:3.8-slim-bullseye

RUN apt-get update && apt-get install -y cron && \
    pip install --no-cache-dir requests python-dotenv && \
    mkdir -p /var/log/weather

WORKDIR /app
COPY main.py .
COPY crontab.txt .
CMD ["sh", "-c", "crontab /app/crontab.txt && cron -f"]