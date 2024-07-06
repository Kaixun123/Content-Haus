import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

from app.config import Config

config = Config()

MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB = config['mysql.user'], config['mysql.password'], config['mysql.host'], config['mysql.db']
DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

database = Database(DATABASE_URL)

