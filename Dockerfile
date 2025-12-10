# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

# Set working directory inside the container
WORKDIR /app

# Install build tools (only in builder stage)
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt


# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim

# Timezone must be UTC
ENV TZ=UTC

# Working directory for runtime container
WORKDIR /app

# Install system dependencies: cron + tzdata
RUN apt-get update && apt-get install -y --no-install-recommends \
        cron \
        tzdata \
    && rm -rf /var/lib/apt/lists/*

# Configure timezone to UTC
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code and scripts into container
COPY app ./app
COPY scripts ./scripts
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Copy key files into container
COPY student_private.pem student_private.pem
COPY student_public.pem student_public.pem
COPY instructor_public.pem instructor_public.pem

# Set permissions on cron file and register it
RUN chmod 0644 /etc/cron.d/2fa-cron
RUN crontab /etc/cron.d/2fa-cron

# Create volume mount points for persistent data
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Declare volumes so Docker can mount them
VOLUME ["/data", "/cron"]

# Expose API port
EXPOSE 8080

# Start cron + FastAPI app when container launches
CMD ["sh", "-c", "cron && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
