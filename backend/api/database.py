from dotenv import load_dotenv
import sys
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

load_dotenv()

DOTENV_DB_HOST=os.getenv("DB_HOST")
DOTENV_DB_PORT=os.getenv("DB_PORT")
DOTENV_DB_USER=os.getenv("DB_USER")
DOTENV_DB_PASSWORD=os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql+asyncpg://{DOTENV_DB_USER}:{DOTENV_DB_PASSWORD}@{DOTENV_DB_HOST}/DB_SupportPortal"
# Для теста: DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# Зависимость для получения сессии БД
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session