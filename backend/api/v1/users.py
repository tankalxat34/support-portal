from fastapi import APIRouter

from api import default

router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def read_users():
    return default.reponse([{"username": "alice"}, {"username": "bob"}])

@router.get("/{user_id}")
async def read_user(user_id: int):
    return default.reponse({"user_id": user_id})