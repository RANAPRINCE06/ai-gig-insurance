from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class PolicyStatus(str, Enum):
    active = "active"
    expired = "expired"
    cancelled = "cancelled"

PLAN_PREMIUMS = {"Basic": 29, "Standard": 49, "Premium": 79}
PLAN_PAYOUTS  = {"Basic": 450, "Standard": 900, "Premium": 1500}

class PolicyCreate(BaseModel):
    worker_id: str
    plan: str
    city: str

class PolicyOut(BaseModel):
    id: str
    worker_id: str
    plan: str
    premium_weekly: float
    payout_amount: float
    start_date: datetime
    end_date: Optional[datetime]
    status: PolicyStatus
    city: str

    class Config:
        from_attributes = True
