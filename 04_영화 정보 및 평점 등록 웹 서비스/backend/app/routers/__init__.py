from fastapi import APIRouter
from .auth import router as auth_router
from .movies import router as movies_router
from .reviews import router as reviews_router

# 모든 라우터를 하나의 메인 라우터에 통합
router = APIRouter()

# 각 라우터 등록
router.include_router(auth_router, tags=["auth"])
router.include_router(movies_router, tags=["movies"])
router.include_router(reviews_router, tags=["reviews"])

__all__ = ["router"]