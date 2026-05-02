from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.prediction.championship_sim import predict_championship
from app.db.models import Prediction

router = APIRouter()

@router.post("/championship/{season}")
def predict_season_championship(season: int, db: Session = Depends(get_db)):
    try:
        results = predict_championship(db, season)
        return {"status": "success", "data":results}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_predictions(season: int= None, race_id:str = None, db:Session = Depends(get_db)):
    query = db.query(Prediction)

    if season:
        query = query.filter(Prediction.season == season, Prediction.race_id == None)
    if race_id:
        query = query.filter(Prediction.race_id == race_id)

    results = query.all()
    return results