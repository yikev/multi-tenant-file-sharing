from fastapi import APIRouter, Depends
from app.token import get_current_user

router = APIRouter(prefix="/tenants", tags=["Tenants"])

@router.get("/")
def list_tenants(current_user: dict = Depends(get_current_user)):
    return {
        "message": "List of tenants",
        "accessed_by_user_id": current_user["user_id"],
        "role": current_user["role"],
    }