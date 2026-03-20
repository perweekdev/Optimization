from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from app.database import engine, Base
from app.routers import router

# FastAPI 앱 생성
app = FastAPI(
    title="Movie Review API",
    description="영화 리뷰 서비스 백엔드 (Streamlit 연동)",
    version="1.0.0"
)

# CORS 설정 (Streamlit localhost:8501 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB 테이블 자동 생성 (개발용, Alembic 권장)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()

# 모든 라우터 등록 (한 줄!)
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Movie Review API 운영중", "docs": "/docs"}