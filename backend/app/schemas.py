from pydantic import BaseModel, EmailStr, UUID4
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    tenant_id: UUID

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class FileCreate(BaseModel):
    file_name: str
    file_path: str  # or use 'file_url' if more accurate
    file_size_kb: int
    thumbnail_path: str | None = None  # Optional thumbnail

    class Config:
        orm_mode = True

class FileResponse(BaseModel):
    id: UUID4
    tenant_id: UUID4
    project_id: Optional[str] = None
    filename: str               # ✅ match SQLAlchemy model
    filepath: str               # ✅ match SQLAlchemy model
    filesize_kb: int            # ✅ match SQLAlchemy model
    thumbnail_path: Optional[str] = None
    date_uploaded: datetime
    date_created: datetime

    class Config:
        from_attributes = True  # ✅ for Pydantic v2
        # orm_mode = True       # ✅ if you're on Pydantic v1

class FileCreate(BaseModel):
    file_name: str
    file_size_kb: int
    file_path: str
    project_id: Optional[str] = None
    thumbnail_path: Optional[str] = None
    date_taken: Optional[datetime] = None
    gps_coordinates: Optional[str] = None

class TenantCreate(BaseModel):
    name: str
    description: Optional[str] = None

class Tenant(TenantCreate):
    id: UUID

    class Config:
        orm_mode = True