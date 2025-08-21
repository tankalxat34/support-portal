from typing import List, Literal
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

# main node

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
    return users

# /user

@router.get("/{user_id}", summary="Получить пользователя по ID")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> schemas.PortalUserSchema:
    """
    Возвращает пользователя по его `iid`.
    """

    result = await db.execute(select(models.PortalUser).where(models.PortalUser.iid == user_id))
    user = result.scalar_one_or_none()

    role_dict = await db.execute(select(models.UserRole).where(models.UserRole.iid == user.portal_role))
    role_dict_result = role_dict.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с ID={user_id} не найден"
        )

    # user["role"] = role_dict_result

    return user

@router.get("/{user_id}/appeals", summary="Получить все обращения пользователя на портале")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> schemas.API_AppealSchema:
    """
    Получить все обращения пользователя на портале
    """
    result = await db.execute(select(models.Appeal).where(models.Appeal.iid_user == user_id))
    appeals = result.scalars().all()

    print(appeals)

    if not appeals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Нет обращений"
        )

    return {
        "appeals": appeals
    }

@router.get("/{user_id}/workgroups", summary="Рабочие группы, в которых состоит пользователь")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
# ) -> List[int]:
) -> schemas.API_UserWorkgroups:
    """
    Рабочие группы, в которых состоит пользователь
    """
    result = await db.execute(select(models.user_to_workgroup).where(models.user_to_workgroup.columns.get("iid_user") == user_id))
    r = result.scalars().all()

    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь не состоит в рабочих группах"
        )

    return {
            "workgroups": r
        }
