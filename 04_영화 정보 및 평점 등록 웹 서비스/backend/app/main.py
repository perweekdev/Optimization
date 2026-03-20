from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Movie Review API", 
    description="영화 리뷰 서비스 (Streamlit 연동)",
    version="1.0.0"
)

# CORS (Streamlit 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Movie Review API 🚀", "docs": "/docs", "redoc": "/redoc"}

# 모든 라우터 지연 로드 (순환 임포트 방지)
@app.on_event("startup")
async def startup():
    # DB 테이블 생성
    from app.database import engine, Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("🚀 Startup complete! http://localhost:8000/docs")

# 라우터 등록 (런타임에만)
try:
    from app.routers import router
    app.include_router(router)
except ImportError as e:
    print(f"Router import error (normal during startup): {e}")