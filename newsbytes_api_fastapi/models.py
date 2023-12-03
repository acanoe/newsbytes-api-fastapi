import sqlalchemy

from .crud import CRUDBase
from .database import Base
from .schemas import StoryCreate, StoryUpdate


class StoryOrm(Base):
    __tablename__ = "stories"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    href = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    hnews = sqlalchemy.Column(sqlalchemy.String)
    lobsters = sqlalchemy.Column(sqlalchemy.String)
    reddit = sqlalchemy.Column(sqlalchemy.String)
    tags = sqlalchemy.Column(sqlalchemy.String)


class CRUDStory(CRUDBase[StoryOrm, StoryCreate, StoryUpdate]):
    def get_by_tag(self, db: sqlalchemy.orm.Session, tag: str) -> list[StoryOrm]:
        return db.query(StoryOrm).filter(StoryOrm.tags.contains(tag)).all()


stories = CRUDStory(StoryOrm)
