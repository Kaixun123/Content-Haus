import logging

import vertexai
from vertexai.generative_models import GenerativeModel, Part

from app.utils import Utils
from app.config import Config
from app.services.base_llm import BaseLLM

config = Config()


class GeminiLLM(BaseLLM):
    """
    Class for the Gemini Language Learning Model (LLM).

    This class provides the necessary functionality to register the Gemini LLM
    with the specified location and project.

    Attributes:
        location (str): The location where the model is deployed or stored.
        project (str): The project name associated with the model.
        model_name (str): The name of the model.
        credentials (str): The credentials to authenticate with the model.
    """

    def register_model(self):
        """
        Registers the Gemini LLM with the specified location and project.
        """
        logging.info(
            f"Registering Gemini LLM with location: {self.location}, project: {self.project}, model_name: {self.model_name}")
        vertexai.init(project=self.project, location=self.location, credentials=self.credentials)
        self.model = GenerativeModel(self.model_name)

    def generate_content(self, video_file_uri, prompt):
        valid_gs_path = Utils.ensure_gcs_path(video_file_uri)
        logging.debug(f"Valid Google Cloud Storage path: {valid_gs_path}")
        video_file = Part.from_uri(valid_gs_path, mime_type="video/mp4")
        contents = [video_file, prompt]
        logging.debug(f"Contents to send to Gemini LLM: {contents}")
        response = self.model.generate_content(contents)
        logging.debug(f"Response from Gemini LLM: {response}")
        return response.candidates[0].content.parts[0].text
