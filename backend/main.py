from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logger import logger
from app.core.database import get_db
from fastapi import Depends

from app.core.config import settings
from app.core.exceptions import DisconnectedDatabaseException
from app.core.exceptions import CustomAppException, global_app_exception_handler

from app.api.v1.api import api_router

app = FastAPI(title=settings.PROJECT_NAME,
              version="1.0.0")

app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_exception_handler(CustomAppException, global_app_exception_handler)

@app.get("/", tags=["Root"])
def read_root():
    return {"success": "Welcome to Schiffs Code FDA API!"}

@app.get("/health", tags=["Health"])
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    API Health Check kiểm tra kết nối Database bất đồng bộ toàn diện
    """
    try:
        await db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Lỗi kết nối tới Database: {str(e)}")
        raise DisconnectedDatabaseException()