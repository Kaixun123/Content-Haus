import logging

from app.models.prompt_model import PromptResponse
from app.repository.prompts import PromptRepository


# TODO: Create base class
class PromptService:
    def __init__(self):
        self.repository = PromptRepository()

    async def create(self, obj: dict):
        prompt_response = PromptResponse(**obj)

        logging.debug(f"Creating prompt response: {prompt_response}")
        await self.repository.create(prompt_response)

    async def fetch(self, key: str):
        return await self.repository.fetch(key)
