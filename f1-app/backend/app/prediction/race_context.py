import httpx
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Race, Driver, Lap, GridPosition

EARLY_SEASON_THRESHOLD = 1
POINTS_SYSTEM = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

def build_prediction_context(db: Session, season: int, target_round: int, early_season_threshold: int = EARLY_SEASON_THRESHOLD) -> dict:
    upcoming_race = db.query(Race).filter(Race.season == season, Race.round_number == target_round).first()
    if not upcoming_race:
        return {"Error": "Race not found", "season": season, "target_round": target_round}

    driver_points = {}
    team_points = {}

    if target_round > 1:
        try:
            prev_round = target_round - 1
            driver_url = f"https://api.jolpi.ca/ergast/f1/{season}/{prev_round}/driverStandings.json"
            team_url = f"https://api.jolpi.ca/ergast/f1/{season}/{prev_round}/constructorStandings.json"
            
            d_res = httpx.get(driver_url, timeout=10).json()
            standings_list = d_res.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
            if standings_list:
                for driver in standings_list[0].get("DriverStandings", []):
                    d_id = driver.get("Driver", {}).get("driverId")
                    driver_points[d_id] = float(driver.get("points", 0))

            t_res = httpx.get(team_url, timeout=10).json()
            t_standings_list = t_res.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
            if t_standings_list:
                for team in t_standings_list[0].get("ConstructorStandings", []):
                    t_id = team.get("Constructor", {}).get("constructorId")
                    team_points[t_id] = float(team.get("points", 0))
        except Exception as e:
            print(f"Error fetching standings from Jolpi: {e}")

    previous_season_races = []
    if target_round <= early_season_threshold:
        previous_season_races_query = (
            db.query(Race)
            .filter(Race.season == season - 1)
            .order_by(Race.round_number.desc())
            .limit(5)
            .all()
        )
        previous_season_races = [{"race_id": r.id, "round_number": r.round_number} for r in previous_season_races_query]

    grid = (
        db.query(GridPosition)
        .filter(GridPosition.race_id == upcoming_race.id)
        .order_by(GridPosition.position)
        .all()
    )
    starting_grid = [{"position": g.position, "driver_id": g.driver_id} for g in grid]

    if not starting_grid:
        try:
            q_url = f"https://api.jolpi.ca/ergast/f1/{season}/{target_round}/qualifying.json"
            q_res = httpx.get(q_url, timeout=10).json()
            races_data = q_res.get("MRData", {}).get("RaceTable", {}).get("Races", [])
            if races_data:
                qual_results = races_data[0].get("QualifyingResults", [])
                starting_grid = [{"position": int(q.get("position", 0)), "driver_id": q.get("Driver", {}).get("driverId")} for q in qual_results]
        except Exception as e:
            print(f"Error fetching qualifying from Jolpi: {e}")

    return {
        "season": season,
        "target-round": target_round,
        "upcoming-race": {
            "race_id": upcoming_race.id,
            "round_number": upcoming_race.round_number,
            "circuit_id": upcoming_race.circuit_id,
            "race_date": upcoming_race.race_date.isoformat() if upcoming_race.race_date else None,
        },
        "starting_grid": starting_grid,
        "previous-season-form": previous_season_races,
        "driver_standings": driver_points,
        "constructor_standings": team_points
    }
