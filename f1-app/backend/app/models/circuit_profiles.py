# Circuit profiles — 2026 F1 season
#
# 2026 REGULATION CHANGES MODELED HERE:
# - DRS abolished. Replaced by Active Aero (X-mode = low drag, Z-mode = high downforce)
# - Overtake Mode = full MGU-K deployment for attack/defence on straights
# - 50/50 power split ICE/electric — battery management is now a race strategy element
# - Circuits with few recharge opportunities severely limit overtake mode availability
#
# KEY METRICS:
# overtake_index             : 0.0 = easy to pass, 1.0 = nearly impossible (Monaco-class)
# dirty_air_sensitivity      : lap time loss in seconds/lap when following within 1 second
# active_aero_effectiveness  : how well X-mode (low drag) aids overtaking on this layout 0.0-1.0
# overtake_mode_usability    : how often drivers can realistically deploy full battery 0.0-1.0
# battery_recharge_rating    : how well the circuit recharges the battery 0.0-1.0
#                              HIGH  = long straights + heavy braking zones (Monza, Baku)
#                              LOW   = flowing high-speed corners, few braking zones (Suzuka, Spa S1)
# battery_starvation_risk    : True if low recharge means overtake mode is rationed
# tyre_stress                : 0.0-1.0

CIRCUIT_PROFILES = {

    # ── Round 1 ───────────────────────────────────────────────────────────────
    "bahrain": {
        "round": 1,
        "name": "Bahrain Grand Prix",
        "circuit_class": "medium",
        "overtake_index": 0.35,
        "dirty_air_sensitivity": 0.40,
        "active_aero_effectiveness": 0.75,
        "overtake_mode_usability": 0.80,
        "battery_recharge_rating": 0.78,
        "battery_starvation_risk": False,
        "tyre_stress": 0.65,
        "lap_length_km": 5.412,
        "notes": (
            "Three heavy braking zones recharge battery consistently every lap. "
            "Overtake mode reliably available for T1 and T4 attacks. "
            "Active aero effective on main straight. Good circuit for 2026 regs."
        ),
    },

    # ── Round 2 ───────────────────────────────────────────────────────────────
    "jeddah": {
        "round": 2,
        "name": "Saudi Arabian Grand Prix",
        "circuit_class": "street",
        "overtake_index": 0.45,
        "dirty_air_sensitivity": 0.55,
        "active_aero_effectiveness": 0.85,
        "overtake_mode_usability": 0.80,
        "battery_recharge_rating": 0.82,
        "battery_starvation_risk": False,
        "tyre_stress": 0.50,
        "lap_length_km": 6.174,
        "notes": (
            "Longest sustained straight on the calendar — ideal for active aero and "
            "overtake mode. Heavy braking into T1 provides strong battery recharge. "
            "High walls limit off-line running so following remains difficult despite good "
            "battery availability."
        ),
    },

    # ── Round 3 ───────────────────────────────────────────────────────────────
    "albert_park": {
        "round": 3,
        "name": "Australian Grand Prix",
        "circuit_class": "medium",
        "overtake_index": 0.50,
        "dirty_air_sensitivity": 0.45,
        "active_aero_effectiveness": 0.65,
        "overtake_mode_usability": 0.65,
        "battery_recharge_rating": 0.60,
        "battery_starvation_risk": False,
        "tyre_stress": 0.55,
        "lap_length_km": 5.278,
        "notes": (
            "Mixed character circuit with moderate battery recharge. "
            "Safety car probability is high — battery-depleted cars may benefit "
            "from recharge during SC laps. Four DRS zones became four active aero zones."
        ),
    },

    # ── Round 4 ───────────────────────────────────────────────────────────────
    "suzuka": {
        "round": 4,
        "name": "Japanese Grand Prix",
        "circuit_class": "high_speed",
        "overtake_index": 0.70,
        "dirty_air_sensitivity": 0.80,
        "active_aero_effectiveness": 0.40,
        "overtake_mode_usability": 0.30,
        "battery_recharge_rating": 0.28,
        "battery_starvation_risk": True,
        "tyre_stress": 0.75,
        "lap_length_km": 5.807,
        "notes": (
            "BATTERY STARVATION RISK. Flowing high-speed layout provides almost no "
            "regeneration — S1 alone (Turns 1-9) drains the battery with zero recharge. "
            "Overtake mode is a scarce resource here. Drivers must choose between "
            "defending and attacking. Grid position is extremely important. "
            "Active aero less effective because speed differential on the straight is "
            "smaller when overtake mode is rationed."
        ),
    },

    # ── Round 5 ───────────────────────────────────────────────────────────────
    "shanghai": {
        "round": 5,
        "name": "Chinese Grand Prix",
        "circuit_class": "medium",
        "overtake_index": 0.40,
        "dirty_air_sensitivity": 0.40,
        "active_aero_effectiveness": 0.72,
        "overtake_mode_usability": 0.72,
        "battery_recharge_rating": 0.70,
        "battery_starvation_risk": False,
        "tyre_stress": 0.60,
        "lap_length_km": 5.451,
        "notes": (
            "Long T13-T16 back straight provides good active aero window. "
            "Heavy braking at T14 reliably recharges battery. "
            "Sprint weekend likely — battery management across sprint and race is key."
        ),
    },

    # ── Round 6 ───────────────────────────────────────────────────────────────
    "miami": {
        "round": 6,
        "name": "Miami Grand Prix",
        "circuit_class": "street",
        "overtake_index": 0.50,
        "dirty_air_sensitivity": 0.50,
        "active_aero_effectiveness": 0.65,
        "overtake_mode_usability": 0.65,
        "battery_recharge_rating": 0.60,
        "battery_starvation_risk": False,
        "tyre_stress": 0.60,
        "lap_length_km": 5.412,
        "notes": (
            "Wider than a traditional street circuit but walls still limit overtaking. "
            "Moderate battery recharge. Overtake mode available but not abundant — "
            "drivers will need to pick their moment carefully."
        ),
    },

    # ── Round 7 ───────────────────────────────────────────────────────────────
    "imola": {
        "round": 7,
        "name": "Emilia Romagna Grand Prix",
        "circuit_class": "medium",
        "overtake_index": 0.68,
        "dirty_air_sensitivity": 0.62,
        "active_aero_effectiveness": 0.55,
        "overtake_mode_usability": 0.50,
        "battery_recharge_rating": 0.48,
        "battery_starvation_risk": True,
        "tyre_stress": 0.55,
        "lap_length_km": 4.909,
        "notes": (
            "BATTERY STARVATION RISK. Tight and twisty layout with limited straight "
            "length means battery recharge is below the threshold for consistent "
            "overtake mode use. Piratella and Acque Minerali provide some regen "
            "but not enough. Qualifying position very important."
        ),
    },

    # ── Round 8 ───────────────────────────────────────────────────────────────
    "monaco": {
        "round": 8,
        "name": "Monaco Grand Prix",
        "circuit_class": "street",
        "overtake_index": 0.97,
        "dirty_air_sensitivity": 0.92,
        "active_aero_effectiveness": 0.05,
        "overtake_mode_usability": 0.15,
        "battery_recharge_rating": 0.20,
        "battery_starvation_risk": True,
        "tyre_stress": 0.30,
        "lap_length_km": 3.337,
        "notes": (
            "EXTREME BATTERY STARVATION. Shortest lap, lowest average speed, "
            "almost no meaningful straight — battery barely recharges per lap. "
            "Active aero provides negligible benefit in the tunnel and on the pit "
            "straight. Overtake mode is effectively useless — no room to use it. "
            "Race result determined almost entirely by qualifying. "
            "Strategy and pit stop execution are the only variables."
        ),
    },

    # ── Round 9 ───────────────────────────────────────────────────────────────
    "catalunya": {
        "round": 9,
        "name": "Spanish Grand Prix",
        "circuit_class": "medium",
        "overtake_index": 0.62,
        "dirty_air_sensitivity": 0.65,
        "active_aero_effectiveness": 0.60,
        "overtake_mode_usability": 0.58,
        "battery_recharge_rating": 0.55,
        "battery_starvation_risk": False,
        "tyre_stress": 0.72,
        "lap_length_km": 4.657,
        "notes": (
            "Long T10-T1 straight gives active aero a window but the rest of the "
            "lap is medium-speed corners that provide only moderate regen. "
            "Tyre deg is high — undercut strategy important. "
            "Dirty air sensitivity elevated in the twisty second sector."
        ),
    },

    # ── Round 10 ──────────────────────────────────────────────────────────────
    "villeneuve": {
        "round": 10,
        "name": "Canadian Grand Prix",
        "circuit_class": "medium",
        "overtake_index": 0.42,
        "dirty_air_sensitivity": 0.43,
        "active_aero_effectiveness": 0.72,
        "overtake_mode_usability": 0.75,
        "battery_recharge_rating": 0.74,
        "battery_starvation_risk": False,
        "tyre_stress": 0.55,
        "lap_length_km": 4.361,
        "notes": (
            "Wall of Champions hairpin provides strong braking-zone regen every lap. "
            "Long pit straight ideal for active aero. Safety car probability is high "
            "on this street-style permanent circuit — SC laps are free battery top-ups."
        ),
    },

    # ── Round 11 ──────────────────────────────────────────────────────────────
    "red_bull_ring": {
        "round": 11,
        "name": "Austrian Grand Prix",
        "circuit_class": "high_speed",
        "overtake_index": 0.32,
        "dirty_air_sensitivity": 0.35,
        "active_aero_effectiveness": 0.80,
        "overtake_mode_usability": 0.82,
        "battery_recharge_rating": 0.80,
        "battery_starvation_risk": False,
        "tyre_stress": 0.60,
        "lap_length_km": 4.318,
        "notes": (
            "Short lap but three heavy braking zones (T1, T3, T4) recharge battery "
            "aggressively. Overtake mode very usable — drivers can deploy multiple "
            "times per lap. Active aero effective on the main straight. "
            "One of the best circuits for 2026 power unit regulations."
        ),
    },

    # ── Round 12 ──────────────────────────────────────────────────────────────
    "silverstone": {
        "round": 12,
        "name": "British Grand Prix",
        "circuit_class": "high_speed",
        "overtake_index": 0.42,
        "dirty_air_sensitivity": 0.55,
        "active_aero_effectiveness": 0.68,
        "overtake_mode_usability": 0.55,
        "battery_recharge_rating": 0.52,
        "battery_starvation_risk": False,
        "tyre_stress": 0.82,
        "lap_length_km": 5.891,
        "notes": (
            "High-speed sweepers (Maggotts-Becketts-Chapel) drain battery hard with "
            "minimal regen. Hangar straight and Wellington straight provide recharge "
            "windows but not enough to fully offset. Tyre deg is the highest on the "
            "calendar — strategy will dominate. Overtake mode available but rationed."
        ),
    },

    # ── Round 13 ──────────────────────────────────────────────────────────────
    "hungaroring": {
        "round": 13,
        "name": "Hungarian Grand Prix",
        "circuit_class": "low_speed",
        "overtake_index": 0.78,
        "dirty_air_sensitivity": 0.78,
        "active_aero_effectiveness": 0.42,
        "overtake_mode_usability": 0.38,
        "battery_recharge_rating": 0.35,
        "battery_starvation_risk": True,
        "tyre_stress": 0.65,
        "lap_length_km": 4.381,
        "notes": (
            "BATTERY STARVATION RISK. Slowest permanent circuit on the calendar. "
            "Constant medium-speed direction changes provide almost no regen per lap. "
            "The single short straight barely allows active aero to work. "
            "Overtake mode is a once-per-lap luxury at best. "
            "Quali result is decisive — this is the new Monaco for strategy."
        ),
    },

    # ── Round 14 ──────────────────────────────────────────────────────────────
    "spa": {
        "round": 14,
        "name": "Belgian Grand Prix",
        "circuit_class": "high_speed",
        "overtake_index": 0.35,
        "dirty_air_sensitivity": 0.50,
        "active_aero_effectiveness": 0.85,
        "overtake_mode_usability": 0.55,
        "battery_recharge_rating": 0.58,
        "battery_starvation_risk": False,
        "tyre_stress": 0.70,
        "lap_length_km": 7.004,
        "notes": (
            "Kemmel straight is the best active aero opportunity on the calendar. "
            "However Eau Rouge / Raidillon and Pouhon are high-speed non-braking "
            "sections that drain the battery. Bus Stop chicane provides strong regen. "
            "Net result: battery is available for Kemmel but drivers must be careful "
            "not to overdeploy earlier. Weather variability adds strategy complexity."
        ),
    },

    # ── Round 15 ──────────────────────────────────────────────────────────────
    "zandvoort": {
        "round": 15,
        "name": "Dutch Grand Prix",
        "circuit_class": "medium",
        "overtake_index": 0.82,
        "dirty_air_sensitivity": 0.72,
        "active_aero_effectiveness": 0.38,
        "overtake_mode_usability": 0.35,
        "battery_recharge_rating": 0.32,
        "battery_starvation_risk": True,
        "tyre_stress": 0.72,
        "lap_length_km": 4.259,
        "notes": (
            "BATTERY STARVATION RISK. Banked Hugenholtz and Arie Luyendyk corners "
            "are sustained high-lateral-load non-braking sections — no regen at all. "
            "Short pit straight limits active aero window. "
            "Overtake mode is extremely scarce. This is effectively an un-overtakeable "
            "circuit under 2026 regs unless a safety car reshuffles the order. "
            "Qualifying result is almost definitive."
        ),
    },

    # ── Round 16 ──────────────────────────────────────────────────────────────
    "monza": {
        "round": 16,
        "name": "Italian Grand Prix",
        "circuit_class": "high_speed",
        "overtake_index": 0.28,
        "dirty_air_sensitivity": 0.28,
        "active_aero_effectiveness": 0.95,
        "overtake_mode_usability": 0.95,
        "battery_recharge_rating": 0.95,
        "battery_starvation_risk": False,
        "tyre_stress": 0.30,
        "lap_length_km": 5.793,
        "notes": (
            "BEST CIRCUIT FOR 2026 REGS. Three massive braking zones (T1, Roggia, "
            "Lesmo, Ascari, Parabolica) recharge the battery to near full every lap. "
            "Overtake mode is freely available — drivers can deploy multiple times "
            "per lap on all three straights. Active aero extremely effective at "
            "200+ mph speed differentials. Slipstream + active aero + overtake mode "
            "combine for the most overtaking opportunities of the season."
        ),
    },

    # ── Round 17 ──────────────────────────────────────────────────────────────
    "baku": {
        "round": 17,
        "name": "Azerbaijan Grand Prix",
        "circuit_class": "street",
        "overtake_index": 0.38,
        "dirty_air_sensitivity": 0.43,
        "active_aero_effectiveness": 0.90,
        "overtake_mode_usability": 0.88,
        "battery_recharge_rating": 0.85,
        "battery_starvation_risk": False,
        "tyre_stress": 0.45,
        "lap_length_km": 6.003,
        "notes": (
            "Second longest straight on the calendar. Heavy braking from 200+ mph "
            "into T1 is one of the best single-corner regen events of the year. "
            "Old town section provides additional braking regen. "
            "Safety car probability is very high — SC laps are free recharges. "
            "Active aero and overtake mode near-freely available."
        ),
    },

    # ── Round 18 ──────────────────────────────────────────────────────────────
    "marina_bay": {
        "round": 18,
        "name": "Singapore Grand Prix",
        "circuit_class": "street",
        "overtake_index": 0.82,
        "dirty_air_sensitivity": 0.80,
        "active_aero_effectiveness": 0.32,
        "overtake_mode_usability": 0.28,
        "battery_recharge_rating": 0.25,
        "battery_starvation_risk": True,
        "tyre_stress": 0.55,
        "lap_length_km": 4.940,
        "notes": (
            "EXTREME BATTERY STARVATION RISK. Longest lap time on the calendar "
            "(over 100 seconds) but almost entirely low-speed chicanes and 90-degree "
            "corners with minimal straight length. Battery barely recharges per lap. "
            "Overtake mode is a once-per-lap gamble. Active aero almost useless. "
            "Combined with narrow walls, this is effectively Monaco-tier for overtaking. "
            "Safety car is near-certain (historically 90%+ probability) — "
            "SC laps are critical battery recovery windows."
        ),
    },

    # ── Round 19 ──────────────────────────────────────────────────────────────
    "americas": {
        "round": 19,
        "name": "United States Grand Prix",
        "circuit_class": "medium",
        "overtake_index": 0.45,
        "dirty_air_sensitivity": 0.50,
        "active_aero_effectiveness": 0.68,
        "overtake_mode_usability": 0.68,
        "battery_recharge_rating": 0.65,
        "battery_starvation_risk": False,
        "tyre_stress": 0.72,
        "lap_length_km": 5.513,
        "notes": (
            "Back straight is the primary active aero / overtake mode zone. "
            "Heavy T12 braking recharges well. High tyre deg means strategy "
            "often overrides on-track passes. Sprint weekend likely."
        ),
    },

    # ── Round 20 ──────────────────────────────────────────────────────────────
    "rodriguez": {
        "round": 20,
        "name": "Mexico City Grand Prix",
        "circuit_class": "medium",
        "overtake_index": 0.48,
        "dirty_air_sensitivity": 0.45,
        "active_aero_effectiveness": 0.72,
        "overtake_mode_usability": 0.70,
        "battery_recharge_rating": 0.70,
        "battery_starvation_risk": False,
        "tyre_stress": 0.50,
        "lap_length_km": 4.304,
        "notes": (
            "High altitude (2285m) means ICE produces ~20% less power — "
            "the electric MGU-K component becomes proportionally more important here "
            "than anywhere else on the calendar. Battery management is critical. "
            "Stadium section provides good regen. Long main straight ideal for "
            "active aero and overtake mode."
        ),
    },

    # ── Round 21 ──────────────────────────────────────────────────────────────
    "interlagos": {
        "round": 21,
        "name": "São Paulo Grand Prix",
        "circuit_class": "medium",
        "overtake_index": 0.38,
        "dirty_air_sensitivity": 0.40,
        "active_aero_effectiveness": 0.72,
        "overtake_mode_usability": 0.73,
        "battery_recharge_rating": 0.72,
        "battery_starvation_risk": False,
        "tyre_stress": 0.62,
        "lap_length_km": 4.309,
        "notes": (
            "Anti-clockwise layout with good regen at Senna S and Ferradura. "
            "Descida do Lago straight is prime active aero territory. "
            "Unpredictable weather is a major strategy wildcard — "
            "rain resets all battery models. Sprint weekend likely."
        ),
    },

    # ── Round 22 ──────────────────────────────────────────────────────────────
    "vegas": {
        "round": 22,
        "name": "Las Vegas Grand Prix",
        "circuit_class": "street",
        "overtake_index": 0.38,
        "dirty_air_sensitivity": 0.43,
        "active_aero_effectiveness": 0.85,
        "overtake_mode_usability": 0.85,
        "battery_recharge_rating": 0.82,
        "battery_starvation_risk": False,
        "tyre_stress": 0.40,
        "lap_length_km": 6.201,
        "notes": (
            "Long Las Vegas Boulevard straight is ideal for active aero. "
            "Three main braking zones provide solid regen. "
            "Cold night temperatures affect both tyres and battery performance — "
            "battery thermal management is a unique consideration here. "
            "Low tyre deg means strategy is less variable."
        ),
    },

    # ── Round 23 ──────────────────────────────────────────────────────────────
    "losail": {
        "round": 23,
        "name": "Qatar Grand Prix",
        "circuit_class": "medium",
        "overtake_index": 0.50,
        "dirty_air_sensitivity": 0.52,
        "active_aero_effectiveness": 0.65,
        "overtake_mode_usability": 0.62,
        "battery_recharge_rating": 0.60,
        "battery_starvation_risk": False,
        "tyre_stress": 0.78,
        "lap_length_km": 5.380,
        "notes": (
            "Flowing medium-speed layout with moderate regen. "
            "Extremely high tyre degradation — highest on calendar alongside Silverstone. "
            "Strategy (especially undercut) will dominate over on-track passes. "
            "Sprint weekend likely. Heat adds thermal stress to battery systems."
        ),
    },

    # ── Round 24 ──────────────────────────────────────────────────────────────
    "yas_marina": {
        "round": 24,
        "name": "Abu Dhabi Grand Prix",
        "circuit_class": "medium",
        "overtake_index": 0.45,
        "dirty_air_sensitivity": 0.45,
        "active_aero_effectiveness": 0.72,
        "overtake_mode_usability": 0.72,
        "battery_recharge_rating": 0.68,
        "battery_starvation_risk": False,
        "tyre_stress": 0.50,
        "lap_length_km": 5.281,
        "notes": (
            "Season finale. Revised layout (2021+) improved overtaking. "
            "Long back straight is the main active aero zone. "
            "Moderate battery recharge — overtake mode available but not abundant. "
            "Championship battles often decided here under strategic pressure."
        ),
    },
}


def get_circuit_profile(circuit_id: str) -> dict:
    """
    Returns the profile for a given circuit ID.
    Falls back to a generic medium-circuit profile if not found.
    """
    profile = CIRCUIT_PROFILES.get(circuit_id)
    if profile:
        return profile

    # Generic fallback for any circuit not in the list
    return {
        "round": 0,
        "name": circuit_id,
        "circuit_class": "medium",
        "overtake_index": 0.50,
        "dirty_air_sensitivity": 0.50,
        "active_aero_effectiveness": 0.60,
        "overtake_mode_usability": 0.60,
        "battery_recharge_rating": 0.60,
        "battery_starvation_risk": False,
        "tyre_stress": 0.60,
        "lap_length_km": 5.0,
        "notes": "Unknown circuit — using generic medium profile.",
    }


def get_battery_starvation_circuits() -> list:
    """Returns list of circuit IDs where battery starvation is a risk."""
    return [
        cid for cid, profile in CIRCUIT_PROFILES.items()
        if profile.get("battery_starvation_risk")
    ]


def get_circuits_by_round() -> list:
    """Returns circuits sorted by round number."""
    return sorted(CIRCUIT_PROFILES.items(), key=lambda x: x[1]["round"])