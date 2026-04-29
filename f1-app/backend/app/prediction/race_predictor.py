import json
from sqlalchemy.orm import Session
from app.prediction.race_context import build_prediction_context
from app.prediction.llm_client import call_llm_with_context
from app.db.models import Prediction

SYSTEM_PROMPT = """
You are an expert Formula 1 race analyst. 
Given season-to-date data, predict the finishing order for ALL 22 drivers for the upcoming race.
You MUST provide a prediction for every single driver from position 1 to 22.
Return ONLY valid JSON in this format:
{
  "predicted_order": [
    {"position": 1, "driver_id": "verstappen", "reasoning": "..."},
    ... (continue for all 20 positions)
  ],
  "summary": "Brief overall reasoning"
}
"""

def predict_race(db: Session, season: int, round_number: int, early_season_threshold: int = 3) -> dict:
    context = build_prediction_context(db, season, round_number, early_season_threshold)
    if "Error" in context:
        return context

    try:
        response = call_llm_with_context(context, SYSTEM_PROMPT)
    except Exception as e:
        return {"Error": f"LLM API failed: {e}"}
    
    try:
        result = json.loads(response)
    except json.JSONDecodeError:
        import re
        match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL | re.IGNORECASE)
        if match:
            try:
                result = json.loads(match.group(1))
            except json.JSONDecodeError:
                return {"Error": "Invalid JSON from LLM", "raw_response": response}
        else:
            return {"Error": "Invalid JSON from LLM", "raw_response": response}

    if not isinstance(result, dict):
        return {"Error": "LLM returned a non-dictionary JSON object", "raw_response": response}

    prediction = Prediction(
        race_id = context["upcoming-race"]["race_id"],
        prediction_type = "pre-race",
        predicted_order = result.get("predicted_order",[]),
        reasoning_trace = result.get("summary", ""),
        model_used = "gemini-3-flash-preview",
        context_snapshot = context,
    )
    db.add(prediction)
    db.commit()
    return result
    