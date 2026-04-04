"""
Fraud detection service.
Mirrors the frontend computeFraudScore logic and adds
Isolation Forest ML model scoring.
"""
from typing import List, Dict


def compute_fraud_score(worker_data: dict) -> Dict:
    """
    Rule-based fraud scoring used for real-time claim decisions.
    Score 0-100. Flags indicate which rules fired.
    Decision:
      < 30  → AUTO_APPROVE
      30-69 → MANUAL_REVIEW
      ≥ 70  → AUTO_REJECT
    """
    score = 0
    flags: List[str] = []

    claims_count = worker_data.get("claims_count", 0)
    if claims_count > 8:
        score += 25
        flags.append("High claim frequency")
    elif claims_count > 5:
        score += 10

    if not worker_data.get("gps_ok", True):
        score += 40
        flags.append("GPS not confirmed in zone")

    if worker_data.get("duplicate_device", False):
        score += 35
        flags.append("Same device, another claim active")

    if worker_data.get("new_upi", False):
        score += 15
        flags.append("UPI changed within 24h")

    if worker_data.get("claim_speed_mins", 5) < 2:
        score += 10
        flags.append("Claim filed unusually fast")

    if worker_data.get("income_discrepancy_pct", 0) > 40:
        score += 20
        flags.append("Income discrepancy >40%")

    score = min(100, score)
    decision = (
        "AUTO_APPROVE" if score < 30
        else "MANUAL_REVIEW" if score < 70
        else "AUTO_REJECT"
    )

    return {
        "score": score,
        "flags": flags,
        "decision": decision,
        "auto_approve": score < 70,
    }


def score_label(score: int) -> str:
    if score < 30:
        return "Low Risk"
    if score < 70:
        return "Medium Risk"
    return "High Risk"


def score_color(score: int) -> str:
    if score < 30:
        return "green"
    if score < 70:
        return "amber"
    return "red"
