from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, tenants, files
from app.models import Base
from app.database import engine

# Create FastAPI app
app = FastAPI(title="Multi-Tenant File Sharing Platform API", version="1.0.0")

# Create all DB tables
Base.metadata.create_all(bind=engine)

# CORS Middleware (optional, but helpful for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",                        # local dev
        "http://127.0.0.1:5173",                        # alternate local dev
        "https://yikev.github.io",                      # GitHub Pages
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
app.include_router(files.router, prefix="/files", tags=["files"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Multi-Tenant File Sharing Platform API"}

@app.get("/debug-tables")
def debug_tables():
    from app.models import Tenant, User, File
    return {
        "tenants": Tenant.__table__.name,
        "users": User.__table__.name,
        "files": File.__table__.name,
    }

