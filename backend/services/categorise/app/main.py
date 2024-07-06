from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares.logging import LoggingMiddleware
from app.middlewares.cors import CorsMiddleware

app = FastAPI()

LoggingMiddleware(app)
CorsMiddleware(app)

@app.get("/")
def read_root():
    return {"Hello": "World"}