"""
Background Celery tasks for GigShield.
- Trigger monitoring across all cities every 5 min
- Fraud score refresh hourly
- Auto-claim generation when triggers fire
"""
import asyncio
from app.workers.celery_worker import celery_app
from app.database import SessionLocal
from app.models.user import User
from app.models.claim import Claim, ClaimStatus
from app.models.trigger import TriggerLog
from app.services.trigger_service import evaluate_triggers, any_triggered
from app.services.fraud_service import compute_fraud_score
from app.integrations.payment_api import initiate_upi_payout
from datetime import datetime
import uuid

MONITORED_CITIES = ["Mumbai", "Delhi", "Bengaluru", "Pune", "Chennai", "Kolkata", "Hyderabad", "Ahmedabad"]


@celery_app.task(name="app.workers.tasks.monitor_all_city_triggers")
def monitor_all_city_triggers():
    """
    Runs every 5 minutes. Fetches weather/AQI for all cities.
    If a trigger fires, creates auto-claims for eligible active workers in that city.
    """
    for city in MONITORED_CITIES:
        trigger_data = asyncio.get_event_loop().run_until_complete(evaluate_triggers(city))
        _log_triggers(city, trigger_data)
        if any_triggered(trigger_data):
            _generate_auto_claims(city, trigger_data)


def _log_triggers(city: str, trigger_data: dict):
    db = SessionLocal()
    try:
        for ttype in ["rain", "heat", "aqi", "flood"]:
            t = trigger_data.get(ttype, {})
            log = TriggerLog(
                id=str(uuid.uuid4()),
                city=city,
                trigger_type=ttype,
                current_value=t.get("current_mmhr") or t.get("current_c") or t.get("current") or t.get("current_m"),
                threshold_value=t.get("threshold_mmhr") or t.get("threshold_c") or t.get("threshold") or t.get("threshold_m"),
                triggered=t.get("triggered", False),
                status=t.get("status", "NORMAL"),
                source=t.get("source", ""),
            )
            db.add(log)
        db.commit()
    finally:
        db.close()


def _generate_auto_claims(city: str, trigger_data: dict):
    db = SessionLocal()
    try:
        workers = db.query(User).filter(
            User.city == city,
            User.status == "active",
            User.is_admin == False,
        ).all()

        for worker in workers:
            if not worker.policies:
                continue
            active_policy = next((p for p in worker.policies if p.status == "active"), None)
            if not active_policy:
                continue

            # Determine which trigger fired
            trigger_name = next(
                (k for k in ["rain", "heat", "aqi", "flood"]
                 if trigger_data.get(k, {}).get("triggered")), None
            )
            if not trigger_name:
                continue

            fraud_result = compute_fraud_score({
                "claims_count": worker.claims_count,
                "gps_ok": True,
                "duplicate_device": False,
                "new_upi": False,
                "claim_speed_mins": 5,
                "income_discrepancy_pct": 0,
            })

            claim = Claim(
                id=f"CLM-{uuid.uuid4().hex[:6].upper()}",
                worker_id=worker.id,
                policy_id=active_policy.id,
                trigger_type=trigger_name.upper(),
                city=city,
                amount=active_policy.payout_amount,
                fraud_score=fraud_result["score"],
                gps_confirmed=True,
                auto_approved=fraud_result["auto_approve"],
                status=ClaimStatus.processing if fraud_result["auto_approve"] else ClaimStatus.flagged,
            )
            db.add(claim)
            worker.claims_count += 1

            if fraud_result["auto_approve"]:
                payout = asyncio.get_event_loop().run_until_complete(
                    initiate_upi_payout(worker.upi_id, active_policy.payout_amount, claim.id)
                )
                claim.status = ClaimStatus.paid
                claim.paid_at = datetime.utcnow()
                claim.razorpay_tx_id = payout.get("txId")

        db.commit()
    finally:
        db.close()


@celery_app.task(name="app.workers.tasks.refresh_fraud_scores")
def refresh_fraud_scores():
    """
    Hourly task: recalculates fraud scores for all workers
    based on their latest claim history.
    """
    db = SessionLocal()
    try:
        workers = db.query(User).filter(User.is_admin == False).all()
        for worker in workers:
            fraud = compute_fraud_score({
                "claims_count": worker.claims_count,
                "gps_ok": True,
                "duplicate_device": False,
                "new_upi": False,
                "claim_speed_mins": 5,
                "income_discrepancy_pct": 0,
            })
            worker.fraud_score = fraud["score"]
        db.commit()
    finally:
        db.close()
