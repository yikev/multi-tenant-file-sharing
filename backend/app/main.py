from fastapi import FastAPI
from app.routes import auth, tenants, files
from app.models import Base
from app.database import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
app.include_router(files.router, prefix="/files", tags=["files"])

@app.get("/")
def read_root():
    return {"message": "Multi-Tenant File Sharing Platform API"}