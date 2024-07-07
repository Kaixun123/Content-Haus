from TikTokApi import TikTokApi
import asyncio
from playwright.async_api import async_playwright
from yt_dlp import YoutubeDL
import os
from response.VideoResponse import VideoResponse
from google.cloud import storage
from dotenv import load_dotenv
import io
import sys

# Load environment variables from .env file
load_dotenv()

# Get the path to the Google Cloud credentials JSON file
google_application_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_application_credentials
gcp_bucket = os.getenv('GCP_BUCKET')

ms_token = os.environ.get("ms_token", None)  # set your own ms_token from tiktok.com cookies

# Initialize GCP storage client
def upload_to_gcp(bucket_name, source_data, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(source_data, rewind=True, content_type='video/mp4')

    print(f"File uploaded to {destination_blob_name}.")

async def fetch_videos(api_function, **kwargs):
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
            videos_info_sorted = sorted(videos_info, key=lambda x: x['views'], reverse=True)

            videos = []
            # Only download the top 10 videos
            for vid in videos_info_sorted[:10]:  # Limit to top 10
                videos.append(vid['link'])
                buffer = io.BytesIO()
                
                def progress_hook(d):
                    if d['status'] == 'finished':
                        buffer.seek(0)
                        upload_to_gcp(gcp_bucket, buffer, f"{vid['author']}_{vid['id']}.mp4")
                        buffer.close()
                
                ydl_opts = {
                    'outtmpl': '-',  # Use a placeholder to force in-memory storage
                    'format': 'bestvideo+bestaudio/best',
                    'quiet': True,
                    'noplaylist': True,
                    'progress_hooks': [progress_hook],
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }],
                }

                # Redirect stdout and stderr to null to suppress verbose output
                with open(os.devnull, 'w') as devnull:
                    old_stdout = sys.stdout
                    old_stderr = sys.stderr
                    sys.stdout = devnull
                    sys.stderr = devnull
                    try:
                        with YoutubeDL(ydl_opts) as ydl:
                            ydl.download([vid['link']])
                    finally:
                        sys.stdout = old_stdout
                        sys.stderr = old_stderr
                    
            return VideoResponse(error=False, urls=videos)

async def fetch_hashtag_videos(name: str):
    return await fetch_videos(lambda api, **kwargs: api.hashtag(name=kwargs['name']).videos(count=10), name=name)

async def fetch_trending_videos():
    return await fetch_videos(lambda api, **kwargs: api.trending.videos(count=10))

async def fetch_username_videos(username: str):
    return await fetch_videos(lambda api, **kwargs: api.user(username=kwargs['username']).videos(count=10), username=username)
