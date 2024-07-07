import os
import tempfile
from TikTokApi import TikTokApi
from playwright.async_api import async_playwright
from yt_dlp import YoutubeDL
from google.cloud import storage
from dotenv import load_dotenv

from app.services.queries import create_search, add_video
from app.response.VideoResponse import VideoResponse
from app.services.database import get_db_session

# Load environment variables from .env file
load_dotenv()

# Get the path to the Google Cloud credentials JSON file
google_application_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_application_credentials
gcp_bucket = os.getenv('GCP_BUCKET')

# set your own ms_token from tiktok.com cookies
ms_token = os.environ.get("ms_token", None)

# Initialize GCP storage client


def upload_to_gcp(bucket_name, source_file_path, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_path, content_type='video/mp4')

    print(f"File uploaded to {destination_blob_name}.")


class YTDLPLogger:
    def debug(self, msg):
        print(f"DEBUG: {msg}")

    def info(self, msg):
        print(f"INFO: {msg}")

    def warning(self, msg):
        print(f"WARNING: {msg}")

    def error(self, msg):
        print(f"ERROR: {msg}")


async def fetch_videos(api_function, type_name: str, **kwargs):
    async with get_db_session() as db:
        async with async_playwright():
            async with TikTokApi() as api:
                await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3,
                                          headless=False, suppress_resource_load_types=["image", "media", "font", "stylesheet"])
                videos_info = []
                async for video in api_function(api, **kwargs):
                    print("username: " + video.author.username)
                    print("video id: " + video.id)
                    print("stats: " + str(video.stats))

                    video_info = {
                        "id": video.id,
                        "link": "https://www.tiktok.com/@" + video.author.username + "/video/" + video.id,
                        "views": video.stats['playCount'],
                        "author": video.author.username,
                    }
                    videos_info.append(video_info)

                # Sort videos by view count in descending order
                videos_info_sorted = sorted(
                    videos_info, key=lambda x: x['views'], reverse=True)

                # Save search to DB
                search = await create_search(db, type_name)

                videos = []
                # Only download the top video
                for vid in videos_info_sorted[:1]:  # Limit to top 1 for now
                    gcp_link = f"{vid['author']}_{vid['id']}.mp4"
                    videos.append(gcp_link)

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                        temp_file_path = temp_file.name

                    # Ensure the file does not exist before downloading
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)

                    def progress_hook(d):
                        if d['status'] == 'finished':
                            print("Download finished, verifying the file size")
                            file_size = os.path.getsize(temp_file_path)
                            if file_size > 0:
                                print(f"File size is {
                                      file_size} bytes. Uploading to GCP")
                                upload_to_gcp(
                                    gcp_bucket, temp_file_path, gcp_link)
                                print(
                                    f"Video downloaded and uploaded: {gcp_link}")
                            else:
                                print("Downloaded file is empty. Skipping upload.")
                        elif d['status'] == 'downloading':
                            print(f"Downloading: {d['_percent_str']}")

                    ydl_opts = {
                        'outtmpl': temp_file_path,  # Save to a temporary file
                        'format': 'bestvideo+bestaudio/best',
                        'quiet': True,
                        'noplaylist': True,
                        'progress_hooks': [progress_hook],
                        'logger': YTDLPLogger(),
                    }

                    try:
                        with YoutubeDL(ydl_opts) as ydl:
                            ydl.download([vid['link']])
                    except Exception as e:
                        print(f"Error downloading video: {e}")

                    # Save video to DB
                    await add_video(db, search.id, vid['link'])

                    # Clean up temporary file
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)

                return VideoResponse(error=False, urls=videos)


async def fetch_hashtag_videos(name: str):
    return await fetch_videos(lambda api, **kwargs: api.hashtag(name=kwargs['name']).videos(count=5), name=name)


async def fetch_trending_videos():
    return await fetch_videos(lambda api, **kwargs: api.trending.videos(count=5), type_name="trending")


async def fetch_username_videos(username: str):
    return await fetch_videos(lambda api, **kwargs: api.user(username=kwargs['username']).videos(count=5), username=username)
