from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.ingestion import ergast
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