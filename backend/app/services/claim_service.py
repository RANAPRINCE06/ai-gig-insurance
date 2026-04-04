"""
Claim processing business logic.
Handles the zero-touch auto-claim pipeline.
"""
from app.services.fraud_service import compute_fraud_score
from app.integrations.payment_api import initiate_upi_payout


async def process_claim(claim_data: dict, worker, policy) -> dict:
    """
    Full claim processing pipeline:
    1. Run fraud scoring
    2. Decide auto-approve or flag
    3. If auto-approve, trigger UPI payout
    Returns updated claim state.
    """
    fraud_input = {
        "claims_count": worker.claims_count,
        "gps_ok": claim_data.get("gps_confirmed", True),
        "duplicate_device": claim_data.get("duplicate_device", False),
        "new_upi": claim_data.get("new_upi", False),
        "claim_speed_mins": claim_data.get("claim_speed_mins", 5),
        "income_discrepancy_pct": claim_data.get("income_discrepancy_pct", 0),
    }

    fraud = compute_fraud_score(fraud_input)

    result = {
        "fraud_score": fraud["score"],
        "fraud_flags": fraud["flags"],
        "fraud_decision": fraud["decision"],
        "auto_approved": fraud["auto_approve"] and fraud_input["gps_ok"],
        "payout": None,
    }

    if result["auto_approved"]:
        payout = await initiate_upi_payout(
            upi_id=worker.upi_id,
            amount=policy.payout_amount,
            claim_id=claim_data.get("claim_id"),
        )
        result["payout"] = payout

    return result


def get_claim_summary(claims: list) -> dict:
    """Aggregate stats for a list of claims."""
    paid = [c for c in claims if c.status == "paid"]
    flagged = [c for c in claims if c.fraud_score >= 70 or c.status == "flagged"]
    total_paid = sum(c.amount for c in paid)
    return {
        "total": len(claims),
        "paid": len(paid),
        "flagged": len(flagged),
        "total_payout": total_paid,
        "auto_rate": round(len([c for c in claims if c.auto_approved]) / len(claims) * 100) if claims else 0,
    }
