import os
from fastapi import FastAPI
import uvicorn
from middlewares.logging import LoggingMiddleware
from middlewares.cors import CorsMiddleware

from api.v1.editor import EditorRestController

app = FastAPI(
    title="Editor Function"
)

LoggingMiddleware(app)
CorsMiddleware(app)

app.include_router(EditorRestController().get_router())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", reload=True)
