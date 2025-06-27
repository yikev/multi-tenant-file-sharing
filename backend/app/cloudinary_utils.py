# backend/app/cloudinary_utils.py
import cloudinary.uploader
import os

def upload_to_cloudinary(file, tenant_id: str, project_id: str):
    filename = os.path.splitext(file.filename)[0]
    public_id = f"tenant_{tenant_id}/project_{project_id}/{filename}"

    result = cloudinary.uploader.upload(
        file.file,
        public_id=public_id,
        resource_type="auto"
    )
    return result["secure_url"], public_id