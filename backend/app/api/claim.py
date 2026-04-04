from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.claim import Claim, ClaimStatus
from app.models.user import User
from app.models.policy import Policy
from app.schemas.claim_schema import ClaimCreate, ClaimDecision, ClaimOut
from app.core.dependencies import get_current_user
from app.services.claim_service import process_claim
from app.services.fraud_service import compute_fraud_score
from app.integrations.payment_api import initiate_upi_payout
from typing import List
from datetime import datetime
import uuid, json

router = APIRouter()

@router.post("/", response_model=ClaimOut, status_code=201)
async def file_claim(payload: ClaimCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    worker = db.query(User).filter(User.id == payload.worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    policy = db.query(Policy).filter(
        Policy.worker_id == payload.worker_id,
        Policy.status == "active"
    ).first()
    if not policy:
        raise HTTPException(status_code=400, detail="No active policy found for this worker")

    fraud_input = {
        "claims_count": worker.claims_count,
        "gps_ok": payload.gps_confirmed,
        "duplicate_device": False,
        "new_upi": False,
        "claim_speed_mins": 5,
        "income_discrepancy_pct": 0,
    }
    fraud = compute_fraud_score(fraud_input)

    claim = Claim(
        id=f"CLM-{uuid.uuid4().hex[:6].upper()}",
        worker_id=payload.worker_id,
        policy_id=policy.id,
        trigger_type=payload.trigger_type,
        city=payload.city,
        amount=policy.payout_amount,
        fraud_score=fraud["score"],
        gps_confirmed=payload.gps_confirmed,
        auto_approved=fraud["auto_approve"] and payload.gps_confirmed,
        duration=payload.duration,
        status=ClaimStatus.processing if fraud["auto_approve"] else ClaimStatus.flagged,
        fraud_flags=json.dumps(fraud["flags"]),
    )
    db.add(claim)
    worker.claims_count += 1
    db.commit()
    db.refresh(claim)

    if claim.auto_approved:
        payout = await initiate_upi_payout(worker.upi_id, claim.amount, claim.id)
        claim.status = ClaimStatus.paid
        claim.paid_at = datetime.utcnow()
        claim.razorpay_tx_id = payout.get("txId")
        db.commit()
        db.refresh(claim)

    return claim

@router.get("/", response_model=List[ClaimOut])
def list_claims(status: str = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    q = db.query(Claim)
    if not current_user.is_admin:
        q = q.filter(Claim.worker_id == current_user.id)
    if status:
        q = q.filter(Claim.status == status)
    return q.order_by(Claim.filed_at.desc()).all()

@router.post("/decide", response_model=ClaimOut)
async def decide_claim(payload: ClaimDecision, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    claim = db.query(Claim).filter(Claim.id == payload.claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    if payload.action == "approve":
        worker = db.query(User).filter(User.id == claim.worker_id).first()
        payout = await initiate_upi_payout(worker.upi_id, claim.amount, claim.id)
        claim.status = ClaimStatus.paid
        claim.paid_at = datetime.utcnow()
        claim.razorpay_tx_id = payout.get("txId")
    elif payload.action == "reject":
        claim.status = ClaimStatus.rejected
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    db.commit()
    db.refresh(claim)
    return claim

@router.get("/{claim_id}", response_model=ClaimOut)
def get_claim(claim_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim
