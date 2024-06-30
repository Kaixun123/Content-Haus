from TikTokApi import TikTokApi
import asyncio
from playwright.async_api import async_playwright
from yt_dlp import YoutubeDL
import os

from response.VideoResponse import VideoResponse

ms_token = os.environ.get("ms_token", None)  # set your own ms_token from tiktok.com cookies
ydl_opts = {
    'outtmpl': 'output/%(uploader)s_%(id)s_%(timestamp)s.%(ext)s',
}

async def fetch_hashtag_videos():
    async with async_playwright():
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, 
                                  headless=False, suppress_resource_load_types=["image", "media", "font", "stylesheet"])
            videos = []
            # FROM: https://github.com/davidteather/TikTok-Api/issues/1040
            async for video in api.hashtag(name="funny").videos(count=5):
                print("username: " + video.author.username)
                print("video id: " + video.id)
                print("stats: " + str(video.stats))

                video_link = "https://www.tiktok.com/@" + video.author.username + "/video/" + video.id
                videos.append(video_link)
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_link])
            
            return VideoResponse(error=False, urls=videos)

async def fetch_trending_videos():
    async with async_playwright():
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, 
                                  headless=False, suppress_resource_load_types=["image", "media", "font", "stylesheet"])
            videos = []
            # FROM: https://github.com/davidteather/TikTok-Api/issues/1040
            async for video in api.trending.videos(count=5):
                print("username: " + video.author.username)
                print("video id: " + video.id)
                print("stats: " + str(video.stats))

                video_link = "https://www.tiktok.com/@" + video.author.username + "/video/" + video.id
                videos.append(video_link)
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_link])
                
            return VideoResponse(error=False, urls=videos)
