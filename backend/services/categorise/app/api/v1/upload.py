from fastapi import APIRouter, UploadFile, File, HTTPException

from scraper.scraper import fetch_hashtag_videos, fetch_trending_videos, fetch_username_videos
from api.v1.base import RestController
from uploader.uploader import upload_to_gcp_bucket

from response.VideoResponse import VideoResponse
from response.UploadResponse import UploadResponse

router = APIRouter()

class UploadRestController(RestController):
    def register_routes(self):
        @self.router.post("/upload", response_model=UploadResponse)
        async def upload_videos(file: UploadFile = File(...)):
            try:
                blob_name = upload_to_gcp_bucket(file)
                return UploadResponse(key_id=blob_name)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file: {str(e)}")