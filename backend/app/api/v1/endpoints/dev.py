from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import User
from app.core.database import get_db
from app.api.deps import get_current_developer
from app.core.logger import logger

router = APIRouter()

@router.get("/system-info")
async def get_system_info(
    developer: User = Depends(get_current_developer),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Developer {developer.email} đang truy cập thông tin hệ thống.")
    return {
        "app_name": "Hệ thống quản lý API",
        "version": "1.0.0",
        "developer": developer.email,
        "message": "Hệ thống ổn định"
    }
