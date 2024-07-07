from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Search(Base):
    __tablename__ = 'search'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    videos = relationship("Video", back_populates="search")

class Video(Base):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True, autoincrement=True)
    search_id = Column(Integer, ForeignKey('search.id'), nullable=False)
    video_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    search = relationship("Search", back_populates="videos")
