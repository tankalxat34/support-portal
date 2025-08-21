import asyncio
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api.database import AsyncSessionLocal, engine, Base
from api import schemas

from api import v1

app = FastAPI(
    title="Support Portal API",
    description="API for Support Portal"
)

# Создание таблиц при старте (для тестов)
@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(v1.users_router)
app.include_router(v1.roles_router)

@app.get("/async")
async def async_endpoint():
    # await asyncio.sleep(1)  # имитация долгой операции
    return {"message": "Done after 1 sec"}