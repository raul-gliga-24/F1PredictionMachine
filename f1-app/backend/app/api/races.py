from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.ingestion import ergast
from app.ingestion import openf1, fastf1_loader
import traceback

router = APIRouter()

@router.get("/")
def get_races(db: Session = Depends(get_db)):
    from app.db.models import Race
    races = db.query(Race).all()
    return {"count": len(races), "races": [{"id": r.id, "season": r.season, "round": r.round_number} for r in races]}

@router.post("/sync/{season}")
def sync_season(season: int = 2026, db: Session = Depends(get_db)):
    try:
        ergast.fetch_circuits(db)
        ergast.fetch_drivers(db, season)
        ergast.fetch_races(db, season)
        return {"status": "synced", "season": season}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}")


@router.post("/sync/{season}/{round_number}")
def sync_round(season: int, round_number: int, db: Session = Depends(get_db)):
    """
    End-to-end sync for a single race weekend:
    - circuits, drivers, races (Ergast)
    - qualifying grid (Ergast)
    - driver mapping (OpenF1)
    - laps (OpenF1)
    - stints (FastF1)
    """
    try:
        ergast.fetch_circuits(db)
        ergast.fetch_drivers(db, season)
        ergast.fetch_races(db, season)

        ergast.fetch_qualifying(db, season, round_number)
        driver_map_stats = openf1.sync_driver_map(db, season, round_number)
        openf1.fetch_laps(db, season, round_number)
        fastf1_loader.fetch_stints(db, season, round_number)

        from app.db.models import Race, GridPosition, Lap, Stint, DriverNumberMap

        race = db.query(Race).filter_by(season=season, round_number=round_number).first()
        if not race:
            raise HTTPException(status_code=404, detail="Race not found after sync")

        return {
            "status": "synced_round",
            "season": season,
            "round_number": round_number,
            "race_id": race.id,
            "driver_map": driver_map_stats,
            "counts": {
                "grid_positions": db.query(GridPosition).filter_by(race_id=race.id).count(),
                "laps": db.query(Lap).filter_by(race_id=race.id).count(),
                "stints": db.query(Stint).filter_by(race_id=race.id).count(),
                "driver_number_map_season": db.query(DriverNumberMap).filter_by(season=season).count(),
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}")