from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StoryBase(BaseModel):
    date: datetime
    title: str
    href: str
    hnews: Optional[str] = None
    lobsters: Optional[str] = None
    reddit: Optional[str] = None
    tags: list[str]


class Story(StoryBase):
    class Config:
        from_attributes = True


class StoryCreate(StoryBase):
    pass


class StoryUpdate(StoryBase):
    pass


class News(BaseModel):
    stories: list[Story]
    tags: list[str]


class ErrorResponse(BaseModel):
    error: str


class MessageResponse(BaseModel):
    message: str
