from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.core.security import get_current_user
from app.models.review import Review
from app.models.user import User
from app.models.movie import Movie
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewListResponse
from app.crud.reviews import (
    create_review,
    get_recent_reviews,
    get_movie_reviews,
    get_review_by_id,
    delete_review,
)

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewResponse)
async def create_review_endpoint(
    review_data: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """리뷰 작성 (로그인 필수)"""
    result = await db.execute(select(Movie).where(Movie.id == review_data.movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    review = Review(
        movie_id=review_data.movie_id,
        user_id=current_user.id,
        content=review_data.content
    )

    return await create_review(db, review)


@router.get("/latest", response_model=List[ReviewListResponse])
async def get_latest_reviews(db: AsyncSession = Depends(get_db)):
    """최근 10개 리뷰 조회"""
    reviews = await get_recent_reviews(db)

    return [
        ReviewListResponse(
            id=review.id,
            movie_id=review.movie_id,
            user_id=review.user_id,
            content=review.content,
            created_at=review.created_at,
            movie_title=review.movie.title if review.movie else "미상",
            username=review.user.username if review.user else "알수없음",
        )
        for review in reviews
    ]


@router.get("/movie/{movie_id}", response_model=List[ReviewListResponse])
async def get_movie_reviews_endpoint(movie_id: int, db: AsyncSession = Depends(get_db)):
    """특정 영화 리뷰 조회"""
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    reviews = await get_movie_reviews(db, movie_id)

    return [
        ReviewListResponse(
            id=review.id,
            movie_id=review.movie_id,
            user_id=review.user_id,
            content=review.content,
            created_at=review.created_at,
            movie_title=review.movie.title if review.movie else "미상",
            username=review.user.username if review.user else "알수없음",
        )
        for review in reviews
    ]


@router.delete("/{review_id}")
async def delete_review_endpoint(
    review_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """리뷰 삭제 (본인 리뷰만 가능)"""
    review = await get_review_by_id(db, review_id)

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this review"
        )

    await delete_review(db, review)

    return {"message": "Review deleted successfully"}