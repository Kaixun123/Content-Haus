from sqlalchemy import Column, String, Text, Integer

from app.models.base import Base


class PromptResponse(Base):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, index=True, nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
