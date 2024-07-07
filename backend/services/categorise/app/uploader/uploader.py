import os
import uuid
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

def upload_to_gcp_bucket(file):
    # Initialize a storage client
    storage_client = storage.Client()

    # Define the bucket name and destination blob name
    bucket_name = os.getenv('GCP_BUCKET')
    key_id = str(uuid.uuid4())
    blob_name = f'userUploads/{key_id}/{file.filename}'

    # Get the bucket and blob
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Upload the file
    blob.upload_from_file(file.file, content_type=file.content_type)

    return blob_name