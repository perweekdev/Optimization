from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

import httpx

from app.database import get_db
from app.core.config import settings
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieResponse
from app.crud.movies import create_movie, get_movies, get_movie, delete_movie
from app.services.tmdb import initialize_movies_from_tmdb

router = APIRouter(prefix="/movies", tags=["movies"])

@router.post("/", response_model=MovieResponse)
async def create_movie(movie_data: MovieCreate, db: AsyncSession = Depends(get_db)):
    """영화 수동 추가 (관리자용)"""
    return await create_movie(db, movie_data)

@router.get("/", response_model=List[MovieResponse])
async def list_movies(db: AsyncSession = Depends(get_db)):
    """영화 목록 조회 (최근 20개)"""
    return await get_movies(db)

@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie_detail(movie_id: int, db: AsyncSession = Depends(get_db)):
    """영화 상세 조회"""
    movie = await get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.delete("/{movie_id}")
async def delete_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    """영화 삭제 (관리자용)"""
    success = await delete_movie(db, movie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}

@router.post("/initialize")
async def initialize_movies():
    """TMDB에서 최신 인기 영화 20개 자동 수집"""
    result = await initialize_movies_from_tmdb()
    return result