import json
import httpx
from sqlalchemy.orm import Session
from app.prediction.llm_client import call_llm_with_context
from app.ingestion.ergast import fetch_standings, fetch_season_results
from app.prediction.championship_sim import build_championship_context

BASE_URL = "https://api.jolpi.ca/ergast/f1"

# Max points per race: 25 (win) 
MAX_PTS_PER_RACE = 25


def fetch_season_schedule(season: int) -> list:
    """Returns list of all rounds in the season with their names."""
    response = httpx.get(f"{BASE_URL}/{season}/races.json?limit=100", timeout=15.0)
    response.raise_for_status()
    races = response.json()["MRData"]["RaceTable"]["Races"]
    return [{"round": int(r["round"]), "race_name": r["raceName"]} for r in races]


def compute_scenario_outline(season: int, target_driver_id: str) -> dict:
    """
    Pure math — no LLM involved.
    Returns a compact outline: gaps, races remaining, max points available,
    and whether the championship is still mathematically possible.
    """
    current_standings = fetch_standings(season, "drivers")
    all_rounds = fetch_season_schedule(season)

    # Find completed rounds from season results
    season_results = fetch_season_results(season)
    completed_rounds = {r["round"] for r in season_results}
    remaining_rounds = [r for r in all_rounds if r["round"] not in completed_rounds]
    races_remaining = len(remaining_rounds)
    max_available = races_remaining * MAX_PTS_PER_RACE

    # Find the target driver
    target = next(
        (d for d in current_standings if d["Driver"]["driverId"] == target_driver_id),
        None
    )
    if not target:
        raise ValueError(f"Driver '{target_driver_id}' not found in {season} standings.")

    target_pts = int(target["points"])
    target_name = f"{target['Driver']['givenName']} {target['Driver']['familyName']}"

    # Get all rivals sorted by points desc
    rivals = [
        {
            "driver_id": d["Driver"]["driverId"],
            "name": f"{d['Driver']['givenName']} {d['Driver']['familyName']}",
            "current_pts": int(d["points"]),
            "gap_to_target": int(d["points"]) - target_pts,
        }
        for d in current_standings
        if d["Driver"]["driverId"] != target_driver_id
    ]
    rivals_sorted = sorted(rivals, key=lambda x: x["current_pts"], reverse=True)

    # Championship is possible if target + max available > leader's current points
    leader_pts = rivals_sorted[0]["current_pts"] if rivals_sorted else 0
    mathematically_possible = (target_pts + max_available) > leader_pts

    return {
        "target_driver_id": target_driver_id,
        "target_driver_name": target_name,
        "target_current_pts": target_pts,
        "races_remaining": races_remaining,
        "remaining_rounds": remaining_rounds,
        "max_available_pts": max_available,
        "mathematically_possible": mathematically_possible,
        "top_rivals": rivals_sorted[:4],  # Top 4 rivals only to save tokens
    }


SCENARIO_SYSTEM_PROMPT = """
You are an expert Formula 1 analyst and championship tactician.

You have been given:
1. A pre-computed scenario outline showing the current standings gap and remaining races.
2. Real season performance data for context on car/driver pace.

Your task: Generate the specific, realistic race-by-race scenario that MUST happen for the target driver to win the championship.

Be precise and realistic — use the actual car performance from the data to determine plausible results.

You MUST return ONLY a valid JSON object with this exact structure:
{
  "possible": true,
  "target_driver": "driver_id",
  "summary": "A single concise paragraph describing what needs to happen overall.",
  "key_requirements": [
    "Bullet-point style requirement string (e.g., 'Verstappen must win at least 8 of the remaining 12 races')"
  ],
  "required_scenario": [
    {
      "round": int,
      "race_name": "string",
      "target_result": "Win/P2/P3/etc.",
      "critical_rival_results": {"driver_id": "DNF/P5/etc."},
      "points_after_race": int
    }
  ],
  "championship_clinched_round": int,
  "final_projected_points": int
}

Only include remaining races in required_scenario. Do not use markdown outside the JSON block.
"""

IMPOSSIBLE_SCENARIO_PROMPT = """
You are an expert Formula 1 analyst.

The target driver CANNOT mathematically win the championship based on the pre-computed outline.

Return ONLY a valid JSON object:
{
  "possible": false,
  "target_driver": "driver_id",
  "summary": "A brief explanation of why the championship is no longer mathematically possible.",
  "points_deficit": int,
  "max_available": int
}
Do not use markdown outside the JSON block.
"""


def predict_scenario(db: Session, season: int, target_driver_id: str) -> dict:
    outline = compute_scenario_outline(season, target_driver_id)

    if not outline["mathematically_possible"]:
        # Fast path: LLM just narrates the impossible case — very cheap call
        context = {
            "scenario_outline": outline,
            "season": season,
        }
        raw = call_llm_with_context(context, IMPOSSIBLE_SCENARIO_PROMPT)
    else:
        # Build compact context (trims standings/rules to save tokens)
        champ_context = build_championship_context(db, season, compact=True)
        context = {
            **champ_context,
            "scenario_outline": outline,
        }
        raw = call_llm_with_context(context, SCENARIO_SYSTEM_PROMPT)

    try:
        print(f"RAW LLM OUTPUT:\n{raw}")
        cleaned = raw.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        return json.loads(cleaned.strip())
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        raise ValueError("LLM failed to return valid JSON for scenario simulation.")
