import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

from app.config import Config

config = Config()

MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB = config['mysql.user'], config['mysql.password'], config['mysql.host'], config['mysql.db']
DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Base class for declarative models
Base = declarative_base()

# Async database connection
database = Database(DATABASE_URL)
