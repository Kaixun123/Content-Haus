from pydantic import BaseModel

class UploadResponse(BaseModel):
    key_id: str