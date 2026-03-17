from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import races, predictions, championship

app = FastAPI(title="F1 Predictor API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(races.router, prefix="/api/races", tags=["races"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])
app.include_router(championship.router, prefix="/api/championship", tags=["championship"])

@app.get("/health")
def health():
    return {"status": "ok"}

from app.db.session import engine
from app.db import models

models.Base.metadata.create_all(bind=engine)