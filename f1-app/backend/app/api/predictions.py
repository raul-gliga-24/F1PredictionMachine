from fastapi import APIRouter
from app.models.dirty_air import calculate_grid_dirty_air
from app.models.tyre_deg import calculate_full_strategy

router = APIRouter()

@router.get("/")
def get_predictions():
    return {"predictions": []}

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
