from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models.review import Review


async def create_review(db: AsyncSession, review: Review) -> Review:
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review


async def get_recent_reviews(db: AsyncSession, limit: int = 10) -> List[Review]:
    result = await db.execute(
        select(Review)
        .options(
            selectinload(Review.movie),
            selectinload(Review.user)
        )
        .order_by(Review.created_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def get_movie_reviews(db: AsyncSession, movie_id: int) -> List[Review]:
    result = await db.execute(
        select(Review)
        .options(
            selectinload(Review.movie),
            selectinload(Review.user)
        )
        .where(Review.movie_id == movie_id)
        .order_by(Review.created_at.desc())
    )
    return result.scalars().all()


async def get_review_by_id(db: AsyncSession, review_id: int) -> Optional[Review]:
    result = await db.execute(
        select(Review).where(Review.id == review_id)
    )
    return result.scalar_one_or_none()


async def delete_review(db: AsyncSession, review: Review) -> None:
    await db.delete(review)
    await db.commit()