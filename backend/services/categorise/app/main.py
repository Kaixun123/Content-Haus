from fastapi import FastAPI
import uvicorn

from app.middlewares.logging import LoggingMiddleware
from app.middlewares.cors import CorsMiddleware
from app.api.v1.categorise import CategoriseRestController

description = """
Categorise Function for Tiktok hackathon🚀

## Scraper

Functions:

* **GET - Get trending** (_/trending - Download and get the latest trending videos in tiktok_)
* **GET - Get by hashtag** (_/hashtag?hashtag=<hashtagVal> - Get the latest hashtag popular videos in tiktok_)
* **GET - Get by username** (_/username?username=<usernameVal> - Get the popular videos from username_)
* **POST - Upload videos** (_/upload (Body - file)- Upload videos to gcp_)
"""

app = FastAPI(
    title="Categorise Function",
    description=description,
)

LoggingMiddleware(app)
CorsMiddleware(app)

app.include_router(CategoriseRestController().get_router())
app.include_router(UploadRestController().get_router())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
