from sqlalchemy import Column, String, Float, Boolean, DateTime
from app.database import Base
from datetime import datetime

class TriggerLog(Base):
    __tablename__ = "trigger_logs"

    id = Column(String, primary_key=True, index=True)
    city = Column(String, nullable=False)
    trigger_type = Column(String, nullable=False)  # rain, aqi, heat, flood
    current_value = Column(Float)
    threshold_value = Column(Float)
    triggered = Column(Boolean, default=False)
    status = Column(String, default="NORMAL")  # ACTIVE, WATCHING, NORMAL
    source = Column(String)
    logged_at = Column(DateTime, default=datetime.utcnow)
