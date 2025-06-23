from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import File
from app.token import get_current_user
from app import models, schemas
from app import config
import shutil
from app.schemas import FileResponse
import os
import cloudinary.uploader

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
    file_size_kb: int = 0,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Upload directly to Cloudinary
    result = cloudinary.uploader.upload(uploaded_file.file, resource_type="auto")

    # Extract useful fields
    cloudinary_url = result["secure_url"]
    public_id = result["public_id"]
    original_filename = result["original_filename"]
    size_in_kb = result.get("bytes", 0) // 1024

    # Create DB entry
    new_file = models.File(
        filename=original_filename,
        filepath=cloudinary_url,  # ✅ now Cloudinary URL
        filesize_kb=size_in_kb,
        thumbnail_path=result.get("thumbnail_url", ""),  # optional
        tenant_id=current_user["tenant_id"],
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "filename": original_filename,
        "url": cloudinary_url,
        "message": "Upload successful"
    }