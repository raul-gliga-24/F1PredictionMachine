import fastf1
import pandas as pd
from sqlalchemy.orm import Session
from app.db.models import Stint, Race

# Cache saves downloaded data locally so you don't re-download
fastf1.Cache.enable_cache("fastf1_cache")

def fetch_stints(db: Session, season: int, round_number: int):
    # Load the race session from FastF1
    session = fastf1.get_session(season, round_number, "R")
    session.load(laps=True, telemetry=False, weather=False)

    race = db.query(Race).filter_by(season=season, round_number=round_number).first()
    if not race:
        print("Race not found in DB")
        return

    laps = session.laps

    # Group by driver and stint number
    for driver_num in laps["DriverNumber"].unique():
        driver_laps = laps[laps["DriverNumber"] == driver_num]

        for stint_num in driver_laps["Stint"].unique():
            stint_laps = driver_laps[driver_laps["Stint"] == stint_num]

            if stint_laps.empty:
                continue

            compound = stint_laps["Compound"].iloc[0]
            start_lap = int(stint_laps["LapNumber"].min())
            end_lap = int(stint_laps["LapNumber"].max())

            # Calculate average degradation (lap time increase per lap)
            lap_times = stint_laps["LapTime"].dt.total_seconds() * 1000
            lap_times = lap_times.dropna()
            avg_deg = float(lap_times.diff().mean()) if len(lap_times) > 1 else 0.0

            stint = Stint(
                race_id=race.id,
                driver_id=str(driver_num),
                stint_number=int(stint_num),
                compound=compound,
                start_lap=start_lap,
                end_lap=end_lap,
                avg_deg_ms=avg_deg,
                optimal_window={"start": start_lap + 10, "end": start_lap + 18}
            )
            db.add(stint)

    db.commit()
    print(f"Stints synced for round {round_number}")