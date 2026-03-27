import httpx
from sqlalchemy.orm import Session
from app.db.models import Lap, Race, Driver, DriverNumberMap

BASE_URL = "https://api.openf1.org/v1"

def _get_race_session_key(db: Session, season: int, round_number: int) -> int | None:
    race = db.query(Race).filter_by(season=season, round_number=round_number).first()
    if not race or not race.race_date:
        return None

    from datetime import timedelta

    # OpenF1 sessions can be located reliably using date filtering.
    # We search for the "Race" session starting near the Ergast race date.
    start = race.race_date.date()
    end = (race.race_date + timedelta(days=3)).date()

    # OpenF1 uses a non-standard filter syntax where operators are embedded in the query string,
    # e.g. ...?date_start>=2024-03-01 (note: no '=' after the parameter name).
    url = (
        f"{BASE_URL}/sessions"
        f"?year={season}"
        f"&session_name=Race"
        f"&date_start%3E%3D{start.isoformat()}"
        f"&date_start%3C%3D{end.isoformat()}"
    )
    sessions = httpx.get(url, timeout=30).json()

    if not sessions or not isinstance(sessions, list):
        return None

    # If multiple sessions match, take the earliest.
    sessions_sorted = sorted(sessions, key=lambda s: s.get("date_start") or "")
    return sessions_sorted[0].get("session_key")


def _norm_name(s: str) -> str:
    import re
    import unicodedata

    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"[^a-z\s]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s


def sync_driver_map(db: Session, season: int, round_number: int) -> dict:
    """
    Build and persist a mapping from OpenF1 driver_number -> Ergast driver_id for this season.
    Prefers joining by acronym (OpenF1 name_acronym == Ergast Driver.code), with a name fallback.
    Also updates Driver.team where available.
    """
    session_key = _get_race_session_key(db, season, round_number)
    if session_key is None:
        return {"mapped": 0, "updated_drivers": 0, "skipped": 0, "reason": "no_session"}

    drivers_data = httpx.get(
        f"{BASE_URL}/drivers",
        params={"session_key": session_key},
        timeout=30,
    ).json()
    if not drivers_data or not isinstance(drivers_data, list):
        return {"mapped": 0, "updated_drivers": 0, "skipped": 0, "reason": "no_drivers"}

    ergast_by_code: dict[str, Driver] = {}
    ergast_by_name: dict[str, Driver] = {}
    for d in db.query(Driver).all():
        if d.code:
            ergast_by_code[d.code.upper()] = d
        ergast_by_name[_norm_name(d.name)] = d

    mapped = 0
    updated_drivers = 0
    skipped = 0

    for od in drivers_data:
        driver_number = od.get("driver_number")
        if driver_number is None:
            skipped += 1
            continue

        acronym = (od.get("name_acronym") or "").upper()
        full_name = od.get("full_name") or ""
        team_name = od.get("team_name") or ""

        match: Driver | None = None
        if acronym and acronym in ergast_by_code:
            match = ergast_by_code[acronym]
        else:
            match = ergast_by_name.get(_norm_name(full_name))

        if not match:
            skipped += 1
            continue

        existing = (
            db.query(DriverNumberMap)
            .filter_by(season=season, driver_number=int(driver_number))
            .first()
        )
        if existing:
            if existing.ergast_driver_id != match.id:
                existing.ergast_driver_id = match.id
            # still count as mapped
            mapped += 1
        else:
            db.add(
                DriverNumberMap(
                    season=season,
                    driver_number=int(driver_number),
                    ergast_driver_id=match.id,
                )
            )
            mapped += 1

        if team_name and (match.team or "") != team_name:
            match.team = team_name
            updated_drivers += 1

    db.commit()
    return {"mapped": mapped, "updated_drivers": updated_drivers, "skipped": skipped, "reason": "ok"}


def fetch_laps(db: Session, season: int, round_number: int):
    # Get the race from DB first
    race = db.query(Race).filter_by(season=season, round_number=round_number).first()
    if not race:
        print("Race not found in DB")
        return

    session_key = _get_race_session_key(db, season, round_number)
    if session_key is None:
        print("No session found")
        return

    # Keep ingestion idempotent for iterative development.
    db.query(Lap).filter_by(race_id=race.id).delete()
    db.commit()

    # Fetch all laps for this session
    laps_data = httpx.get(
        f"{BASE_URL}/laps",
        params={"session_key": session_key},
        timeout=60,
    ).json()
    if not laps_data or not isinstance(laps_data, list):
        # Occasionally the API returns a JSON object with a detail string (e.g., transient rate limiting).
        if isinstance(laps_data, dict) and laps_data.get("detail"):
            import time

            time.sleep(2)
            laps_data = httpx.get(
                f"{BASE_URL}/laps",
                params={"session_key": session_key},
                timeout=60,
            ).json()

        if not laps_data or not isinstance(laps_data, list):
            print(f"Unexpected laps payload for session_key={session_key}: {type(laps_data).__name__}")
            return

    num_map: dict[int, str] = {
        m.driver_number: m.ergast_driver_id
        for m in db.query(DriverNumberMap).filter_by(season=season).all()
    }

    for l in laps_data:
        driver_number = l.get("driver_number")
        if driver_number is None:
            continue
        ergast_driver_id = num_map.get(int(driver_number))
        if not ergast_driver_id:
            # Skip laps we can't attribute to a known Ergast driver
            continue

        lap = Lap(
            race_id=race.id,
            driver_id=ergast_driver_id,
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