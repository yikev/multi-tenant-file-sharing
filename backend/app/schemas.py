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
    file_name: str
    file_path: str
    file_size_kb: int
    thumbnail_path: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True

class FileCreate(BaseModel):
    file_name: str
    file_size_kb: int
    file_path: str
    thumbnail_path: Optional[str] = None
    date_taken: Optional[datetime] = None
    gps_coordinates: Optional[str] = None