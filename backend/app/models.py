from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text, Enum, Table, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime
from app.database import Base

class RoleEnum(str, enum.Enum):
    admin = "Admin"
    manager = "Manager"
    viewer = "Viewer"

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    users = relationship("User", back_populates="tenant")
    files = relationship("File", back_populates="tenant")
    projects = relationship("Project", back_populates="tenant")  

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    tenant = relationship("Tenant", back_populates="projects")

    files = relationship("File", back_populates="project")

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.viewer)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    tenant = relationship("Tenant", back_populates="users")

    uploads = relationship("File", back_populates="uploader")
    activities = relationship("ActivityLog", back_populates="user")

class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    filesize_kb = Column(Integer, nullable=False)
    thumbnail_path = Column(String, nullable=True)
    tags = Column(ARRAY(String))
    date_uploaded = Column(DateTime, default=datetime.utcnow)
    date_created = Column(DateTime, default=datetime.utcnow)

    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    uploader_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    tenant = relationship("Tenant", back_populates="files")
    uploader = relationship("User", back_populates="uploads")
    project = relationship("Project", back_populates="files")
    logs = relationship("ActivityLog", back_populates="file")

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action = Column(String, nullable=False)  # e.g., 'upload', 'download', 'delete'
    timestamp = Column(DateTime, default=datetime.utcnow)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"), nullable=False)

    user = relationship("User", back_populates="activities")
    file = relationship("File", back_populates="logs")