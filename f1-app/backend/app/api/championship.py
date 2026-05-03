from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.prediction.championship_sim import predict_championship
from app.prediction.scenario_sim import predict_scenario
from app.db.models import Prediction

router = APIRouter()

@router.post("/championship/{season}")
def predict_season_championship(season: int, detailed: bool = False, db: Session = Depends(get_db)):
    try:
        results = predict_championship(db, season, detailed=detailed)
        return {"status": "success", "data": results}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/scenario/{season}/{driver_id}")
def simulate_to_win(season: int, driver_id: str, db: Session = Depends(get_db)):
    try:
        result = predict_scenario(db, season, driver_id)
        return {"status": "success", "data": result}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_predictions(season: int = None, race_id: str = None, db: Session = Depends(get_db)):
    query = db.query(Prediction)

    if season:
        query = query.filter(Prediction.season == season, Prediction.race_id == None)
    if race_id:
        query = query.filter(Prediction.race_id == race_id)

    results = query.all()
    return results