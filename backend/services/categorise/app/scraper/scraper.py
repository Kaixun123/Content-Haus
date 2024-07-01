from TikTokApi import TikTokApi
import asyncio
from playwright.async_api import async_playwright
from yt_dlp import YoutubeDL
from yt_dlp.postprocessor.common import PostProcessor
from yt_dlp.utils import sanitize_filename

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

async def fetch_username_videos():
    async with async_playwright():
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, 
                                      headless=False, suppress_resource_load_types=["image", "media", "font", "stylesheet"])
            videos_info = []
            async for video in api.user(username="funny_ooo").videos(count=20):
                print("username: " + video.author.username)
                print("video id: " + video.id)
                print("stats: " + str(video.stats))
                print(video.desc)

                video_info = {
                    "link": "https://www.tiktok.com/@" + video.author.username + "/video/" + video.id,
                    "views": video.stats['playCount']  # Assuming 'playCount' is the key for views
                }
                videos_info.append(video_info)

            # Sort videos by view count in descending order
            videos_info_sorted = sorted(videos_info, key=lambda x: x['views'], reverse=True)

            videos = []
            # ydl_opts = {}  # Define your YoutubeDL options here
            # Only download the top 10 videos
            for video_info in videos_info_sorted[:10]:  # Limit to top 10
                videos.append(video_info['link'])
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_info['link']])
                
            return VideoResponse(error=False, urls=videos)