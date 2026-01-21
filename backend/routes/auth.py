from fastapi import APIRouter

router = APIRouter()


@router.get("/me")
async def get_user():
    # For testing purposes, return a mock user
    return {"id": 1, "email": "test@example.com", "name": "Test User"}