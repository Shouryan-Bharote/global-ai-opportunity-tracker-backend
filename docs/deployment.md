# Deployment Guide — TrackIT Backend

This guide details how to build, containerize, and deploy the **TrackIT** (Global AI Opportunity Tracker) backend in production.

---

## 1. Architecture Overview

The production deployment consists of three decoupled components:

```
                      ┌──────────────────────┐
                      │  Internet / Clients  │
                      │ (Flutter App / Web)  │
                      └──────────┬───────────┘
                                 │ HTTP (8000)
                                 ▼
                      ┌──────────────────────┐
                      │     trackit-api      │
                      │  (FastAPI + Uvicorn) │
                      └──────────┬───────────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           │                     │                     │
           ▼                     │                     ▼
┌──────────────────────┐         │          ┌──────────────────────┐
│  trackit-scheduler   │         │          │   trackit-postgres   │
│ (APScheduler Daemon) │─────────┴─────────▶│    (PostgreSQL 16)   │
└──────────────────────┘                    └──────────────────────┘
```

1. **`trackit-api`**: High-performance FastAPI REST API serving `/api/v1/opportunities`, `/api/v1/jobs`, and `/health`.
2. **`trackit-scheduler`**: Asynchronous background daemon running periodic scraping jobs (Devpost, Unstop) at configured cron intervals (default: nightly at 2:00 AM UTC).
3. **`trackit-postgres`**: Persistent relational database storing opportunities and job execution runs with UPSERT deduplication.

---

## 2. Quickstart: Local Docker Deployment

### Prerequisites
- Docker Engine 24+ & Docker Compose v2+

### Step 1: Prepare Environment File
Copy the provided `.env.docker` template or `.env.example`:

```bash
cp .env.docker .env
```

Open `.env` and configure your LLM API keys:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
GEMINI_API_KEY=AIzaSy_your_gemini_key_here
POSTGRES_PASSWORD=your_secure_db_password
```

### Step 2: Build and Start Containers

```bash
docker compose up -d --build
```

### Step 3: Verify Deployment

1. **Check container status**:
   ```bash
   docker compose ps
   ```
2. **Verify API health probe**:
   ```bash
   curl -s http://localhost:8000/health
   ```
   Expected response:
   ```json
   {"status":"ok","app_name":"TrackIT Backend","environment":"production","database_connected":true}
   ```
3. **Access Interactive API Docs**:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Step 4: Monitor Logs

```bash
# View API server logs
docker compose logs -f api

# View Scheduler logs
docker compose logs -f scheduler

# View Database logs
docker compose logs -f db
```

To stop all services:
```bash
docker compose down
```

---

## 3. Production Deployment Scenarios

### Option A: Virtual Private Server (VPS / AWS EC2 / DigitalOcean)

1. **Install Docker & Git on your server**:
   ```bash
   sudo apt-get update && sudo apt-get install -y docker.io docker-compose-plugin git
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/Shouryan-Bharote/global-ai-opportunity-tracker-backend.git
   cd global-ai-opportunity-tracker-backend
   ```

3. **Configure production environment**:
   ```bash
   cp .env.docker .env
   nano .env
   ```

4. **Launch with Docker Compose**:
   ```bash
   docker compose up -d
   ```

5. **Set up Reverse Proxy (Nginx + Let's Encrypt SSL)**:
   Add an Nginx server block to terminate SSL and proxy requests to `http://127.0.0.1:8000`:
   ```nginx
   server {
       server_name api.yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
   Issue SSL via Certbot:
   ```bash
   sudo certbot --nginx -d api.yourdomain.com
   ```

---

### Option B: Cloud PaaS (Render / Railway / Fly.io)

TrackIT supports PaaS environments that consume Dockerfiles or web containers:

1. **Database**:
   - Create a managed PostgreSQL instance in the dashboard.
   - Copy the provided connection string (e.g., `postgres://user:pass@host/db`).
   - The application automatically translates `postgres://` to `postgresql+psycopg2://`.

2. **Web Service (`api`)**:
   - Connect your GitHub repository.
   - Build Type: **Dockerfile**.
   - Set environment variables:
     - `DATABASE_URL` = `<Your managed database connection string>`
     - `ENVIRONMENT` = `production`
     - `GROQ_API_KEY` = `<your key>`
     - `GEMINI_API_KEY` = `<your key>`
     - `HEADLESS` = `true`
   - Set health check path to `/health`.

3. **Worker Service (`scheduler`)**:
   - Create a second service (Background Worker) from the same repository.
   - Command override: `python -m scraper.core.scheduler.job_scheduler --scheduler`
   - Supply the same `DATABASE_URL` and LLM credentials.

---

## 4. Database Management & Backups

### Automatic Schema Creation
Database tables (`OpportunityDB`, `JobRun`) are initialized automatically on startup via `init_db()` in [shared/database/session.py](file:///d:/My%20Projects/Major%20Project/backend/global-ai-opportunity-tracker-backend/shared/database/session.py). No manual SQL migrations are required for fresh setups.

### PostgreSQL Backups
To create an on-demand SQL dump from the container:
```bash
docker compose exec -t db pg_dump -U trackit -d trackit > trackit_backup_$(date +%F).sql
```

To restore from a backup:
```bash
docker compose exec -i db psql -U trackit -d trackit < trackit_backup_2026-10-18.sql
```

---

## 5. Security & Operational Checklist

- [x] **Container Security**: Non-root directory permissions for scrapers and stealth browser dependencies.
- [x] **CORS Enforcement**: Restrict `CORS_ORIGINS` in production `.env` to trusted client origins instead of `["*"]`.
- [x] **Secrets Management**: Never commit `.env` containing live API keys or database passwords.
- [x] **Health Probes**: Container monitors `/health` to restart degraded containers automatically.
- [x] **Concurrency & Retries**: Scraper orchestrator limits concurrency to 2 parallel tasks with retry backoffs.
