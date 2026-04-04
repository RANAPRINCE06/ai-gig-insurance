from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ClaimStatus(str, Enum):
    processing = "processing"
    pending = "pending"
    paid = "paid"
    flagged = "flagged"
    rejected = "rejected"

class ClaimCreate(BaseModel):
    worker_id: str
    policy_id: Optional[str]
    trigger_type: str
    city: str
    gps_confirmed: bool = True
    duration: Optional[str]

class ClaimDecision(BaseModel):
    claim_id: str
    action: str  # approve | reject
    reason: Optional[str]

class ClaimOut(BaseModel):
    id: str
    worker_id: str
    policy_id: Optional[str]
    trigger_type: str
    city: str
    amount: float
    fraud_score: int
    gps_confirmed: bool
    auto_approved: bool
    duration: Optional[str]
    status: ClaimStatus
    filed_at: datetime
    paid_at: Optional[datetime]
    razorpay_tx_id: Optional[str]
    fraud_flags: Optional[str]

    class Config:
        from_attributes = True

class FraudResult(BaseModel):
    score: int
    flags: List[str]
    decision: str  # AUTO_APPROVE | MANUAL_REVIEW | AUTO_REJECT
    auto_approve: bool
