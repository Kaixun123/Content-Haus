import logging
import os

from google.cloud import storage
from config import Config
from services.gemini_llm import GeminiLLM
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
config = Config()


logging.basicConfig(
    level=config['log.level'],
    format='%(asctime)s [%(threadName)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %Z'
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=config['google.application.credentials']
logging.info(f"Configuration path set: {os.environ["GOOGLE_APPLICATION_CREDENTIALS"]}")

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

# Instantiate Google Cloud Storage client
# TODO: Use Env
storage_client = storage.Client()
BUCKET_NAME = config['bucket.name']
logging.info(f"Instantiate bucket: {BUCKET_NAME}")

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

    # Download video from Google Cloud Storage
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(video_key)
        blob.download_to_filename(local_video_path)
        logging.info("Successful video download")
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        raise HTTPException(status_code=500, detail=f"Error downloading video: {e}")

    # Run the Gemini model on the video
    try:
        logging.info("Attempting LLM prediction...")
        output = llm.generate_content(local_video_path, configured_prompt)
        logging.info("Successful video process")
    except Exception as e:
        logging.error(f"Error processing video: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing video: {e}")

    # Delete the video locally
    try:
        os.remove(local_video_path)
        logging.info("Video deleted")
    except Exception as e:
        logging.error(f"Error deleting video: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting local video: {e}")

    return {"message": "Video processed successfully", "output": output}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
