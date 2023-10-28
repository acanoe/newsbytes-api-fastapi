from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Story(BaseModel):
    id: int
    date: datetime
    title: str
    href: str
    hnews: Optional[str] = None
    lobsters: Optional[str] = None
    reddit: Optional[str] = None
    tags: list[str]


class News(BaseModel):
    stories: list[Story]
    tags: list[str]
