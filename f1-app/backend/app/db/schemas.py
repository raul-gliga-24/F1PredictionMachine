from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CircuitBase(BaseModel):
    id: str
    name: str
    circuit_class: str
    overtake_index: float
    drs_zones: int

class CircuitRead(CircuitBase):
    class Config:
        from_attributes = True


class DriverBase(BaseModel):
    id: str
    name: str
    code: str
    team: str

class DriverRead(DriverBase):
    class Config:
        from_attributes = True


class RaceRead(BaseModel):
    id: int
    season: int
    round_number: int
    circuit_id: str
    race_date: Optional[datetime]
    is_completed: bool

    class Config:
        from_attributes = True


class PredictionRead(BaseModel):
    id: int
    race_id: int
    created_at: datetime
    prediction_type: str
    predicted_order: list
    reasoning_trace: str
    model_used: str

    class Config:
        from_attributes = True