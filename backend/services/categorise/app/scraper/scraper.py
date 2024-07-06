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
            videos_info = []
            # FROM: https://github.com/davidteather/TikTok-Api/issues/1040
            async for video in api.hashtag(name="funny").videos(count=10):
                print("username: " + video.author.username)
                print("video id: " + video.id)
                print("stats: " + str(video.stats))

                video_info = {
                    "link": "https://www.tiktok.com/@" + video.author.username + "/video/" + video.id,
                    "views": video.stats['playCount'],
                    "author": video.author.username,
                }

                videos_info.append(video_info)

            # Sort videos by view count in descending order
            videos_info_sorted = sorted(videos_info, key=lambda x: x['views'], reverse=True)

            videos = []
            # Only download the top 10 videos
            for vid in videos_info_sorted[:5]:  # Limit to top 10
                videos.append(vid['link'])
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([vid['link']])
                
            return VideoResponse(error=False, urls=videos)

async def fetch_trending_videos():
    async with async_playwright():
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, 
                                  headless=False, suppress_resource_load_types=["image", "media", "font", "stylesheet"])
            videos_info = []
            # FROM: https://github.com/davidteather/TikTok-Api/issues/1040
            async for video in api.trending.videos(count=10):
                print("username: " + video.author.username)
                print("video id: " + video.id)
                print("stats: " + str(video.stats))


                video_info = {
                    "link": "https://www.tiktok.com/@" + video.author.username + "/video/" + video.id,
                    "views": video.stats['playCount'],
                    "author": video.author.username,
                }

                videos_info.append(video_info)

            # Sort videos by view count in descending order
            videos_info_sorted = sorted(videos_info, key=lambda x: x['views'], reverse=True)

            videos = []
            # Only download the top 10 videos
            for vid in videos_info_sorted[:5]:  # Limit to top 10
                videos.append(vid['link'])
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([vid['link']])
                
            return VideoResponse(error=False, urls=videos)

async def fetch_username_videos():
    async with async_playwright():
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, 
                                      headless=False, suppress_resource_load_types=["image", "media", "font", "stylesheet"])
            videos_info = []
            async for video in api.user(username="funny_ooo").videos(count=10):
                print("username: " + video.author.username)
                print("video id: " + video.id)
                print("stats: " + str(video.stats))

                video_info = {
                    "link": "https://www.tiktok.com/@" + video.author.username + "/video/" + video.id,
                    "views": video.stats['playCount'],
                    "author": video.author.username,
                }
                videos_info.append(video_info)

            # Sort videos by view count in descending order
            videos_info_sorted = sorted(videos_info, key=lambda x: x['views'], reverse=True)

            videos = []
            # Only download the top 10 videos
            for vid in videos_info_sorted[:5]:  # Limit to top 10
                videos.append(vid['link'])
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([vid['link']])
                
            return VideoResponse(error=False, urls=videos)

#to test and experiement
# async def user_example():
#     async with TikTokApi() as api:
#         await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, 
#                                       headless=False, suppress_resource_load_types=["image", "media", "font", "stylesheet"])
#         user = api.user("therock")
#         user_data = await user.info()
#         print(user_data)

#         async for video in user.videos(count=30):
#             print(video)
#             print(video.as_dict)