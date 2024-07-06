import logging

import vertexai
from services.base_llm import BaseLLM
from vertexai.generative_models import GenerativeModel, Part


class GeminiLLM(BaseLLM):
    """
    Class for the Gemini Language Learning Model (LLM).

    This class provides the necessary functionality to register the Gemini LLM
    with the specified location and project.

    Attributes:
        location (str): The location where the model is deployed or stored.
        project (str): The project name associated with the model.
        model_name (str): The name of the model.
    """

    def register_model(self):
        """
        Registers the Gemini LLM with the specified location and project.
        """
        logging.info(
            f"Registering Gemini LLM with location: {self.location}, project: {self.project}, model_name: {self.model_name}")
        vertexai.init(project=self.project, location=self.location)
        self.model = GenerativeModel(self.model_name)

    def generate_content(self, video_file_uri, prompt):
        video_file = Part.from_uri(video_file_uri, mime_type="video/mp4")
        contents = [video_file, prompt]
        response = self.model.generate_content(contents)
        logging.debug(f"Response from Gemini LLM: {response}")
