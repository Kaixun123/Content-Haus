import json
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage
from google.oauth2.service_account import Credentials

from app.api.v1.process import ProcessController
from app.config import Config

app = FastAPI()
config = Config()

logging.basicConfig(
    level=config['log.level'],
    format='%(asctime)s [%(threadName)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %Z'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate Google Cloud Storage client
try:
    credentials_info = json.loads(config['google.application.credentials'])
    credentials = Credentials.from_service_account_info(credentials_info)
    storage_client = storage.Client(credentials=credentials)
    BUCKET_NAME = config['bucket.name']
    logging.info(f"Instantiate bucket: {BUCKET_NAME}")
except Exception as e:
    logging.error(f"Failed to instantiate bucket: {e}")

app.include_router(ProcessController().get_router())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
