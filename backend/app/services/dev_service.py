from app.core.logger import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.core.exceptions import (
    DisconnectedDatabaseException,
    DisconnectedRedisException,
)

class DeveloperService:
    async def check_health(self, db: AsyncSession, redis: Redis):
        """Nghiệp vụ kiểm tra sức khỏe của cơ sở dữ liệu"""
        try:
            await db.execute(text("SELECT 1"))
        except Exception as e:
            logger.error(f"Đã mất kết nối với PostgreSQL: {e}")
            raise DisconnectedDatabaseException()

        try:
            await redis.ping()
        except Exception as e:
            logger.error(f"Đã mất kết nối với Redis: {e}")
            raise DisconnectedRedisException()

        return {
            "status": "success",
            "message": "Mọi thứ kết nối ổn định"
        }
    

dev_service = DeveloperService()