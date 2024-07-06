from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.ext.declarative import declarative_base

class PromptResponse(declarative_base()):
    __tablename__ = "prompts"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), unique=True, index=True, nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
