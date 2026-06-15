from pydantic import BaseModel
from app.core.exceptions import ErrorDetail

class SystemInfoData(BaseModel):
    app_name: str
    version: str
    developer: str

class DevErrors:
    DATABASE_ERROR = ErrorDetail("DATABASE_ERROR", 503, "Mất kết nối với cơ sở dữ liệu.")
    REDIS_ERROR = ErrorDetail("REDIS_ERROR", 503, "Mất kết nối với Redis.")