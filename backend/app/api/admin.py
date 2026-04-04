from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.claim import Claim, ClaimStatus
from app.models.policy import Policy
from app.core.dependencies import get_current_user
from app.schemas.user_schema import UserOut
from typing import List

router = APIRouter()

def require_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    workers = db.query(User).filter(User.is_admin == False).all()
    claims = db.query(Claim).all()
    paid_claims = [c for c in claims if c.status == ClaimStatus.paid]
    total_payouts = sum(c.amount for c in paid_claims)
    flagged = [c for c in claims if c.fraud_score >= 70 or c.status == ClaimStatus.flagged]
    active_policies = db.query(Policy).filter(Policy.status == "active").count()
    weekly_rev = sum(({"Basic": 29, "Standard": 49, "Premium": 79}.get(w.plan, 49)) for w in workers)
    loss_ratio = round((total_payouts / weekly_rev) * 100, 1) if weekly_rev else 0
    auto_rate = round((len([c for c in claims if c.auto_approved]) / len(claims)) * 100) if claims else 0

    return {
        "total_workers": len(workers),
        "active_policies": active_policies,
        "total_payouts_mtd": total_payouts,
        "flagged_claims": len(flagged),
        "weekly_revenue": weekly_rev,
        "loss_ratio": loss_ratio,
        "total_claims_mtd": len(claims),
        "auto_approve_rate": auto_rate,
    }

@router.get("/workers", response_model=List[UserOut])
def all_workers(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(User).filter(User.is_admin == False).all()

@router.patch("/workers/{worker_id}/suspend")
def suspend_worker(worker_id: str, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    worker = db.query(User).filter(User.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    worker.status = "suspended"
    db.commit()
    return {"message": f"Worker {worker_id} suspended"}

@router.get("/stats/loss-ratio")
def loss_ratio_trend(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    # Returns weekly loss ratio data for chart
    claims = db.query(Claim).all()
    paid = sum(c.amount for c in claims if c.status == ClaimStatus.paid)
    return {"loss_ratio": round(paid / 392 * 100, 1) if paid else 68.4}
