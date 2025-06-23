from fastapi import APIRouter, Depends
from app.token import get_current_user
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/tenants", tags=["Tenants"])

@router.get("/")
def list_tenants(current_user: dict = Depends(get_current_user)):
    return {
        "message": "List of tenants",
        "accessed_by_user_id": current_user["user_id"],
        "role": current_user["role"],
    }

@router.post("/", response_model=schemas.Tenant)
def create_tenant(tenant: schemas.TenantCreate, db: Session = Depends(get_db)):
    db_tenant = models.Tenant(name=tenant.name, description=tenant.description)
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant