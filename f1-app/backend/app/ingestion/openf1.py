import httpx
from sqlalchemy.orm import Session
from app.db.models import Lap, Race

BASE_URL = "https://api.openf1.org/v1"

def fetch_laps(db: Session, season: int, round_number: int):
    # Get the race from DB first
    race = db.query(Race).filter_by(season=season, round_number=round_number).first()
    if not race:
        print("Race not found in DB")
        return

    # OpenF1 uses session_key — fetch it first
    sessions = httpx.get(
        f"{BASE_URL}/sessions",
        params={"year": season, "round_number": round_number, "session_type": "Race"}
    ).json()

    if not sessions:
        print("No session found")
        return

    session_key = sessions[0]["session_key"]

    # Fetch all laps for this session
    laps_data = httpx.get(
        f"{BASE_URL}/laps",
        params={"session_key": session_key}
    ).json()

    for l in laps_data:
        lap = Lap(
            race_id=race.id,
            driver_id=str(l.get("driver_number", "")),
            lap_number=l.get("lap_number", 0),
            lap_time_ms=int((l.get("lap_duration") or 0) * 1000),
            position=l.get("position", 0),
            tyre_compound="unknown",
            tyre_age=0,
            is_pit_lap=False,
            gap_ahead_ms=int((l.get("gap_to_leader") or 0) * 1000)
        )
        db.add(lap)

    db.commit()
    print(f"Laps synced: {len(laps_data)}")