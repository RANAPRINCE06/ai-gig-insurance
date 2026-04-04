"""
Premium calculation service.
Formula: base_premium × zone_multiplier × history_multiplier × season_multiplier
"""

PLAN_BASE = {"Basic": 29, "Standard": 49, "Premium": 79}

ZONE_MULTIPLIERS = {
    "High": 1.4,
    "Medium": 1.2,
    "Normal": 1.0,
    "Low": 0.9,
}

SEASON_MULTIPLIERS = {
    "Monsoon": 1.3,
    "Summer": 1.2,
    "Normal": 1.0,
    "Winter": 0.95,
}


def compute_premium(worker, plan: str) -> float:
    base = PLAN_BASE.get(plan, 49)
    zone = ZONE_MULTIPLIERS.get(getattr(worker, "zone_risk", "Normal"), 1.0)
    season = SEASON_MULTIPLIERS.get(getattr(worker, "season", "Normal"), 1.0)
    history = 0.95 if getattr(worker, "claims_count", 0) == 0 else 1.0
    premium = round(base * zone * history * season, 2)
    return premium


def get_premium_breakdown(worker, plan: str) -> dict:
    base = PLAN_BASE.get(plan, 49)
    zone = ZONE_MULTIPLIERS.get(getattr(worker, "zone_risk", "Normal"), 1.0)
    season = SEASON_MULTIPLIERS.get(getattr(worker, "season", "Normal"), 1.0)
    history = 0.95 if getattr(worker, "claims_count", 0) == 0 else 1.0
    premium = round(base * zone * history * season, 2)
    return {
        "base": base,
        "zone_multiplier": zone,
        "history_multiplier": history,
        "season_multiplier": season,
        "final_premium": premium,
        "formula": f"₹{base} × {zone} × {history} × {season} = ₹{premium}/week",
    }
