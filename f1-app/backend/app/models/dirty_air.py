from app.models.circuit_profiles import get_circuit_profile


def calculate_dirty_air_exposure(grid_position: int, circuit_id: str) -> dict:
    """
    Calculates how much a driver will suffer from dirty air based on
    their grid position and the circuit characteristics.

    Returns a dict with exposure score and lap time penalty estimate.
    """
    profile = get_circuit_profile(circuit_id)

    # P1 has zero dirty air — clean air all race
    if grid_position == 1:
        return {
            "exposure_score": 0.0,
            "lap_time_penalty_sec": 0.0,
            "overtake_mode_available": 1.0,
            "notes": "Clean air — no dirty air exposure"
        }

    # Base exposure increases with grid position
    # P2 is slightly exposed, P10+ is heavily exposed at race start
    base_exposure = min((grid_position - 1) * 0.08, 0.85)

    # Adjust for circuit dirty air sensitivity
    sensitivity = profile["dirty_air_sensitivity"]
    exposure_score = round(base_exposure * sensitivity, 3)

    # Lap time penalty in seconds per lap when stuck in traffic
    lap_time_penalty = round(exposure_score * 0.6, 3)

    # Battery starvation makes overtaking even harder —
    # if you can't deploy overtake mode freely, dirty air is more punishing
    battery_rating = profile["battery_recharge_rating"]
    overtake_mode_available = round(
        profile["overtake_mode_usability"] * (1 - exposure_score * 0.3), 3
    )

    # Flag high risk situations
    is_high_risk = (
        exposure_score > 0.5 or
        profile["battery_starvation_risk"] and grid_position > 5
    )

    return {
        "exposure_score": exposure_score,
        "lap_time_penalty_sec": lap_time_penalty,
        "overtake_mode_available": overtake_mode_available,
        "battery_recharge_rating": battery_rating,
        "battery_starvation_risk": profile["battery_starvation_risk"],
        "active_aero_effectiveness": profile["active_aero_effectiveness"],
        "is_high_risk": is_high_risk,
        "notes": (
            f"Grid P{grid_position} at {profile['name']}. "
            f"Exposure: {exposure_score:.2f}. "
            f"Estimated {lap_time_penalty:.2f}s/lap penalty in traffic. "
            + ("WARNING: Battery starvation circuit — overtake mode severely limited." 
               if profile["battery_starvation_risk"] else "")
        )
    }


def calculate_grid_dirty_air(grid: list, circuit_id: str) -> list:
    """
    Takes a full grid and returns dirty air scores for every driver.

    grid = [
        {"position": 1, "driver_id": "max_verstappen"},
        {"position": 2, "driver_id": "lando_norris"},
        ...
    ]
    """
    results = []
    for entry in grid:
        score = calculate_dirty_air_exposure(entry["position"], circuit_id)
        results.append({
            "driver_id": entry["driver_id"],
            "grid_position": entry["position"],
            **score
        })
    return results