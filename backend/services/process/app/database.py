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
        self.table = Table(self.table_name, metadata, autoload_with=self.engine)

        if not self.engine.dialect.has_table(self.engine, self.table_name):
            Base.metadata.create_all(bind=engine)
    
    async def start_database(self):
        logging.info("Attempting to connect to database...")
        try:
            await database.connect()
            logging.info("Database connection successful")
        except Exception as e:
            logging.info("Failed to connect to the database")
        
    
    async def disconnect_database(self):
        await database.disconnect()