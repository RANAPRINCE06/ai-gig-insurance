from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, user, policy, claim, admin
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GigShield API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(user.router, prefix="/api/users", tags=["Users"])
app.include_router(policy.router, prefix="/api/policies", tags=["Policies"])
app.include_router(claim.router, prefix="/api/claims", tags=["Claims"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
def root():
    return {"message": "GigShield API is running", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "ok"}
