import json
from sqlalchemy.orm import session
from app.db.models import Prediction
from app.prediction.llm_client import call_llm_with_context
from app.ingestion.ergast import fetch_drivers, fetch_standings, fetch_season_results


def build_championship_context(db, season: int, compact: bool = False):
    prev_season = season - 1
    prev_driver_standings = fetch_standings(prev_season, "drivers")
    prev_constructor_standings = fetch_standings(prev_season, "constructors")

    current_lineup = fetch_drivers(db, season)
    real_season_performance_data = fetch_season_results(season)

    if compact:
        # Trim context to save input tokens for scenario mode
        prev_driver_standings = prev_driver_standings[:5]
        prev_constructor_standings = prev_constructor_standings[:5]
        rule_changes = "2026: major regulation changes, Cadillac 11th team, Audi takes Sauber."
    else:
        rule_changes = "2026 introduces massive regulation changes: 50/50 ICE/Electrical power split, active aerodynamics, smaller and lighter cars, and the removal of MGU-H. Cadillac enters as the 11th team. Audi takes over Sauber."

    context = {
        "target_season": season,
        "previous_driver_standings": prev_driver_standings,
        "previous_constructor_standings": prev_constructor_standings,
        "current_lineup": current_lineup,
        "rule_changes": rule_changes,
        "real_season_performance_data": real_season_performance_data,
    }
    return context


SYSTEM_PROMPT_BASE = """
You are an expert Formula 1 analyst. Based on the provided context, predict the final Driver and Constructor standings for the target season.

CRITICAL INSTRUCTION: You have been provided with 'real_season_performance_data' which contains the actual top 10 race results for the season so far. You MUST use this data to accurately judge true car pace and driver form. Ensure your final standings predictions closely align with the competitive order shown in these actual race results.

You MUST return a valid JSON object with the following structure:
{
  "summary": "A high-level overview of the season narrative, explaining how the cars actually performed.",
  "driver_standings": [
    {"driver_id": "string", "position": int, "points": int, "reasoning": "string"}
  ],
  "constructor_standings": [
    {"team_id": "string", "position": int, "points": int, "reasoning": "string"}
  ]
}
Do not use markdown formatting outside the JSON block.
"""

DETAILED_SCHEMA_ADDITION = """
Additionally, you MUST include a "race_results" key in your JSON response:
"race_results": [
  {
    "round": int,
    "race_name": "string",
    "top_5": ["driver_id_1", "driver_id_2", "driver_id_3", "driver_id_4", "driver_id_5"],
    "fastest_lap": "driver_id",
    "notable_dnfs": ["driver_id"]
  }
]
Use actual results from real_season_performance_data for completed races. Predict the remaining races based on car performance.
"""


def predict_championship(db: session, season: int, detailed: bool = False):
    context = build_championship_context(db, season)
    system_prompt = SYSTEM_PROMPT_BASE + (DETAILED_SCHEMA_ADDITION if detailed else "")
    raw_response = call_llm_with_context(context, system_prompt)

    try:
        cleaned = raw_response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        response_data = json.loads(cleaned.strip())
    except json.JSONDecodeError:
        raise ValueError("LLM failed to return valid JSON")

    for driver_pred in response_data.get("driver_standings", []):
        new_pred = Prediction(
            prediction_type="championship_driver",
            season=season,
            race_id=None,
            driver_id=driver_pred["driver_id"],
            position=driver_pred["position"],
            points=driver_pred.get("points"),
            reasoning=driver_pred["reasoning"],
        )
        db.add(new_pred)

    db.commit()
    return response_data