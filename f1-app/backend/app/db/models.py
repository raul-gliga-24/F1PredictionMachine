from sqlalchemy import (
    Column, Integer, Float, String, Boolean,
    DateTime, ForeignKey, JSON, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class Circuit(Base):
    __tablename__ = "circuits"

    id             = Column(String, primary_key=True)
    name           = Column(String, nullable=False)
    country        = Column(String)
    circuit_class  = Column(String)
    overtake_index = Column(Float)
    drs_zones      = Column(Integer)
    lap_length_km  = Column(Float)

    races = relationship("Race", back_populates="circuit")


class Driver(Base):
    __tablename__ = "drivers"

    id          = Column(String, primary_key=True)
    name        = Column(String, nullable=False)
    code        = Column(String)
    team        = Column(String)
    nationality = Column(String)

    laps   = relationship("Lap", back_populates="driver")
    stints = relationship("Stint", back_populates="driver")


class DriverNumberMap(Base):
    __tablename__ = "driver_number_map"
    __table_args__ = (
        UniqueConstraint("season", "driver_number", name="uq_driver_number_map_season_driver_number"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    season = Column(Integer, nullable=False)
    driver_number = Column(Integer, nullable=False)
    ergast_driver_id = Column(String, ForeignKey("drivers.id"), nullable=False)


class Race(Base):
    __tablename__ = "races"
    __table_args__ = (
        UniqueConstraint("season", "round_number", name="uq_races_season_round_number"),
    )

    id           = Column(Integer, primary_key=True, autoincrement=True)
    season       = Column(Integer, nullable=False)
    round_number = Column(Integer, nullable=False)
    circuit_id   = Column(String, ForeignKey("circuits.id"))
    race_date    = Column(DateTime)
    is_completed = Column(Boolean, default=False)

    circuit        = relationship("Circuit", back_populates="races")
    laps           = relationship("Lap", back_populates="race")
    stints         = relationship("Stint", back_populates="race")
    grid_positions = relationship("GridPosition", back_populates="race")
    predictions    = relationship("Prediction", back_populates="race")


class GridPosition(Base):
    __tablename__ = "grid_positions"
    __table_args__ = (
        UniqueConstraint("race_id", "driver_id", name="uq_grid_positions_race_driver"),
    )

    id                 = Column(Integer, primary_key=True, autoincrement=True)
    race_id            = Column(Integer, ForeignKey("races.id"))
    driver_id          = Column(String, ForeignKey("drivers.id"))
    position           = Column(Integer)
    q3_time_ms         = Column(Integer)
    tyre_compound      = Column(String)
    dirty_air_exposure = Column(Float)
    gap_ahead_ms       = Column(Integer)

    race = relationship("Race", back_populates="grid_positions")


class Lap(Base):
    __tablename__ = "laps"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    race_id       = Column(Integer, ForeignKey("races.id"))
    driver_id     = Column(String, ForeignKey("drivers.id"))
    lap_number    = Column(Integer)
    lap_time_ms   = Column(Integer)
    position      = Column(Integer)
    tyre_compound = Column(String)
    tyre_age      = Column(Integer)
    is_pit_lap    = Column(Boolean, default=False)
    gap_ahead_ms  = Column(Integer)

    race   = relationship("Race", back_populates="laps")
    driver = relationship("Driver", back_populates="laps")


class Stint(Base):
    __tablename__ = "stints"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    race_id        = Column(Integer, ForeignKey("races.id"))
    driver_id      = Column(String, ForeignKey("drivers.id"))
    stint_number   = Column(Integer)
    compound       = Column(String)
    start_lap      = Column(Integer)
    end_lap        = Column(Integer)
    avg_deg_ms     = Column(Float)
    optimal_window = Column(JSON)

    race   = relationship("Race", back_populates="stints")
    driver = relationship("Driver", back_populates="stints")


class Prediction(Base):
    __tablename__ = "predictions"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    race_id          = Column(Integer, ForeignKey("races.id"))
    created_at       = Column(DateTime, default=datetime.utcnow)
    prediction_type  = Column(String)
    predicted_order  = Column(JSON)
    reasoning_trace  = Column(Text)
    model_used       = Column(String)
    context_snapshot = Column(JSON)

    race = relationship("Race", back_populates="predictions")