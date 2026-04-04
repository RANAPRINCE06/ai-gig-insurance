"""
Premium prediction ML model.
Uses a trained scikit-learn regression model.
Falls back to rule-based premium_service if model not available.
"""
import os
import pickle
import numpy as np
from app.services.premium_service import compute_premium as rule_based_premium

MODEL_PATH = os.path.join(os.path.dirname(__file__), "premium_model.pkl")
_model = None


def _load_model():
    global _model
    if _model is None and os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model


PLAN_ENCODE = {"Basic": 0, "Standard": 1, "Premium": 2}
ZONE_ENCODE = {"Low": 0, "Normal": 1, "Medium": 2, "High": 3}
SEASON_ENCODE = {"Winter": 0, "Normal": 1, "Summer": 2, "Monsoon": 3}


def predict_premium(worker, plan: str) -> float:
    """
    Returns ML-predicted weekly premium if model exists,
    otherwise falls back to rule-based calculation.
    """
    model = _load_model()
    if model is None:
        return rule_based_premium(worker, plan)

    features = np.array([[
        PLAN_ENCODE.get(plan, 1),
        ZONE_ENCODE.get(getattr(worker, "zone_risk", "Normal"), 1),
        SEASON_ENCODE.get(getattr(worker, "season", "Normal"), 1),
        min(getattr(worker, "claims_count", 0), 20),
        min(getattr(worker, "fraud_score", 0), 100),
        getattr(worker, "avg_income", 700),
    ]])

    prediction = model.predict(features)[0]
    return round(float(prediction), 2)
