from fastapi import FastAPI, Response, status
import os
import uvicorn

from scraper.scraper import fetch_hashtag_videos, fetch_trending_videos
from response.VideoResponse import VideoResponse

app = FastAPI()

@app.get("/trending", response_model=VideoResponse)
async def trending_videos(response: Response):
    result = await fetch_trending_videos()
    if result.error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return result

@app.get("/hashtag", response_model=VideoResponse)
async def root(response: Response):
    result = await fetch_hashtag_videos()
    if result.error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
