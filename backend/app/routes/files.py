from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import File
from app.token import get_current_user
from app import models, schemas
from app import config
import shutil
from app.schemas import FileResponse
import os
from app.cloudinary_utils import upload_to_cloudinary

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=list[schemas.FileResponse])
def get_files(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    files = db.query(models.File).filter(models.File.tenant_id == current_user["tenant_id"]).all()
    return [FileResponse.model_validate(f) for f in files]  # Pydantic v2

@router.post("/upload")
def upload_file(
    uploaded_file: UploadFile = FastAPIFile(...),
    project_id: str = Form(...),
    file_size_kb: int = 0,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tenant_id = current_user["tenant_id"]
    # project_id = current_user.get("active_project_id", "default")  # 👈 Customize if needed

    # Use the Cloudinary utility
    cloudinary_url, public_id = upload_to_cloudinary(uploaded_file, tenant_id, project_id)

    # Fallbacks
    original_filename = uploaded_file.filename
    size_in_kb = file_size_kb or (uploaded_file.size // 1024 if hasattr(uploaded_file, "size") else 0)

    # Save metadata in DB
    new_file = models.File(
        filename=original_filename,
        filepath=cloudinary_url,
        filesize_kb=size_in_kb,
        thumbnail_path="",  # You can generate one via Cloudinary transformations if needed
        tenant_id=tenant_id,
        project_id=project_id,
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "filename": original_filename,
        "url": cloudinary_url,
        "message": "Upload successful"
    }