from typing import List, Literal
from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api import default
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/v1/roles",
    tags=["roles"],
    responses={404: {"description": "Not found"}}
)


# /roles

@router.get("/", summary="Получить все роли, доступные на портале")
async def get_roles(
    db: AsyncSession = Depends(get_db)
) -> schemas.API_UserRoleList:
    """
    Получить все роли, доступные на портале
    """
    role_dict = await db.execute(select(models.UserRole))
    role_dict_result = role_dict.scalars().all()

    if not role_dict_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )

    return {"roles": role_dict_result}

# /role

@router.get("/{role_id}", summary="Получить информацию о роли")
async def get_role(
    role_id: int,
    db: AsyncSession = Depends(get_db)
) -> schemas.UserRoleSchema:
    """
    Получить информацию о роли
    """
    role_dict = await db.execute(select(models.UserRole).where(models.UserRole.iid == role_id))
    role_dict_result = role_dict.scalar_one_or_none()

    if not role_dict_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Роль с id == {role_id} не существует"
        )

    return role_dict_result

@router.get("/roleByUserID/{user_id}", summary="Получить роль по ID пользователя")
async def roleByUserID(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> schemas.UserRoleSchema:
    """
    Возвращает детализацию о роли пользователя по его ID
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

    return role_dict_result