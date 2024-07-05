import os

import boto3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import Config
from services.gemini_llm import GeminiLLM

app = FastAPI()
config = Config()

# Maybe TODO: Move registration of middlewares to separate module
# LoggingMiddleware(app)
# CorsMiddleware(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate s3 client
# TODO: Use Env
s3_client = boto3.client('s3')
BUCKET_NAME = config['bucket.name']

# Instantiate LLM
llm = GeminiLLM(
    location=config['gemini.location'],
    project=config['gemini.project.id'],
    model_name=config['gemini.model.name'],
)


# Pydantic Model for Video Requests
class VideoRequest(BaseModel):
    key: str


# Credentials
# TODO: Use env variables for Google Credentials

# Prompt configuration
configured_prompt = "Analyse this video, and come up with a storyboard for recreating this video. It should be engaging and appeal to users."


# This UUID to be stored as key in cloud bucket.
@app.post("/process-video/")
async def process_video(request: VideoRequest):
    video_key = request.key
    local_video_path = f"/tmp/{video_key.split('/')[-1]}"

    # Download video from S3
    try:
        s3_client.download_file(BUCKET_NAME, video_key, local_video_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading video: {e}")

    # Run the Gemini model on the video
    try:
        output = llm.generate_content(local_video_path, configured_prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {e}")

    # Delete the video locally
    try:
        os.remove(local_video_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting local video: {e}")

    return {"message": "Video processed successfully", "output": output}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
