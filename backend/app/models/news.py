from sqlalchemy import Column, Integer, String, DateTime
from app.database.base import Base
import datetime

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    link = Column(String, unique=True, index=True, nullable=False)
    image_url = Column(String, nullable=True)
    published_date = Column(String, nullable=True) # Ex: "Há 14 horas" ou data real
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
