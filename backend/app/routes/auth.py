from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database, utils

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserCreate)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = utils.hash_password(user.password)
    new_user = models.User(email=user.email, password_hash=hashed_pw, tenant_id=user.tenant_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user

@router.post("/login")
def login(user_credentials: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    if not utils.verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(status_code=403, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": str(user.id), "tenant_id": str(user.tenant_id)}