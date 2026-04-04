from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserOut, TokenResponse
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
import uuid

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    count = db.query(User).count()
    worker_id = f"W{str(count + 1).zfill(3)}"
    initials = "".join(p[0].upper() for p in payload.name.split()[:2])

    user = User(
        id=worker_id,
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        mobile=payload.mobile,
        upi_id=payload.upi_id or f"{payload.mobile}@upi",
        platform=payload.platform,
        city=payload.city,
        plan=payload.plan,
        avg_income=payload.avg_income,
        initials=initials,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse)
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.id, "role": "admin" if user.is_admin else "worker"})
    return {"access_token": token, "token_type": "bearer", "user": user}

@router.post("/admin-login", response_model=TokenResponse)
def admin_login(username: str, password: str, db: Session = Depends(get_db)):
    if username != "admin" or password != "admin123":
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    admin = db.query(User).filter(User.is_admin == True).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin user not found")
    token = create_access_token({"sub": admin.id, "role": "admin"})
    return {"access_token": token, "token_type": "bearer", "user": admin}
