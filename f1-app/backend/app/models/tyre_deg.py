from app.models.circuit_profiles import get_circuit_profile


# Baseline deg rates (seconds of lap time lost per lap) per compound
# These are starting points — refined later using real FastF1 historical data
BASELINE_DEG_RATES = {
    "soft":   0.085,
    "medium": 0.042,
    "hard":   0.018,
    "inter":  0.025,
    "wet":    0.015,
}

# Optimal stint lengths per compound before deg becomes too costly
OPTIMAL_STINT_LENGTH = {
    "soft":   {"min": 10, "max": 20},
    "medium": {"min": 18, "max": 35},
    "hard":   {"min": 28, "max": 50},
    "inter":  {"min": 5,  "max": 25},
    "wet":    {"min": 5,  "max": 30},
}


def calculate_deg_rate(compound: str, circuit_id: str, track_temp_c: float = 35.0) -> dict:
    """
    Calculates tyre degradation rate for a given compound at a given circuit.
    Adjusts for track temperature and circuit tyre stress.
    """
    profile = get_circuit_profile(circuit_id)
    base_rate = BASELINE_DEG_RATES.get(compound.lower(), 0.042)
    tyre_stress = profile["tyre_stress"]

    # Temperature adjustment — every 10°C above 30°C adds 8% more deg on softs,
    # 5% on mediums, 2% on hards
    temp_multipliers = {"soft": 0.008, "medium": 0.005, "hard": 0.002}
    temp_mult = temp_multipliers.get(compound.lower(), 0.005)
    temp_delta = max(0, track_temp_c - 30)
    temp_adjustment = 1 + (temp_delta * temp_mult)

    # Final deg rate
    deg_rate = round(base_rate * tyre_stress * temp_adjustment, 4)

    return {
        "compound": compound,
        "circuit_id": circuit_id,
        "deg_rate_sec_per_lap": deg_rate,
        "tyre_stress": tyre_stress,
        "track_temp_c": track_temp_c,
        "notes": (
            f"{compound.capitalize()} at {profile['name']}: "
            f"{deg_rate:.4f}s/lap degradation at {track_temp_c}°C track temp."
        )
    }


def calculate_pit_window(
    compound: str,
    circuit_id: str,
    race_laps: int = 57,
    track_temp_c: float = 35.0
) -> dict:
    """
    Calculates the optimal pit window for a given compound.
    Returns earliest, optimal, and latest lap to pit.
    """
    deg_info = calculate_deg_rate(compound, circuit_id, track_temp_c)
    deg_rate = deg_info["deg_rate_sec_per_lap"]
    stint_range = OPTIMAL_STINT_LENGTH.get(compound.lower(), {"min": 15, "max": 30})

    # If deg rate is very high, shorten the window
    if deg_rate > 0.07:
        adjustment = -5
    elif deg_rate > 0.05:
        adjustment = -2
    else:
        adjustment = 0

    earliest = max(1, stint_range["min"] + adjustment)
    optimal  = int((stint_range["min"] + stint_range["max"]) / 2) + adjustment
    latest   = min(race_laps - 5, stint_range["max"] + adjustment)

    return {
        "compound": compound,
        "earliest_lap": earliest,
        "optimal_lap": optimal,
        "latest_lap": latest,
        "deg_rate_sec_per_lap": deg_rate,
        "undercut_vulnerability": deg_rate > 0.06,
        "notes": (
            f"Pit window for {compound} at {get_circuit_profile(circuit_id)['name']}: "
            f"laps {earliest}–{latest}, optimal lap {optimal}. "
            + ("HIGH undercut vulnerability." if deg_rate > 0.06 else "")
        )
    }


def calculate_full_strategy(
    circuit_id: str,
    race_laps: int = 57,
    track_temp_c: float = 35.0
) -> dict:
    """
    Returns a full one-stop and two-stop strategy recommendation
    for a given circuit, including pit windows for all compounds.
    """
    compounds = ["soft", "medium", "hard"]
    windows = {
        c: calculate_pit_window(c, circuit_id, race_laps, track_temp_c)
        for c in compounds
    }

    profile = get_circuit_profile(circuit_id)

    # Recommend one-stop vs two-stop based on tyre stress
    if profile["tyre_stress"] > 0.70:
        recommendation = "two_stop"
        strategy_note = "High tyre stress — two stop likely optimal."
    elif profile["tyre_stress"] > 0.55:
        recommendation = "one_or_two_stop"
        strategy_note = "Medium tyre stress — one or two stop depending on safety car."
    else:
        recommendation = "one_stop"
        strategy_note = "Low tyre stress — one stop should be sufficient."

    return {
        "circuit_id": circuit_id,
        "circuit_name": profile["name"],
        "race_laps": race_laps,
        "track_temp_c": track_temp_c,
        "strategy_recommendation": recommendation,
        "strategy_note": strategy_note,
        "pit_windows": windows,
    }