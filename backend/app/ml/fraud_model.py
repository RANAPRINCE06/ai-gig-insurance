"""
Fraud detection ML model — Isolation Forest.
Detects statistical outliers in claim patterns.
Falls back to rule-based fraud_service if model not trained.
"""
import os
import pickle
import numpy as np
from app.services.fraud_service import compute_fraud_score as rule_based_score

MODEL_PATH = os.path.join(os.path.dirname(__file__), "fraud_model.pkl")
_model = None


def _load_model():
    global _model
    if _model is None and os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
    return _model


def predict_fraud_score(worker_data: dict) -> dict:
    """
    Returns fraud assessment dict.
    Uses Isolation Forest anomaly score if model loaded,
    otherwise falls back to rule-based scoring.
    """
    model = _load_model()

    # Always run rule-based for flags
    rule_result = rule_based_score(worker_data)

    if model is None:
        return rule_result

    features = np.array([[
        worker_data.get("claims_count", 0),
        0 if worker_data.get("gps_ok", True) else 1,
        1 if worker_data.get("duplicate_device", False) else 0,
        1 if worker_data.get("new_upi", False) else 0,
        worker_data.get("claim_speed_mins", 5),
        worker_data.get("income_discrepancy_pct", 0),
    ]])

    # Isolation Forest: -1 = anomaly, 1 = normal
    anomaly = model.predict(features)[0]
    anomaly_score = model.score_samples(features)[0]  # lower = more anomalous

    # Blend ML signal with rule score
    ml_boost = 30 if anomaly == -1 else 0
    final_score = min(100, rule_result["score"] + ml_boost)

    decision = (
        "AUTO_APPROVE" if final_score < 30
        else "MANUAL_REVIEW" if final_score < 70
        else "AUTO_REJECT"
    )

    return {
        "score": final_score,
        "flags": rule_result["flags"],
        "decision": decision,
        "auto_approve": final_score < 70,
        "ml_anomaly": anomaly == -1,
        "isolation_score": round(anomaly_score, 4),
    }
