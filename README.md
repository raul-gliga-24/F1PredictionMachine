# F1PredictionMachine
F1 prediction web app with a FastAPI backend and a React (Vite) frontend.  
Backend exposes race, prediction, and championship endpoints and uses Postgres + Redis.
## Tech stack
- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: React + Vite
- **Database**: Postgres
- **Cache / broker**: Redis
- **Data**: FastF1 (and planned: Ergast/OpenF1)
- **LLM**: Gemini (via `GEMINI_API_KEY`)
## Repo structure
- `f1-app/backend/` — FastAPI app (`uvicorn main:app`)
- `f1-app/frontend/` — React Vite app
- `f1-app/docker-compose.yml` — Postgres, Redis, backend services
## Prerequisites
- **Docker Desktop** (recommended for Postgres/Redis/backend via Compose)
- **Node.js** (for the frontend)
- **Python 3.12** (optional if running backend outside Docker)
## Quick start (Docker backend + local frontend)
From the project root:
```bash
cd "f1-app"
docker compose up -d postgres redis backend
Frontend (separate terminal):

cd "f1-app/frontend"
npm install
npm run dev
Frontend: http://localhost:5173
Backend API: http://localhost:8000
Health check: http://localhost:8000/health
Environment variables
Backend reads .env from:

f1-app/backend/.env
Minimum required keys (based on backend/app/config.py):

DATABASE_URL (example: postgresql+psycopg2://f1user:f1pass@postgres:5432/f1db)
REDIS_URL (example: redis://redis:6379/0)
GEMINI_API_KEY (your key)
ENVIRONMENT (optional, default: development)
Important: .env is ignored by git (see .gitignore). Don’t commit secrets.

API routes
The backend mounts these routers:

/api/races
/api/predictions
/api/championship
Health:

GET /health → { "status": "ok" }
Development notes
Backend runs with --reload in Docker Compose for faster iteration.
CORS is configured to allow the Vite dev server at http://localhost:5173.
Roadmap
Ingestion from Ergast + OpenF1 and normalization into Postgres
Derived models (dirty air, tyre degradation)
Pre-race and live scenario prediction outputs
Championship Monte Carlo simulation + narrative layer
