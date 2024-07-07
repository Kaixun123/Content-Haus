# main.py
from fastapi import FastAPI
import uvicorn

from app.middlewares.logging import LoggingMiddleware
from app.middlewares.cors import CorsMiddleware
from app.api.v1.categorise import CategoriseRestController

description = """
Categorise Function for Tiktok hackathon🚀

## Scraper

Functions:

* **Get trending** (_/trending - Download and get the latest trending videos in tiktok_)
* **Get by hashtag** (_/hashtag - Get the latest hashtag popular videos in tiktok_)
"""


app = FastAPI(
    title="Categorise Function",
    description=description,
)

LoggingMiddleware(app)
CorsMiddleware(app)

app.include_router(CategoriseRestController().get_router())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
