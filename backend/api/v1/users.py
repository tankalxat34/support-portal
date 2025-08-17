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


@router.get("/{user_id}", response_model=schemas.PortalUserSchema)
async def get_users(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.PortalUser).where(models.PortalUser.iid == user_id))
    user = result.scalar().first()
    return user