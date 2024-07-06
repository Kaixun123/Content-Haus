from app.models.prompt_model import PromptResponse
from app.repository.base import BaseRepository


class PromptRepository(BaseRepository):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(PromptRepository, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'model'):
            super().__init__(PromptResponse())

    async def create(self, obj: PromptResponse):
        if not self.is_correct_model(obj):
            raise ValueError(f"Invalid model type: expected PromptResponse, got {type(obj)}")

        query = self.db_connector.table.insert()
        obj_dict = {k: v for k, v in obj.__dict__.items() if k != '_sa_instance_state'}
        await self.db_connector.database.execute(query=query, values=obj_dict)

    def fetch(self, key: str):
        query = self.db_connector.table.select().where(self.db_connector.table.c.key == key)
        return self.db_connector.database.fetch_one(query)
