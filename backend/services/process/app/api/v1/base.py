from abc import ABC, abstractmethod

from fastapi import APIRouter


class RestController(ABC):
    """
    A base class for REST controllers.

    This class provides a foundational structure for all REST controllers within the application,
    facilitating the creation of modular and reusable RESTful endpoints. It initializes an APIRouter
    instance that subclasses can use to register their specific routes, promoting separation of concerns
    and cleaner code organization.

    Attributes:
        router (APIRouter): An instance of FastAPI's APIRouter, used for registering routes.
    """

    def __init__(self):
        self.router = APIRouter()
        self.register_routes()

    def get_router(self):
        """
        Returns the APIRouter instance associated with the controller.
        
        Returns:
            APIRouter: The APIRouter instance associated with the controller.
        """
        return self.router

    @abstractmethod
    def register_routes(self):
        """
        An abstract method that must be implemented by subclasses to register
        routes for the REST controller.
        """
        pass
