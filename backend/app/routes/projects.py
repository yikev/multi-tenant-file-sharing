from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, database
from app.models import Project
from app.schemas import ProjectCreate, ProjectOut
from app.token import get_current_user
from typing import List
import uuid

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(project_data: ProjectCreate,
                   db: Session = Depends(get_db),
                   current_user = Depends(get_current_user)):

    existing = db.query(Project).filter_by(
        name=project_data.name,
        tenant_id=current_user["tenant_id"]
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Project with this name already exists")

    project = Project(
        id=uuid.uuid4(),
        name=project_data.name,
        description=project_data.description,
        thumbnail_url=project_data.thumbnail_url,
        tenant_id=current_user["tenant_id"]
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project

@router.get("/", response_model=List[schemas.ProjectOut])  # or ProjectResponse
def get_projects(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tenant_id = current_user["tenant_id"]
    projects = db.query(models.Project).filter(models.Project.tenant_id == tenant_id).all()
    return projects  

@router.get("/{project_name}", response_model=schemas.ProjectOut)
def get_project_by_name(
    project_name: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    project = (
        db.query(models.Project)
        .filter(models.Project.name == project_name)
        .filter(models.Project.tenant_id == current_user["tenant_id"])
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project