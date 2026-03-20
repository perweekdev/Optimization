from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.models.movie import Movie
from app.schemas.movie import MovieCreate

async def create_movie(db: AsyncSession, movie: Movie) -> Movie:
    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    return movie

async def get_movies(db: AsyncSession, skip: int = 0, limit: int = 20) -> List[Movie]:
    result = await db.execute(
        select(Movie).offset(skip).limit(limit).order_by(Movie.created_at.desc())
    )
    return result.scalars().all()

async def get_movie(db: AsyncSession, movie_id: int) -> Optional[Movie]:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    return result.scalar_one_or_none()

async def get_movie_by_title(db: AsyncSession, title: str) -> Optional[Movie]:
    result = await db.execute(select(Movie).where(Movie.title == title))
    return result.scalar_one_or_none()

async def delete_movie(db: AsyncSession, movie_id: int) -> bool:
    movie = await get_movie(db, movie_id)
    if movie:
        await db.delete(movie)
        await db.commit()
        return True
    return False