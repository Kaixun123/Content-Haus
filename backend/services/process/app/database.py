from app.repository.SQLConnector import engine, Base, database
from app.models.prompt_model import PromptResponse
from sqlalchemy import Table, MetaData
import logging

class DatabaseConnector:
    def __init__(self):
        self.base = Base
        self.engine = engine
        self.table_name = PromptResponse.__tablename__

        metadata = MetaData()
        self.table = Table(self.table_name, metadata)

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
            await database.connect()
            await self._check_and_create_table()
            logging.info("Database connection successful")
        except Exception as e:
            logging.error(f"Failed to connect to the database: {e}")

    async def disconnect_database(self):
        logging.info("Attempting to disconnect from the database...")
        try:
            await database.disconnect()
            logging.info("Database disconnection successful")
        except Exception as e:
            logging.error(f"Failed to disconnect from the database: {e}")
