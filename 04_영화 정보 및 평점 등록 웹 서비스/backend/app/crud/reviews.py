from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.review import Review

async def create_review(db: AsyncSession, review: Review) -> Review:
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review

async def get_recent_reviews(db: AsyncSession, limit: int = 10) -> List[Review]:
    """미션 요구사항: 최근 10개 리뷰 (영화ID, 등록일, 리뷰내용)"""
    result = await db.execute(
        select(Review).order_by(Review.created_at.desc()).limit(limit)
    )
    return result.scalars().all()

async def get_movie_reviews(db: AsyncSession, movie_id: int) -> List[Review]:
    result = await db.execute(
        select(Review).where(Review.movie_id == movie_id).order_by(Review.created_at.desc())
    )
    return result.scalars().all()