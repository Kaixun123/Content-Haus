from TikTokApi import TikTokApi
import asyncio
from playwright.async_api import async_playwright
from response.VideoResponse import VideoResponse
import os

ms_token = os.environ.get("ms_token", None)  # set your own ms_token from tiktok.com cookies

async def fetch_hashtag_videos():
    async with async_playwright():
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
            tag = api.hashtag(name="funny")
            videos = []
            async for video in tag.videos(count=30):
                video_dict = video.as_dict
                
                try:
                    last_url = video_dict['video']['bitrateInfo'][-1]['PlayAddr']['UrlList'][-1]
                    videos.append(last_url)
                except (KeyError, IndexError) as e:
                    print(f"Error extracting URL: {e}")
                    print(e)
                    return VideoResponse(error=True, urls=[])
            
            return VideoResponse(error=False, urls=videos)

async def fetch_trending_videos():
    async with async_playwright():
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, headless=False)
            videos = []
            async for video in api.trending.videos(count=30):
                video_dict = video.as_dict
                
                try:
                    last_url = video_dict['video']['bitrateInfo'][-1]['PlayAddr']['UrlList']
                    videos.append(last_url)
                except (KeyError, IndexError) as e:
                    print(f"Error extracting URL: {e}")
                    return VideoResponse(error=True, urls=[])
                
            return VideoResponse(error=False, urls=videos)
