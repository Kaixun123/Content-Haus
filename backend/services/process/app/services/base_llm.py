from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Abstract base class for Language Learning Models (LLM).

    This class provides a template for initializing and registering language learning models
    with the necessary attributes such as location, project, and model name.

    Attributes:
        location (str): The location where the model is deployed or stored.
        project (str): The project name associated with the model.
        model_name (str): The name of the model.
    """

    def __init__(self, location, project, model_name, credentials=None):
        """
        Initializes a new instance of the BaseLLM class.

        Args:
            location (str): The location where the model is deployed or stored.
            project (str): The project name associated with the model.
            model_name (str): The name of the model.
        """
        self.location = location
        self.project = project
        self.model_name = model_name
        self.credentials = credentials
        self.register_model()

    @abstractmethod
    def register_model(self):
        """
        Abstract method to register the model.

        Implementations should provide the mechanism to register the model
        in the specified location and project.
        """
        pass
