# routes/videoRoutes.py
from fastapi import APIRouter, Response, status, Query
from scraper.scraper import fetch_hashtag_videos, fetch_trending_videos, fetch_username_videos
from response.VideoResponse import VideoResponse

router = APIRouter()

@router.get("/trending", response_model=VideoResponse)
async def trending_videos(response: Response):
    result = await fetch_trending_videos()
    if result.error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return result

@router.get("/hashtag", response_model=VideoResponse)
async def hashtag_videos(response: Response, hashtag: str = Query(..., description="Hashtag to search for")):
    result = await fetch_hashtag_videos(name=hashtag)
    if result.error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return result

@router.get("/username", response_model=VideoResponse)
async def username_videos(response: Response, username: str = Query(..., description="Username to search for")):
    result = await fetch_username_videos(username=username)
    if result.error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return result   