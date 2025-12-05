
FROM python:3.11-slim AS builder


WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS runtime

ENV TZ=UTC

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . /app


RUN mkdir -p /data /cron && chmod 755 /data /cron


COPY cron/2fa-cron /etc/cron.d/2fa-cron


RUN chmod 0644 /etc/cron.d/2fa-cron \
    && crontab /etc/cron.d/2fa-cron


EXPOSE 8080


CMD ["sh", "-c", "cron && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
