import json
from sqlalchemy.orm import Session
from app.prediction.race_context import build_prediction_context
from app.prediction.llm_client import call_llm_with_context
from app.db.models import Prediction

SYSTEM_PROMPT = """
You are an expert Formula 1 race analyst. 
Given season-to-date data, predict the finishing order for the upcoming race.
Return ONLY valid JSON in this format:
{
  "predicted_order": [
    {"position": 1, "driver_id": "verstappen", "reasoning": "..."},
    ...
  ],
  "summary": "Brief overall reasoning"
}
"""

def predict_race(db: Session, season: int, round_number: int) -> dict:
    context = build_prediction_context(db, season, round_number)
    