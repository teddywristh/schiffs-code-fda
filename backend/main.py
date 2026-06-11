from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from admin import create_admin_user
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.exceptions import DisconnectedDatabaseException, DisconnectedRedisException
from app.core.exceptions import CustomAppException, global_app_exception_handler
from app.core.logger import logger
from app.core.database import AsyncSessionLocal, get_db
from app.core.redis import redis_client, get_redis

from app.api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi động kết nối tới Redis
    try:
        await redis_client.connect()
    except Exception as e:
        logger.error(f"Không thể kết nối tới Redis lúc khởi chạy: {e}")

    async with AsyncSessionLocal() as session:
        try:
            await create_admin_user(session)
        except Exception as e:
            logger.error(f"không thể tạo tài khoản Admin: {e}")
            
    yield
    # Đóng kết nối Redis
    await redis_client.close()

app = FastAPI(title=settings.PROJECT_NAME,
              version="1.0.0",
              lifespan=lifespan)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_exception_handler(CustomAppException, global_app_exception_handler)

@app.get("/", tags=["Root"])
def read_root():
    return {"success": "Welcome to Schiffs Code FDA API!"}

@app.get("/health", tags=["Health"])
async def health_check(
    db: AsyncSession = Depends(get_db),
    redis = Depends(get_redis)
):
    """
    API Health Check kiểm tra kết nối Database và Redis bất đồng bộ toàn diện
    """
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Lỗi kết nối tới Database: {str(e)}")
        raise DisconnectedDatabaseException()

    # Kiểm tra Redis
    try:
        await redis.ping()
    except Exception as e:
        logger.error(f"Lỗi kết nối tới Redis: {str(e)}")
        raise DisconnectedRedisException()

    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected"
    }