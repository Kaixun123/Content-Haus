from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares.logging import LoggingMiddleware
from app.middlewares.cors import CorsMiddleware
from app.api.v1.vectorise import VectoriseRestController

app = FastAPI()

# Maybe TODO: Move registration of middlewares to separate module
LoggingMiddleware(app)
CorsMiddleware(app)

# Maybe TODO: Move registration of routers to separate module
app.include_router(VectoriseRestController().get_router())
