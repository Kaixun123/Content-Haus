from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from middlewares.base import Middleware


class CorsMiddleware(Middleware):
    """
    A singleton class to apply CORS middleware to a FastAPI application.

    This class ensures that only one instance of itself can be created and
    applies CORS settings to the FastAPI application to allow requests from
    specified origins.

    Attributes:
        __instance (CorsMiddleware): The singleton instance of the CorsMiddleware, private.
        __app (FastAPI): The FastAPI application instance, private.
        __origins (list): A list of origins allowed to make requests to the FastAPI application, private.

    Methods:
        __new__(cls, app: FastAPI): Creates a new instance of CorsMiddleware if one doesn't exist.
        __apply(): Applies CORS middleware settings to the FastAPI application.
    """

    __instance = None
    __app = None
    __origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://tiktok-techjam-2024.web.app"
    ]

    def __new__(cls, app: FastAPI):
        """
        Ensures that only one instance of CorsMiddleware is created. If an instance
        already exists, it returns that instance; otherwise, it creates a new one,
        applies the CORS settings to the provided FastAPI application, and returns
        the new instance.

        Parameters:
            app (FastAPI): The FastAPI application to which the CORS settings will be applied.

        Returns:
            CorsMiddleware: The singleton instance of the CorsMiddleware.
        """
        if cls.__instance is None:
            cls.__instance = super(CorsMiddleware, cls).__new__(cls)
            cls.__instance.__app = app
            cls.__instance.apply()
        return cls.__instance

    def apply(self):
        """
        Private method to apply CORS middleware settings to the FastAPI application.
        This method configures the application to allow requests from the specified origins,
        with any HTTP method and any header.
        """
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=self.__origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
