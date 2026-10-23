# Multi-stage or slim Python 3.13 production image
FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATCHRIGHT_BROWSERS_PATH=/ms-playwright \
    PORT=8000

WORKDIR /app

# Install system dependencies needed for PostgreSQL client, curl healthchecks, and browser dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy dependency specifications first to leverage Docker layer caching
COPY pyproject.toml poetry.lock /app/

# Install Python dependencies
RUN poetry install --no-root --no-interaction

# Install Patchright stealth Chromium browser and system dependencies
RUN python -m patchright install --with-deps chromium

# Copy application source code and pre-seeded SQLite database
COPY . /app

# Ensure non-root permissions for browser and app execution
RUN mkdir -p /app/scraper/data/outputs && \
    chmod -R 777 /app/scraper/data

# Expose default API port
EXPOSE 8000

# Container health probe (supports Render dynamic PORT or fallback to 8000)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Default entrypoint runs the FastAPI REST API binding dynamically to Render's injected $PORT
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
