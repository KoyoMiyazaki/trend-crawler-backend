from app.database import Base
from sqlalchemy import Column, String, DateTime


class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    source = Column(String, nullable=False)
    published_at = Column(DateTime)
    fetched_at = Column(DateTime, nullable=False)
