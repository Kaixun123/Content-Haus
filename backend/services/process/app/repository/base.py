import logging
from abc import ABC

from app.database import DatabaseConnector


class BaseRepository(ABC):
    def __init__(self, model):
        self.model = model
        self.db_connector = DatabaseConnector()

    def is_correct_model(self, used_model):
        logging.debug(f"Used model: {used_model}, expected model: {type(self.model)}")
        return isinstance(used_model, type(self.model))
