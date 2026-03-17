# Team and car performance ratings — 2026 F1 season
#
# CORRECT 2026 POWER UNIT LANDSCAPE:
# Mercedes  → Mercedes works, McLaren, Williams, Alpine
# Ferrari   → Ferrari works, Haas, Cadillac (new team)
# Ford      → Red Bull, RB (Red Bull Powertrains + Ford)
# Honda     → Aston Martin (customer only)
# Audi      → Sauber (full factory takeover)

TEAM_PERFORMANCE_2026 = {

    "mclaren": {
        "full_name": "McLaren F1 Team",
        "power_unit": "mercedes",
        "pace_rating": 0.92,
        "race_pace_rating": 0.92,
        "reliability": 0.89,
        "development_trend": "stable",
        "pu_competitiveness": 0.92,
        "last_updated_round": 1,
        "notes": (
            "Title favourites. Best chassis combined with best PU. "
            "Norris is the benchmark. Piastri pushing every weekend. "
            "Mercedes PU advantage amplified by McLaren aero efficiency."
        ),
    },

    "mercedes": {
        "full_name": "Mercedes-AMG Petronas",
        "power_unit": "mercedes",
        "pace_rating": 0.88,
        "race_pace_rating": 0.88,
        "reliability": 0.92,
        "development_trend": "improving",
        "pu_competitiveness": 0.92,
        "last_updated_round": 1,
        "notes": (
            "Best PU on the grid in 2026. Lost Hamilton to Ferrari. "
            "Russell leads the works team. Best reliability of any constructor."
        ),
    },

    "ferrari": {
        "full_name": "Scuderia Ferrari",
        "power_unit": "ferrari",
        "pace_rating": 0.88,
        "race_pace_rating": 0.86,
        "reliability": 0.83,
        "development_trend": "improving",
        "pu_competitiveness": 0.88,
        "last_updated_round": 1,
        "notes": (
            "Second best PU in 2026. Hamilton joined — best driver pairing "
            "on the grid with Leclerc. Car suits new regs. "
            "Strategy department still a weak point."
        ),
    },

    "red_bull": {
        "full_name": "Oracle Red Bull Racing",
        "power_unit": "ford",
        "pace_rating": 0.84,
        "race_pace_rating": 0.83,
        "reliability": 0.79,
        "development_trend": "stable",
        "pu_competitiveness": 0.82,
        "last_updated_round": 1,
        "notes": (
            "Cut ties with Honda, now on Ford PU (Red Bull Powertrains + Ford). "
            "Year one reliability risk is real. Verstappen masks the PU gap "
            "to Mercedes and Ferrari. Ford bringing major investment."
        ),
    },

    "williams": {
        "full_name": "Williams Racing",
        "power_unit": "mercedes",
        "pace_rating": 0.76,
        "race_pace_rating": 0.75,
        "reliability": 0.85,
        "development_trend": "improving",
        "pu_competitiveness": 0.92,
        "last_updated_round": 1,
        "notes": (
            "Mercedes PU is a huge asset. Sainz joined and elevated the team. "
            "Best of the rest on power circuits — Monza, Baku, Las Vegas."
        ),
    },

    "alpine": {
        "full_name": "BWT Alpine F1 Team",
        "power_unit": "mercedes",
        "pace_rating": 0.74,
        "race_pace_rating": 0.73,
        "reliability": 0.83,
        "development_trend": "improving",
        "pu_competitiveness": 0.92,
        "last_updated_round": 1,
        "notes": (
            "Switched from Renault to Mercedes PU for 2026 — transformative upgrade. "
            "No longer at a power deficit. Moved from backmarker to genuine "
            "points contender every single weekend."
        ),
    },

    "haas": {
        "full_name": "MoneyGram Haas F1 Team",
        "power_unit": "ferrari",
        "pace_rating": 0.71,
        "race_pace_rating": 0.70,
        "reliability": 0.79,
        "development_trend": "stable",
        "pu_competitiveness": 0.88,
        "last_updated_round": 1,
        "notes": (
            "Ferrari PU gives Haas a strong engine in the midfield. "
            "Chassis limited by budget. Points on power circuits. Consistent."
        ),
    },

    "rb": {
        "full_name": "Visa Cash App RB",
        "power_unit": "ford",
        "pace_rating": 0.72,
        "race_pace_rating": 0.71,
        "reliability": 0.78,
        "development_trend": "stable",
        "pu_competitiveness": 0.82,
        "last_updated_round": 1,
        "notes": (
            "Same Ford PU as Red Bull works — same reliability risk year one. "
            "Benefits from Red Bull technical transfer within budget cap."
        ),
    },

    "aston_martin": {
        "full_name": "Aston Martin Aramco",
        "power_unit": "honda",
        "pace_rating": 0.58,
        "race_pace_rating": 0.56,
        "reliability": 0.80,
        "development_trend": "declining",
        "pu_competitiveness": 0.81,
        "last_updated_round": 1,
        "notes": (
            "STRUGGLING IN 2026. Kept Honda after Red Bull switched to Ford. "
            "Honda customer-only supply is decent but the chassis is the problem — "
            "completely failed to adapt to new regs. "
            "Alonso performing miracles just to score occasional points. "
            "Major update package expected mid-season."
        ),
    },

    "sauber": {
        "full_name": "Audi F1 Team",
        "power_unit": "audi",
        "pace_rating": 0.62,
        "race_pace_rating": 0.61,
        "reliability": 0.70,
        "development_trend": "improving",
        "pu_competitiveness": 0.76,
        "last_updated_round": 1,
        "notes": (
            "Audi full factory takeover complete. Brand new PU in year one — "
            "reliability is the biggest unknown on the grid. "
            "Currently behind all other PU suppliers on outright power. "
            "Heavy investment means strong improvement expected. "
            "2026 is a learning year."
        ),
    },

    "cadillac": {
        "full_name": "Cadillac F1 Team",
        "power_unit": "ferrari",
        "pace_rating": 0.62,
        "race_pace_rating": 0.60,
        "reliability": 0.72,
        "development_trend": "improving",
        "pu_competitiveness": 0.88,
        "last_updated_round": 1,
        "notes": (
            "NEW TEAM for 2026. First American F1 constructor in decades. "
            "Running Ferrari PU — excellent engine, inexperienced operation. "
            "First-year chassis expected to be off the pace. "
            "Ferrari PU means no embarrassment on straights. "
            "Pit crew and strategy experience are the main gaps. "
            "Expect significant improvement across the season."
        ),
    },
}


DRIVER_RATINGS_2026 = {
    "max_verstappen": {
        "team": "red_bull",
        "pace_rating": 0.98,
        "overtake_aggression": 0.90,
        "wet_weather_skill": 0.97,
        "tyre_management": 0.92,
        "qualifying_delta": -0.25,
        "notes": "Best driver on the grid. Extracts more than the car deserves."
    },
    "lando_norris": {
        "team": "mclaren",
        "pace_rating": 0.95,
        "overtake_aggression": 0.82,
        "wet_weather_skill": 0.88,
        "tyre_management": 0.86,
        "qualifying_delta": -0.20,
        "notes": "Title favourite. Best car and a top-3 driver."
    },
    "oscar_piastri": {
        "team": "mclaren",
        "pace_rating": 0.91,
        "overtake_aggression": 0.80,
        "wet_weather_skill": 0.85,
        "tyre_management": 0.84,
        "qualifying_delta": -0.10,
        "notes": "Pushing Norris hard every weekend. Underrated."
    },
    "charles_leclerc": {
        "team": "ferrari",
        "pace_rating": 0.94,
        "overtake_aggression": 0.85,
        "wet_weather_skill": 0.87,
        "tyre_management": 0.80,
        "qualifying_delta": -0.18,
        "notes": "Exceptional qualifier. Hamilton as teammate adds pressure."
    },
    "lewis_hamilton": {
        "team": "ferrari",
        "pace_rating": 0.93,
        "overtake_aggression": 0.88,
        "wet_weather_skill": 0.96,
        "tyre_management": 0.95,
        "qualifying_delta": -0.10,
        "notes": (
            "Moved to Ferrari for 2026. Adapting to new car. "
            "Tyre management and wet weather are world class."
        )
    },
    "george_russell": {
        "team": "mercedes",
        "pace_rating": 0.91,
        "overtake_aggression": 0.80,
        "wet_weather_skill": 0.85,
        "tyre_management": 0.87,
        "qualifying_delta": -0.15,
        "notes": "Leads Mercedes works team. Consistent and clinical."
    },
    "carlos_sainz": {
        "team": "williams",
        "pace_rating": 0.91,
        "overtake_aggression": 0.86,
        "wet_weather_skill": 0.88,
        "tyre_management": 0.90,
        "qualifying_delta": -0.15,
        "notes": "Moved to Williams. Immediately made them a threat."
    },
    "fernando_alonso": {
        "team": "aston_martin",
        "pace_rating": 0.92,
        "overtake_aggression": 0.92,
        "wet_weather_skill": 0.93,
        "tyre_management": 0.96,
        "qualifying_delta": -0.20,
        "notes": (
            "Elite driver in an uncompetitive car. "
            "Keeping Aston Martin relevant through pure racecraft. Legend."
        )
    },
    "lance_stroll": {
        "team": "aston_martin",
        "pace_rating": 0.74,
        "overtake_aggression": 0.65,
        "wet_weather_skill": 0.72,
        "tyre_management": 0.75,
        "qualifying_delta": 0.30,
        "notes": "Consistent but well below Alonso."
    },
}


def get_team_performance(team_id: str) -> dict:
    return TEAM_PERFORMANCE_2026.get(team_id, {
        "pace_rating": 0.65,
        "race_pace_rating": 0.65,
        "reliability": 0.80,
        "development_trend": "unknown",
        "pu_competitiveness": 0.75,
        "notes": "Unknown team — using generic midfield profile."
    })


def get_driver_rating(driver_id: str) -> dict:
    return DRIVER_RATINGS_2026.get(driver_id, {
        "pace_rating": 0.78,
        "overtake_aggression": 0.75,
        "wet_weather_skill": 0.78,
        "tyre_management": 0.78,
        "qualifying_delta": 0.0,
        "notes": "Unknown driver — using generic midfield profile."
    })


def get_power_unit_ranking() -> list:
    return [
        {
            "pu": "mercedes",
            "rating": 0.92,
            "teams": ["mercedes", "mclaren", "williams", "alpine"],
            "note": "Best PU on the grid. Four teams benefit."
        },
        {
            "pu": "ferrari",
            "rating": 0.88,
            "teams": ["ferrari", "haas", "cadillac"],
            "note": "Strong and proven. Cadillac get a solid base as new team."
        },
        {
            "pu": "ford",
            "rating": 0.82,
            "teams": ["red_bull", "rb"],
            "note": "Year one — Red Bull Powertrains + Ford. Reliability risk."
        },
        {
            "pu": "honda",
            "rating": 0.81,
            "teams": ["aston_martin"],
            "note": "Customer-only supply. No longer a works partnership."
        },
        {
            "pu": "audi",
            "rating": 0.76,
            "teams": ["sauber"],
            "note": "Brand new PU. Learning year. Heavy investment behind it."
        },
    ]