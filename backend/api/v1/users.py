from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api import default
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", summary="Получить список пользователей")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Возвращает список пользователей с пагинацией.
    """
    result = await db.execute(
        select(models.PortalUser).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    return {"users": users}

@router.get("/{user_id}", summary="Получить пользователя по ID")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """
    Возвращает пользователя по его `iid`.
    """
    result = await db.execute(select(models.PortalUser).where(models.PortalUser.iid == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с ID={user_id} не найден"
        )

    return {"user": user}