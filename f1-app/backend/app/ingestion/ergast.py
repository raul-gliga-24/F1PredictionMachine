import httpx
from sqlalchemy.orm import Session
from app.db.models import Circuit, Driver, Race, GridPosition
from datetime import datetime

BASE_URL = "https://api.jolpi.ca/ergast/f1"

def fetch_circuits(db: Session):
    response = httpx.get(f"{BASE_URL}/circuits.json?limit=100")
    data = response.json()["MRData"]["CircuitTable"]["Circuits"]

    for c in data:
        existing = db.get(Circuit, c["circuitId"])
        if not existing:
            circuit = Circuit(
                id=c["circuitId"],
                name=c["circuitName"],
                country=c["Location"]["country"],
                circuit_class="unknown",
                overtake_index=0.5,
                drs_zones=2,
                lap_length_km=0.0
            )
            db.add(circuit)
    db.commit()
    print(f"Circuits synced: {len(data)}")


def fetch_drivers(db: Session, season: int = 2024):
    response = httpx.get(f"{BASE_URL}/{season}/drivers.json?limit=100")
    data = response.json()["MRData"]["DriverTable"]["Drivers"]

    for d in data:
        existing = db.get(Driver, d["driverId"])
        if not existing:
            driver = Driver(
                id=d["driverId"],
                name=f"{d['givenName']} {d['familyName']}",
                code=d.get("code", ""),
                team="",
                nationality=d.get("nationality", "")
            )
            db.add(driver)
    db.commit()
    print(f"Drivers synced: {len(data)}")


def fetch_races(db: Session, season: int = 2024):
    response = httpx.get(f"{BASE_URL}/{season}/races.json?limit=100")
    data = response.json()["MRData"]["RaceTable"]["Races"]

    for r in data:
        race = Race(
            season=season,
            round_number=int(r["round"]),
            circuit_id=r["Circuit"]["circuitId"],
            race_date=datetime.strptime(r["date"], "%Y-%m-%d"),
            is_completed=False
        )
        db.add(race)
    db.commit()
    print(f"Races synced: {len(data)}")


def fetch_qualifying(db: Session, season: int, round_number: int):
    response = httpx.get(f"{BASE_URL}/{season}/{round_number}/qualifying.json")
    data = response.json()["MRData"]["RaceTable"]["Races"]

    if not data:
        print(f"No qualifying data for {season} round {round_number}")
        return

    results = data[0]["QualifyingResults"]
    race = db.query(Race).filter_by(season=season, round_number=round_number).first()

    if not race:
        print("Race not found in DB")
        return

    for q in results:
        gp = GridPosition(
            race_id=race.id,
            driver_id=q["Driver"]["driverId"],
            position=int(q["position"]),
            q3_time_ms=0,
            tyre_compound="unknown",
            dirty_air_exposure=0.0,
            gap_ahead_ms=0
        )
        db.add(gp)
    db.commit()
    print(f"Qualifying synced: {len(results)} drivers")