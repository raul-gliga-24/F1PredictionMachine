from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.prediction.race_context import build_prediction_context
from app.models.dirty_air import calculate_grid_dirty_air
from app.models.tyre_deg import calculate_full_strategy
from app.core.redis import cache_response


router = APIRouter()

@router.get("/")
def get_predictions(db: Session = Depends(get_db)):
    from app.db.models import Prediction
    predictions = db.query(Prediction).order_by(Prediction.created_at.desc()).all()
    return {"predictions": [
        {
            "id": p.id,
            "race_id": p.race_id,
            "prediction_type": p.prediction_type,
            "predicted_order": p.predicted_order,
            "reasoning_trace": p.reasoning_trace,
            "model_used": p.model_used,
            "created_at": p.created_at
        } for p in predictions
    ]}

@router.get("/test/dirty-air/{circuit_id}")
def test_dirty_air(circuit_id: str):
    sample_grid = [
        {"position": 1, "driver_id": "verstappen"},
        {"position": 2, "driver_id": "norris"},
        {"position": 3, "driver_id": "leclerc"},
        {"position": 4, "driver_id": "hamilton"},
        {"position": 5, "driver_id": "russell"},
        {"position": 10, "driver_id": "alonso"},
        {"position": 15, "driver_id": "stroll"},
        {"position": 20, "driver_id": "bottas"},
    ]
    return {"circuit": circuit_id, "grid": calculate_grid_dirty_air(sample_grid, circuit_id)}

@router.get("/test/strategy/{circuit_id}")
def test_strategy(circuit_id: str, laps: int = 57, temp: float = 35.0):
    return calculate_full_strategy(circuit_id, laps, temp)

@router.get("/pre-race/context/{season}/{round_number}")
@cache_response(expire_seconds=86400) # Cache for 24 hours
def preview_pre_race_context(

    season : int,
    round_number : int,
    early_season_threshold: int = 3,
    db: Session = Depends(get_db),
):
    return build_prediction_context(db, season, round_number, early_season_threshold)

@router.post("/pre-race/{season}/{round_number}")
@cache_response(expire_seconds=86400) # Cache for 24 hours
def run_pre_race_prediction(

    season: int,
    round_number: int,
    early_season_threshold: int = 3,
    db: Session = Depends(get_db),
):
    try:
        from app.prediction.race_predictor import predict_race
        return predict_race(db, season, round_number, early_season_threshold)
    except Exception as e:
        import traceback
        with open("C:/Users/raulg/Desktop/Project/F1 predict/f1-app/error.log", "w") as f:
            f.write(traceback.format_exc())
        raise e
