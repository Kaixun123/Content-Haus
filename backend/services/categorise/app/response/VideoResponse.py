from pydantic import BaseModel

class VideoResponse(BaseModel):
    error: bool
    urls: list[str]