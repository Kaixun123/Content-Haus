import time
import logging
from fastapi import FastAPI, Request

from app.middlewares.base import Middleware

class LoggingMiddleware(Middleware):
    """
    A singleton middleware class for logging HTTP requests in a FastAPI application.
    
    This class ensures that only one instance of itself can be created and applies
    logging functionality to log details of HTTP requests made to the FastAPI application.
    
    Attributes:
        _instance (LoggingMiddleware): The singleton instance of the LoggingMiddleware, private.
    """
    __instance = None

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
            cls.__instance = super(LoggingMiddleware, cls).__new__(cls)
            cls.__instance.__app = app
            cls.__instance.apply()
        return cls.__instance

    def apply(self):
        """
        Private method to apply logging middleware settings to the FastAPI application.
        This method configures the application to log details of HTTP requests including
        method, path, and duration of the request.
        
        Parameters:
            app (FastAPI): The FastAPI application to which the logging settings will be applied.
        """
        @self.__app.middleware("http")
        async def log_request_middleware(request: Request, call_next):
            request_start_time = time.monotonic()
            response = await call_next(request)
            request_duration = time.monotonic() - request_start_time
            log_data = {
                "method": request.method,
                "path": request.url.path,
                "duration": request_duration
            }
            logging.info(log_data)
            return response