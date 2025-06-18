from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database, utils, token
from app.token import get_current_user, create_access_token

router = APIRouter(tags=["Authentication"])

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
    if not user or not utils.verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(status_code=403, detail="Invalid credentials")

    access_token = token.create_access_token(
        data={"user_id": str(user.id), "tenant_id": str(user.tenant_id), "role": user.role.value}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"user_id": current_user["user_id"], "role": current_user["role"]}