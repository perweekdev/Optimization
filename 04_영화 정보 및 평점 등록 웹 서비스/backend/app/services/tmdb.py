import httpx
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database import get_db
from app.crud.movies import create_movie, get_movie_by_title
from app.models.movie import Movie

async def initialize_movies_from_tmdb(limit: int = 20) -> Dict[str, int]:
    """TMDB API에서 최신 인기 영화 20개 가져와 DB 저장"""
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # TMDB 인기 영화 조회 (한국어)
            response = await client.get(
                "https://api.themoviedb.org/3/movie/popular",
                params={
                    "api_key": settings.TMDB_API_KEY,
                    "language": "ko-KR",
                    "page": 1
                }
            )
            response.raise_for_status()
            tmdb_movies: List[Dict[str, Any]] = response.json()["results"][:limit]
        except httpx.HTTPStatusError as e:
            raise Exception(f"TMDB API 오류 ({e.response.status_code}): {e.response.text}")
        except Exception as e:
            raise Exception(f"TMDB 연결 실패: {str(e)}")
    
    # DB에 저장 (중복 체크)
    saved_count = 0
    async for db in get_db():  # DB 세션 사용
        for movie_data in tmdb_movies:
            title = movie_data["title"]
            
            # 중복 체크
            existing_movie = await get_movie_by_title(db, title)
            if existing_movie:
                continue
            
            # Movie 객체 생성
            db_movie = Movie(
                title=title,
                release_date=movie_data["release_date"][:10] if movie_data["release_date"] else None,
                director="미상",  # credits API 별도 호출 가능
                genre="드라마, 액션",  # 장르 매핑 테이블 구현 가능
                poster_url=f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}" 
                          if movie_data.get('poster_path') else None
            )
            
            await create_movie(db, db_movie)
            saved_count += 1
    
    return {
        "message": f"{saved_count}/{len(tmdb_movies)} movies initialized from TMDB!",
        "saved": saved_count,
        "total": len(tmdb_movies)
    }