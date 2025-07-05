from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, Form, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import File
from uuid import UUID
from app.token import get_current_user
from app import models, schemas
from app import config
import json
import shutil
from app.schemas import FileResponse
import os
from app.cloudinary_utils import upload_to_cloudinary
from app.cloudinary_utils import delete_from_cloudinary 

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=list[schemas.FileResponse])
def get_files(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    files = db.query(models.File).filter(models.File.tenant_id == current_user["tenant_id"]).all()
    return [FileResponse.model_validate(f) for f in files]  # Pydantic v2

from typing import Optional
import json

from typing import Optional
from fastapi import Form
import json

@router.post("/upload")
def upload_file(
    uploaded_file: UploadFile = FastAPIFile(...),
    project_id: str = Form(...),
    tags: str = Form(None),  # 👈 still comes in as a string
    file_size_kb: int = 0,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tenant_id = current_user["tenant_id"]

    # 👇 Parse tags string as JSON if provided
    try:
        tag_list = json.loads(tags) if tags else []
        if not isinstance(tag_list, list) or not all(isinstance(tag, str) for tag in tag_list):
            raise ValueError
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid format for tags. Provide a JSON array of strings.")

    # Upload to Cloudinary
    cloudinary_url, public_id = upload_to_cloudinary(uploaded_file, tenant_id, project_id)

    # Save metadata
    new_file = models.File(
        filename=uploaded_file.filename,
        filepath=cloudinary_url,
        filesize_kb=file_size_kb,
        thumbnail_path="",
        tenant_id=tenant_id,
        project_id=project_id,
        tags=tag_list,  # 👈 Save as list of strings
        public_id=public_id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    project = db.query(models.Project).filter_by(id=project_id, tenant_id=tenant_id).first()
    if not project:
        raise HTTPException(status_code=400, detail="Invalid project ID for this tenant")

    return {
        "filename": uploaded_file.filename,
        "url": cloudinary_url,
        "message": "Upload successful"
    }

@router.delete("/files/{file_id}", status_code=204)
def delete_file(
    file_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    file = db.query(File).filter(File.id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    if file.tenant_id != current_user["tenant_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if file.public_id:
        try:
            delete_from_cloudinary(file.public_id)
        except Exception as e:
            print(f"Cloudinary deletion failed: {e}")

    db.delete(file)
    db.commit()
    return None  # 204 No Content