from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Search, Video

async def create_search(db: AsyncSession, type_name: str):
    search = Search(type=type_name)
    db.add(search)
    await db.commit()
    await db.refresh(search)
    return search

async def add_video(db: AsyncSession, search_id: int, video_url: str):
    video = Video(search_id=search_id, video_url=video_url)
    db.add(video)
    await db.commit()
    await db.refresh(video)
    return video
