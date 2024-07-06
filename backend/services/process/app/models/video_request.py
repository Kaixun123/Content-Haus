from pydantic import BaseModel


# Pydantic Model for Video Requests
class VideoRequest(BaseModel):
    key: str
