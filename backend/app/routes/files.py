from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import File
from app.token import get_current_user
from app import models, schemas
import shutil
import os

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=list[schemas.FileResponse])
def get_files(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    files = db.query(models.File).filter(models.File.tenant_id == current_user["tenant_id"]).all()
    return files

@router.post("/upload")
def upload_file(
    uploaded_file: UploadFile = FastAPIFile(...),
    file_size_kb: int = 0,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    filename = uploaded_file.filename
    filepath = os.path.join(UPLOAD_DIR, filename)

    # Save file
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    # Create DB entry
    new_file = models.File(
        filename=filename,
        filepath=filepath,
        filesize_kb=file_size_kb,
        thumbnail_path="",  # Update later if needed
        tenant_id=current_user["tenant_id"]
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {"filename": filename, "message": "Upload successful"}