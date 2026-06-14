from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.models.user_model import User
from app.schemas.dev_schema import HealthCheck
from app.core.database import get_db
from app.core.redis import get_redis
from app.api.deps import get_current_developer
from app.core.logger import logger
from app.services.dev_service import dev_service

router = APIRouter()

@router.get("/system-info")
async def get_system_info(
    dev: User = Depends(get_current_developer)
):
    logger.info(f"Developer {dev.email} đang truy cập thông tin hệ thống.")
    return {
        "app_name": "Hệ thống quản lý API",
        "version": "1.0.0",
        "developer": dev.email,
        "message": "Hệ thống ổn định"
    }

@router.get("/health", response_model=HealthCheck)
async def check_connect_db(
    dev: User = Depends(get_current_developer),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    """API Dev kiểm tra kết nối với các cơ sở dữ liệu"""
    return await dev_service.check_health(db=db, redis=redis)
