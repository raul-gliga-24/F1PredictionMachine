from sqlalchemy.orm import Session, func
from app.db.models import Race, Driver, DriverNumberMap, Lap


def build_prediction_context(db: Session, season: int, target_round: int) -> dict:
    """
    Build sesason-to-date context for a pre-race prediction.

    Returns a JSON dict with:
    - season , target_round
    - upcoming_race : basic info about the target race
    - drivers: driver season stats 
    - teams: team season stats
    - races-summary : quick overview of previous races

    """ 
    upcoming_race = (db.query(Race).filter(Race.season == season, Race.round_number == target_round).first())
    if not upcoming_race:
        return {"Error":"Race not found","season":season , "target_round":target_round}

    previous_races = (db.query(Race).filter(Race.season == season, Race.round_number < target_round).order_by(Race.round_number).all())

    # Build driver season stats from lap data
    driver_stats = []
    for r in previous_races:
        laps = db.query(Lap).filter(Lap.race_id == r.id).order_by(Lap.lap_number.desc()).all()
        seen = set()
        for lap in laps:
            if lap.driver_id not in seen:
                seen.add(lap.driver_id)
                driver_stats.append({
                    "driver_id": lap.driver_id,
                    "round": r.round_number,
                    "final_position": lap.position,
                })

    return {
        "season": season,
        "target-round": target_round,
        "upcoming-race": {
            "race_id": upcoming_race.id,
            "round_number": upcoming_race.round_number,
            "circuit_id": upcoming_race.circuit_id,
            "race_date": upcoming_race.race_date.isoformat() if upcoming_race.race_date else None,
        },
        "previous-races": [
            {
                "race_id": r.id,
                "round_number": r.round_number,
                "circuit_id": r.circuit_id,
            } for r in previous_races
        ],
        "drivers": driver_stats,
        "teams": [],
    }
