import json
import logging

from fastapi import HTTPException
from google.oauth2.service_account import Credentials

from app.utils import Utils
from app.config import Config
from app.api.v1.base import RestController
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
                # Check if the key exists in the database
                gs_filepath = Utils.ensure_gcs_path(request.key)
                existing_record = await self.svc.fetch(gs_filepath)
                if existing_record:
                    logging.info("Video already exists, retrieving result from database");
                    return {"message": "Video processed", "data": existing_record['response']}
                
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
                output = llm.generate_content(gs_filepath, self.configured_prompt)
                logging.debug("Successful video process")
            except Exception as e:
                logging.error(f"Error processing video: {e}")
                raise HTTPException(status_code=500, detail=f"Error processing video: {e}")

            obj = {"key": gs_filepath, "prompt": self.configured_prompt, "response": output}
            try:
                await self.svc.create(obj)
            except Exception as e:
                logging.error(f"Error saving prompt response: {e}")
                raise HTTPException(status_code=500, detail=f"Error saving prompt response: {e}")

            return {"message": "Video processed successfully", "output": output}
