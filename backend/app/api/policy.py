from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.policy import Policy
from app.models.user import User
from app.schemas.policy_schema import PolicyCreate, PolicyOut, PLAN_PREMIUMS, PLAN_PAYOUTS
from app.core.dependencies import get_current_user
from app.services.premium_service import compute_premium
from typing import List
from datetime import datetime, timedelta
import uuid

router = APIRouter()

@router.post("/", response_model=PolicyOut, status_code=201)
def create_policy(payload: PolicyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    worker = db.query(User).filter(User.id == payload.worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    premium = compute_premium(worker, payload.plan)
    payout = PLAN_PAYOUTS.get(payload.plan, 450)

    policy = Policy(
        id=f"POL-{uuid.uuid4().hex[:8].upper()}",
        worker_id=payload.worker_id,
        plan=payload.plan,
        premium_weekly=premium,
        payout_amount=payout,
        city=payload.city,
        end_date=datetime.utcnow() + timedelta(days=365),
    )
    db.add(policy)
    worker.plan = payload.plan
    db.commit()
    db.refresh(policy)
    return policy

@router.get("/", response_model=List[PolicyOut])
def list_policies(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        return db.query(Policy).all()
    return db.query(Policy).filter(Policy.worker_id == current_user.id).all()

@router.get("/{policy_id}", response_model=PolicyOut)
def get_policy(policy_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy
