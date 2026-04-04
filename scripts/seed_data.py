"""
Seed the GigShield database with demo workers, policies, and claims.
Run: python scripts/seed_data.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.policy import Policy
from app.models.claim import Claim, ClaimStatus
from app.core.security import hash_password
from datetime import datetime, timedelta
import uuid

Base.metadata.create_all(bind=engine)

WORKERS = [
    {"id": "W001", "name": "Rahul Kumar",  "email": "rahul@gmail.com",   "mobile": "9876543210", "upi_id": "rahul@upi",   "platform": "Zomato",  "city": "Mumbai",    "plan": "Standard", "avg_income": 950,  "zone_risk": "High",   "season": "Monsoon", "fraud_score": 12, "claims_count": 4},
    {"id": "W002", "name": "Priya Singh",   "email": "priya@gmail.com",   "mobile": "9876543211", "upi_id": "priya@upi",   "platform": "Swiggy",  "city": "Delhi",     "plan": "Basic",    "avg_income": 780,  "zone_risk": "High",   "season": "Summer",  "fraud_score": 8,  "claims_count": 2},
    {"id": "W003", "name": "Amit Sharma",   "email": "amit@gmail.com",    "mobile": "9876543212", "upi_id": "amit@upi",    "platform": "Amazon",  "city": "Bengaluru", "plan": "Premium",  "avg_income": 1200, "zone_risk": "Normal", "season": "Normal",  "fraud_score": 5,  "claims_count": 1},
    {"id": "W004", "name": "Deepa Nair",    "email": "deepa@gmail.com",   "mobile": "9876543213", "upi_id": "deepa@upi",   "platform": "Zomato",  "city": "Mumbai",    "plan": "Standard", "avg_income": 820,  "zone_risk": "High",   "season": "Monsoon", "fraud_score": 78, "claims_count": 9, "status": "flagged"},
    {"id": "W005", "name": "Kiran Rao",     "email": "kiran@gmail.com",   "mobile": "9876543214", "upi_id": "kiran@upi",   "platform": "Blinkit", "city": "Pune",      "plan": "Basic",    "avg_income": 650,  "zone_risk": "Normal", "season": "Normal",  "fraud_score": 3,  "claims_count": 0},
    {"id": "W006", "name": "Suresh Patel",  "email": "suresh@gmail.com",  "mobile": "9876543215", "upi_id": "suresh@upi",  "platform": "Amazon",  "city": "Ahmedabad", "plan": "Standard", "avg_income": 870,  "zone_risk": "Normal", "season": "Summer",  "fraud_score": 11, "claims_count": 1},
    {"id": "W007", "name": "Ravi Yadav",    "email": "ravi@gmail.com",    "mobile": "9876543216", "upi_id": "ravi@upi",    "platform": "Swiggy",  "city": "Delhi",     "plan": "Premium",  "avg_income": 1100, "zone_risk": "High",   "season": "Summer",  "fraud_score": 22, "claims_count": 2},
    {"id": "W008", "name": "Kavitha Rao",   "email": "kavitha@gmail.com", "mobile": "9876543217", "upi_id": "kavitha@upi", "platform": "Zomato",  "city": "Kolkata",   "plan": "Basic",    "avg_income": 690,  "zone_risk": "Normal", "season": "Normal",  "fraud_score": 88, "claims_count": 11, "status": "suspended"},
]

CLAIMS_SEED = [
    {"id": "CLM-001", "worker_id": "W001", "trigger_type": "Heavy Rain",  "city": "Mumbai",    "amount": 900,  "fraud_score": 12, "gps_confirmed": True,  "auto_approved": True,  "duration": "3h 45m", "status": "paid",       "filed_at": "2026-04-01"},
    {"id": "CLM-002", "worker_id": "W001", "trigger_type": "Flood Alert", "city": "Mumbai",    "amount": 900,  "fraud_score": 15, "gps_confirmed": True,  "auto_approved": True,  "duration": "4h 10m", "status": "paid",       "filed_at": "2026-03-18"},
    {"id": "CLM-003", "worker_id": "W001", "trigger_type": "Heavy Rain",  "city": "Mumbai",    "amount": 900,  "fraud_score": 18, "gps_confirmed": True,  "auto_approved": True,  "duration": "3h 20m", "status": "paid",       "filed_at": "2026-03-08"},
    {"id": "CLM-004", "worker_id": "W001", "trigger_type": "AQI Spike",   "city": "Mumbai",    "amount": 900,  "fraud_score": 11, "gps_confirmed": True,  "auto_approved": True,  "duration": "2h 55m", "status": "processing", "filed_at": "2026-04-04"},
    {"id": "CLM-005", "worker_id": "W002", "trigger_type": "AQI Spike",   "city": "Delhi",     "amount": 450,  "fraud_score": 8,  "gps_confirmed": True,  "auto_approved": True,  "duration": "5h 00m", "status": "paid",       "filed_at": "2026-03-25"},
    {"id": "CLM-006", "worker_id": "W002", "trigger_type": "Heat Alert",  "city": "Delhi",     "amount": 450,  "fraud_score": 19, "gps_confirmed": True,  "auto_approved": True,  "duration": "6h 30m", "status": "paid",       "filed_at": "2026-03-12"},
    {"id": "CLM-007", "worker_id": "W003", "trigger_type": "Heavy Rain",  "city": "Bengaluru", "amount": 1500, "fraud_score": 5,  "gps_confirmed": True,  "auto_approved": True,  "duration": "3h 15m", "status": "paid",       "filed_at": "2026-03-20"},
    {"id": "CLM-008", "worker_id": "W004", "trigger_type": "Heavy Rain",  "city": "Mumbai",    "amount": 900,  "fraud_score": 78, "gps_confirmed": False, "auto_approved": False, "duration": "4h 00m", "status": "flagged",    "filed_at": "2026-04-02"},
    {"id": "CLM-009", "worker_id": "W004", "trigger_type": "Flood Alert", "city": "Mumbai",    "amount": 900,  "fraud_score": 82, "gps_confirmed": False, "auto_approved": False, "duration": "3h 50m", "status": "flagged",    "filed_at": "2026-03-28"},
    {"id": "CLM-010", "worker_id": "W007", "trigger_type": "AQI Spike",   "city": "Delhi",     "amount": 1500, "fraud_score": 22, "gps_confirmed": True,  "auto_approved": False, "duration": "4h 20m", "status": "pending",    "filed_at": "2026-04-03"},
    {"id": "CLM-011", "worker_id": "W008", "trigger_type": "Heavy Rain",  "city": "Kolkata",   "amount": 450,  "fraud_score": 88, "gps_confirmed": False, "auto_approved": False, "duration": "3h 30m", "status": "flagged",    "filed_at": "2026-04-01"},
]

PLAN_PREMIUMS = {"Basic": 29, "Standard": 49, "Premium": 79}
PLAN_PAYOUTS  = {"Basic": 450, "Standard": 900, "Premium": 1500}

def seed():
    db = SessionLocal()
    try:
        # Admin user
        if not db.query(User).filter(User.id == "ADMIN").first():
            admin = User(
                id="ADMIN", name="Arjun Mehta", email="admin@gigshield.com",
                hashed_password=hash_password("admin123"),
                mobile="9000000000", platform="GigShield", city="Mumbai",
                plan="Premium", initials="AM", is_admin=True,
            )
            db.add(admin)

        # Workers
        for w in WORKERS:
            if db.query(User).filter(User.id == w["id"]).first():
                continue
            initials = "".join(p[0].upper() for p in w["name"].split()[:2])
            user = User(
                id=w["id"], name=w["name"], email=w["email"],
                hashed_password=hash_password("password123"),
                mobile=w["mobile"], upi_id=w["upi_id"],
                platform=w["platform"], city=w["city"], plan=w["plan"],
                avg_income=w["avg_income"], zone_risk=w["zone_risk"],
                season=w["season"], fraud_score=w["fraud_score"],
                claims_count=w["claims_count"],
                status=w.get("status", "active"), initials=initials,
            )
            db.add(user)

            policy = Policy(
                id=f"POL-{w['id']}",
                worker_id=w["id"],
                plan=w["plan"],
                premium_weekly=PLAN_PREMIUMS[w["plan"]],
                payout_amount=PLAN_PAYOUTS[w["plan"]],
                city=w["city"],
                end_date=datetime.utcnow() + timedelta(days=365),
            )
            db.add(policy)

        db.commit()

        # Claims
        for c in CLAIMS_SEED:
            if db.query(Claim).filter(Claim.id == c["id"]).first():
                continue
            claim = Claim(
                id=c["id"],
                worker_id=c["worker_id"],
                policy_id=f"POL-{c['worker_id']}",
                trigger_type=c["trigger_type"],
                city=c["city"],
                amount=c["amount"],
                fraud_score=c["fraud_score"],
                gps_confirmed=c["gps_confirmed"],
                auto_approved=c["auto_approved"],
                duration=c["duration"],
                status=c["status"],
                filed_at=datetime.strptime(c["filed_at"], "%Y-%m-%d"),
                paid_at=datetime.strptime(c["filed_at"], "%Y-%m-%d") if c["status"] == "paid" else None,
                razorpay_tx_id=f"RZP{uuid.uuid4().hex[:9].upper()}" if c["status"] == "paid" else None,
            )
            db.add(claim)

        db.commit()
        print("✅ Database seeded successfully!")
        print(f"   Workers: {len(WORKERS) + 1} (incl. admin)")
        print(f"   Policies: {len(WORKERS)}")
        print(f"   Claims: {len(CLAIMS_SEED)}")
        print("\n🔑 Login credentials:")
        print("   Admin:  admin@gigshield.com / admin123")
        print("   Worker: rahul@gmail.com / password123")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
