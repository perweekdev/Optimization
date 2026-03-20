from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from app.core.config import settings

# 비동기 SQLAlchemy 엔진
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True,  # 개발 중 쿼리 로깅
    pool_pre_ping=True
)

# 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# 기본 Base 클래스
class Base(DeclarativeBase):
    pass

# DB 세션 의존성
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()