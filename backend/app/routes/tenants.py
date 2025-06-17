from fastapi import APIRouter

router = APIRouter()

# Define your endpoints
@router.get("/")
def list_tenants():
    return {"message": "List of tenants"}