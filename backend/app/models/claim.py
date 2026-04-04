from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

class ClaimStatus(str, enum.Enum):
    processing = "processing"
    pending = "pending"
    paid = "paid"
    flagged = "flagged"
    rejected = "rejected"

class Claim(Base):
    __tablename__ = "claims"

    id = Column(String, primary_key=True, index=True)
    worker_id = Column(String, ForeignKey("users.id"), nullable=False)
    policy_id = Column(String, ForeignKey("policies.id"), nullable=True)
    trigger_type = Column(String)  # Heavy Rain, AQI Spike, Flood, Heat Wave
    city = Column(String)
    amount = Column(Float, nullable=False)
    fraud_score = Column(Integer, default=0)
    gps_confirmed = Column(Boolean, default=True)
    auto_approved = Column(Boolean, default=False)
    duration = Column(String)  # e.g. "3h 45m"
    status = Column(Enum(ClaimStatus), default=ClaimStatus.processing)
    filed_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
    razorpay_tx_id = Column(String, nullable=True)
    fraud_flags = Column(String, nullable=True)  # JSON string of flags

    worker = relationship("User", back_populates="claims")
    policy = relationship("Policy", back_populates="claims")
