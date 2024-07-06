import json
import logging

from fastapi import HTTPException
from google.oauth2.service_account import Credentials

from app.api.v1.base import RestController
from app.config import Config
from app.models.video_request import VideoRequest
from app.services.gemini_llm import GeminiLLM
from app.services.prompts import PromptService

config = Config()


class ProcessController(RestController):
    configured_prompt = """
                        Analyse this video, and come up with a storyboard for recreating this video.
                        
                        It should be engaging and appeal to users.
                        """
    svc = PromptService()

    def register_routes(self):
        @self.router.post("/process-video/")
        async def process_video(request: VideoRequest):
            try:
                # TODO: Handle singleton LLM instance
                credentials_info = json.loads(config['google.application.credentials'])
                credentials = Credentials.from_service_account_info(credentials_info)

                llm = GeminiLLM(
                    location=config['gemini.location'],
                    project=config['gemini.project.id'],
                    model_name=config['gemini.model.name'],
                    credentials=credentials
                )
                logging.debug("Attempting LLM prediction...")
                output = llm.generate_content(request.key, self.configured_prompt)
                logging.debug("Successful video process")
            except Exception as e:
                logging.error(f"Error processing video: {e}")
                raise HTTPException(status_code=500, detail=f"Error processing video: {e}")

            obj = {"key": request.key, "prompt": self.configured_prompt, "response": output}
            try:
                await self.svc.create(obj)
            except Exception as e:
                logging.error(f"Error saving prompt response: {e}")
                raise HTTPException(status_code=500, detail=f"Error saving prompt response: {e}")

            return {"message": "Video processed successfully", "output": output}
