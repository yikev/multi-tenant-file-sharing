# routes/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.routes.auth import get_current_user
from app import models, schemas

router = APIRouter()

@router.get("/", response_model=schemas.DashboardResponse)
def get_dashboard(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    tenant_id = current_user["tenant_id"]
    user_id = current_user["user_id"]

    total_files = db.query(models.File).filter_by(tenant_id=tenant_id).count()
    total_storage = db.query(func.sum(models.File.filesize_kb)).filter_by(tenant_id=tenant_id).scalar() or 0
    total_users = db.query(models.User).filter_by(tenant_id=tenant_id).count()
    tenant_name = db.query(models.Tenant.name).filter_by(id=tenant_id).scalar()
    user = db.query(models.User).filter_by(id=user_id).first()
    user_name = user.email if user else "Unknown"

    recent_files = db.query(models.File)\
        .filter_by(tenant_id=tenant_id)\
        .order_by(models.File.date_uploaded.desc())\
        .limit(5).all()

    recent_projects = db.query(models.Project)\
        .filter_by(tenant_id=tenant_id)\
        .order_by(models.Project.last_updated.desc())\
        .limit(5).all()

    return {
        "total_files": total_files,
        "total_storage_kb": total_storage,
        "total_users": total_users,
        "tenant_name": tenant_name,
        "user_name": user_name,
        "recent_files": recent_files,
        "recent_projects": recent_projects
    }