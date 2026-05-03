# F1PredictionMachine

F1PredictionMachine is an AI-powered Formula 1 prediction web application. It combines data ingestion from Ergast and OpenF1 with the reasoning capabilities of Gemini to generate pre-race insights and full championship predictions. It features a modern, responsive React dashboard utilizing sleek glassmorphism design.

## Features
- **Single Race Predictions**: Generates race outcomes based on grid positions, driver form, and circuit data.
- **Championship Season Simulation**: Predicts full Driver and Constructor standings with detailed narratives. Features a "Hindsight/Cheat" mode that ingests real-time season results to ensure highly accurate projections.
- **Dynamic Scheduling**: Automatically fetches accurate race schedules and circuit names for any chosen season via the Ergast API.
- **Modern Dashboard**: A professional glassmorphism UI with curated driver/team color mappings and animated transitions.
- **Data Ingestion Pipeline**: Synchronizes circuits, drivers, races, qualifying results, and lap data into a structured Postgres database using `httpx`.

## Tech Stack
- **Backend**: Python 3.12, FastAPI, SQLAlchemy, Uvicorn
- **Frontend**: React + Vite, Lucide-React for icons, Vanilla CSS
- **Database**: Postgres (managed via Docker)
- **Cache**: Redis
- **Data Sources**: Ergast API, OpenF1, FastF1
- **LLM**: Google Gemini (via `google-genai` SDK using `gemini-3-flash`)

## Repo Structure
- `f1-app/backend/` — FastAPI application (`uvicorn main:app`)
- `f1-app/frontend/` — React Vite application
- `f1-app/docker-compose.yml` — Orchestrates Postgres, Redis, and Backend services

## Prerequisites
- **Docker Desktop** (Required for Postgres, Redis, and Backend execution)
- **Node.js** (Required for the frontend)

## Quick Start (Docker Backend + Local Frontend)

1. **Start the backend services:**
```bash
cd f1-app
docker compose up -d postgres redis backend
```

2. **Start the frontend (in a separate terminal):**
```bash
cd f1-app/frontend
npm install
npm run dev
```

3. **Access the application:**
- Frontend Dashboard: `http://localhost:5173`
- Backend API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## Environment Variables

The backend requires a `.env` file located at `f1-app/backend/.env`.

**Minimum required keys:**
```env
DATABASE_URL=postgresql+psycopg2://f1user:f1pass@postgres:5432/f1db
REDIS_URL=redis://redis:6379/0
GEMINI_API_KEY=your_google_gemini_api_key_here
ENVIRONMENT=development
```
*Note: `.env` is ignored by git. Never commit your secrets.*

## Recent Updates
- **Hindsight Predictions**: Added context-aware season predictions. The Ergast ingestor now pulls actual top-10 race results for a given season, injecting them into the Gemini prompt so the LLM can "cheat" and perfectly align its standings with real car performance.
- **Dynamic Race Selector**: The UI now pulls the exact number of rounds and their official circuit names directly from the Ergast API based on the selected season.
- **UI Overhaul**: Implemented a modern, responsive Glassmorphism design system across the application.
- **Robust LLM Parsing**: Built custom JSON parsing and fallback routines to handle complex, large-token Gemini outputs safely into SQLite/Postgres.

## Development Notes
- The backend runs with `--reload` in Docker Compose for fast iteration.
- CORS is natively configured to allow requests from the Vite dev server.

## API Routes
The backend mounts several modular routers:
- `/api/races` - Endpoints for syncing season data and fetching schedules.
- `/api/predictions` - Trigger and retrieve single race predictions.
- `/api/championship` - Trigger and retrieve full season championship standings.
