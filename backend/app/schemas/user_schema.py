from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class UserStatus(str, Enum):
    active = "active"
    suspended = "suspended"
    flagged = "flagged"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    mobile: str
    upi_id: Optional[str] = None
    platform: str
    city: str
    plan: str = "Basic"
    avg_income: float = 700

class UserUpdate(BaseModel):
    name: Optional[str]
    mobile: Optional[str]
    upi_id: Optional[str]
    platform: Optional[str]
    city: Optional[str]
    plan: Optional[str]
    avg_income: Optional[float]
    status: Optional[UserStatus]

class UserOut(BaseModel):
    id: str
    name: str
    email: str
    mobile: str
    upi_id: Optional[str]
    platform: str
    city: str
    plan: str
    avg_income: float
    claims_count: int
    fraud_score: float
    zone_risk: str
    season: str
    status: UserStatus
    initials: Optional[str]

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
