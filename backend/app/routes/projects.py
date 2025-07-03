from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Project
from app.schemas import ProjectCreate, ProjectOut
from app.token import get_current_user
import uuid

router = APIRouter()

@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(project_data: ProjectCreate,
                   db: Session = Depends(get_db),
                   current_user = Depends(get_current_user)):

    # Prevent duplicate project names (optional)
    existing = db.query(Project).filter_by(name=project_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Project with this name already exists")

    project = Project(
        id=uuid.uuid4(),
        name=project_data.name,
        description=project_data.description,
        thumbnail_url=project_data.thumbnail_url,
        tenant_id = current_user["tenant_id"]
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project