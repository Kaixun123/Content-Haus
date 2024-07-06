from app.models.prompt_model import PromptResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, MetaData
from app.config import Config
from databases import Database
import logging

config = Config()
MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB = config['mysql.user'], config['mysql.password'], config['mysql.host'], config['mysql.db']
Base = declarative_base()

class DatabaseConnector:
    def __init__(self):
        self.databaseURL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
        self.base = Base
        self.engine = create_async_engine(self.databaseURL, echo=True)
        self.AsyncSessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=AsyncSession
        )
        self.table_name = PromptResponse.__tablename__

        metadata = MetaData()
        self.table = Table(self.table_name, metadata)
        self.database = Database(self.databaseURL)

    async def _check_and_create_table(self):
        async with self.engine.begin() as connection:
            # Check if table exists
            result = await connection.run_sync(lambda conn: self.engine.dialect.has_table(conn, self.table_name))
            if not result:
                logging.info(f"Creating table {self.table_name}")
                await connection.run_sync(self.base.metadata.create_all)
            else:
                logging.info(f"Table {self.table_name} already exists")

    async def start_database(self):
        logging.info("Attempting to connect to the database...")
        try:
            await self.database.connect()
            await self._check_and_create_table()
            logging.info("Database connection successful")
        except Exception as e:
            logging.error(f"Failed to connect to the database: {e}")

    async def disconnect_database(self):
        logging.info("Attempting to disconnect from the database...")
        try:
            await self.database.disconnect()
            logging.info("Database disconnection successful")
        except Exception as e:
            logging.error(f"Failed to disconnect from the database: {e}")
