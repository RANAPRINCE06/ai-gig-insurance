from sqlalchemy import Column, String, Integer, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class UserStatus(str, enum.Enum):
    active = "active"
    suspended = "suspended"
    flagged = "flagged"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # e.g. W001
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    upi_id = Column(String)
    platform = Column(String)  # Zomato, Swiggy, Amazon, Blinkit
    city = Column(String)
    plan = Column(String, default="Basic")  # Basic, Standard, Premium
    avg_income = Column(Float, default=700)
    claims_count = Column(Integer, default=0)
    fraud_score = Column(Float, default=0)
    zone_risk = Column(String, default="Normal")
    season = Column(String, default="Normal")
    status = Column(Enum(UserStatus), default=UserStatus.active)
    is_admin = Column(Boolean, default=False)
    initials = Column(String)

    policies = relationship("Policy", back_populates="worker")
    claims = relationship("Claim", back_populates="worker")
