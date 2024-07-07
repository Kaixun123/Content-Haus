import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

@asynccontextmanager
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session      