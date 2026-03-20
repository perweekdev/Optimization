import httpx
from datetime import datetime, date
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.database import get_db
from app.crud.movies import create_movie, get_movie_by_title
from app.models.movie import Movie


def parse_release_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


async def initialize_movies_from_tmdb(limit: int = 20) -> Dict[str, Any]:
    """TMDB API에서 최신 인기 영화 20개 가져와 DB 저장"""

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                "https://api.themoviedb.org/3/movie/popular",
                params={
                    "api_key": settings.TMDB_API_KEY,
                    "language": "ko-KR",
                    "page": 1,
                },
            )
            response.raise_for_status()
            tmdb_movies: List[Dict[str, Any]] = response.json()["results"][:limit]
        except httpx.HTTPStatusError as e:
            raise Exception(f"TMDB API 오류 ({e.response.status_code}): {e.response.text}")
        except Exception as e:
            raise Exception(f"TMDB 연결 실패: {str(e)}")

    saved_count = 0

    async for db in get_db():
        for movie_data in tmdb_movies:
            title = movie_data.get("title")
            if not title:
                continue

            existing_movie = await get_movie_by_title(db, title)
            if existing_movie:
                continue

            release_date = parse_release_date(movie_data.get("release_date"))
            poster_path = movie_data.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            db_movie = Movie(
                title=title,
                release_date=release_date,
                director="미상",
                genre="드라마, 액션",
                poster_url=poster_url,
            )

            await create_movie(db, db_movie)
            saved_count += 1

    return {
        "message": f"{saved_count}/{len(tmdb_movies)} movies initialized from TMDB!",
        "saved": saved_count,
        "total": len(tmdb_movies),
    }