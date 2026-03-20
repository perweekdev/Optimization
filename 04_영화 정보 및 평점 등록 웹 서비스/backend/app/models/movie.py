from sqlalchemy import Column, Integer, String, Date, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, index=True, nullable=False)
    release_date = Column(Date)
    director = Column(String(100))
    genre = Column(String(255))
    poster_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())