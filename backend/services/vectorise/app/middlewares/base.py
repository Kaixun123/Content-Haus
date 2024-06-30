from abc import ABC, abstractmethod

class Middleware(ABC):
    """
    An abstract base class that defines the interface for middleware classes.
    
    All middleware classes inheriting from this interface must implement the
    __apply method, which applies the middleware's functionality to a FastAPI application.
    """
    
    @abstractmethod
    def apply(self):
        """
        An abstract method that must be implemented by subclasses to apply
        middleware settings to a FastAPI application.
        """
        pass