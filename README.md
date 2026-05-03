# F1PredictionMachine

F1PredictionMachine is an AI-powered Formula 1 prediction web application. It combines live data ingestion from the Ergast API with the reasoning capabilities of Google Gemini to generate pre-race insights, full championship standings, and unique "Simulate to Win" scenario analyses. It features a polished, modern React dashboard with glassmorphism design, animated F1 speed lines, and a responsive layout.

## Features

- **Single Race Predictions**: Generates race outcome predictions based on grid positions, driver form, and circuit characteristics.
- **Championship Season Simulation**: Predicts full Driver and Constructor standings for an entire season.
  - **Simple Mode**: High-level summary + final standings.
  - **Detailed Mode**: Every race's top 5 finishers, fastest lap, and notable DNFs in an expandable accordion, alongside the final standings.
- **Simulate to Win**: Select any driver on the grid — the backend mathematically computes the required championship scenario (race-by-race results needed for that driver to clinch the title) and the LLM narrates it. Automatically flags when a championship is mathematically impossible.
- **Dynamic Scheduling**: Automatically fetches accurate race schedules and circuit names for any chosen season via the Ergast API.
- **Modern Dashboard**: Glassmorphism UI with team/driver color mappings, animated F1 speed lines, tech-grid background, and smooth transitions. Non-scrollable until predictions are loaded.
- **Data Ingestion Pipeline**: Synchronizes circuits, drivers, races, and qualifying data into a structured Postgres database via `httpx`.

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy, Uvicorn
- **Frontend**: React + Vite, Lucide-React icons, Vanilla CSS
- **Database**: Postgres (managed via Docker)
- **Cache**: Redis
- **Data Sources**: Ergast API (via jolpi.ca mirror)
- **LLM**: Google Gemini (via `google-genai` SDK, `gemini-3-flash-preview`)

## Repo Structure

```
f1-app/
  backend/          # FastAPI app (uvicorn main:app)
    app/
      api/          # Route handlers (races, predictions, championship)
      ingestion/    # Ergast data fetchers
      prediction/   # LLM clients, race predictor, championship_sim, scenario_sim
      db/           # SQLAlchemy models and session
  frontend/         # React + Vite app
  docker-compose.yml
```

## Prerequisites

- **Docker Desktop** (required for Postgres, Redis, and Backend)
- **Node.js** (required for the frontend)

## Quick Start (Docker Backend + Local Frontend)

1. **Start backend services:**
```bash
cd f1-app
docker compose up -d postgres redis backend
```

2. **Start frontend (separate terminal):**
```bash
cd f1-app/frontend
npm install
npm run dev
```

3. **Access the application:**
   - Frontend: `http://localhost:5173`
   - Backend API Docs: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

## Environment Variables

The backend requires a `.env` file at `f1-app/backend/.env`:

```env
DATABASE_URL=postgresql+psycopg2://f1user:f1pass@postgres:5432/f1db
REDIS_URL=redis://redis:6379/0
GEMINI_API_KEY=your_google_gemini_api_key_here
ENVIRONMENT=development
```
> `.env` is git-ignored. Never commit secrets.

## API Routes

| Router | Prefix | Description |
|---|---|---|
| Races | `/api/races` | Season schedule, data sync |
| Predictions | `/api/predictions` | Single race predictions |
| Championship | `/api/championship` | Season standings + Simulate to Win |

### Key Endpoints

- `POST /api/predictions/pre-race/{season}/{round}` — Single race prediction
- `POST /api/championship/championship/{season}?detailed=false` — Season prediction (set `detailed=true` for per-race breakdown)
- `POST /api/championship/scenario/{season}/{driver_id}` — Simulate what must happen for a driver to win the championship

## Recent Updates

- **Simulate to Win**: New mode that computes exactly what race results are needed for any driver to clinch the championship. Backend does all the math; LLM only narrates the outcome for maximum token efficiency.
- **Detailed Season Mode**: Detailed championship predictions now include a race-by-race accordion with top 5, fastest lap, and notable DNFs for every round.
- **UI Revamp**: Redesigned header with animated F1Predict brand logo, modern 3-mode selector (Race / Season / Simulate to Win), animated red speed lines in the background, and a faint tech-grid overlay.
- **Scroll Lock**: Page is non-scrollable until predictions are generated, keeping the UI clean and focused.
- **Project Cleanup**: Removed accidental root-level scaffolding and all unused boilerplate assets.

## Development Notes

- The backend runs with `--reload` in Docker Compose for fast dev iteration.
- CORS is configured to allow all origins from the Vite dev server.
- The `compact=True` flag on `build_championship_context()` trims previous standings and rule descriptions to save input tokens during scenario simulations.
