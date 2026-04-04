from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

class PolicyStatus(str, enum.Enum):
    active = "active"
    expired = "expired"
    cancelled = "cancelled"

class Policy(Base):
    __tablename__ = "policies"

    id = Column(String, primary_key=True, index=True)
    worker_id = Column(String, ForeignKey("users.id"), nullable=False)
    plan = Column(String, nullable=False)  # Basic, Standard, Premium
    premium_weekly = Column(Float, nullable=False)
    payout_amount = Column(Float, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    status = Column(Enum(PolicyStatus), default=PolicyStatus.active)
    city = Column(String)

    worker = relationship("User", back_populates="policies")
    claims = relationship("Claim", back_populates="policy")
