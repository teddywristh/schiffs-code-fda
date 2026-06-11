# Hướng dẫn sử dụng & Kết quả tích hợp Redis

Chúng ta đã tích hợp thành công Redis vào dự án! 

## Các thay đổi đã thực hiện

1. **Docker & Môi trường**:
   - Thêm dịch vụ `redis` sử dụng image `redis:7-alpine` vào [docker-compose.yml](file:///c:/Users/YOGA/Desktop/MyProjects/Schiffs-Code-Fda/schiffs-code-fda/docker-compose.yml).
   - Bổ sung cấu hình cổng và kết nối Redis vào [.env](file:///c:/Users/YOGA/Desktop/MyProjects/Schiffs-Code-Fda/schiffs-code-fda/.env) và [.env.example](file:///c:/Users/YOGA/Desktop/MyProjects/Schiffs-Code-Fda/schiffs-code-fda/.env.example).
   - Thêm thư viện `redis` (hỗ trợ async) vào [requirements.txt](file:///c:/Users/YOGA/Desktop/MyProjects/Schiffs-Code-Fda/schiffs-code-fda/backend/requirements.txt).
2. **Backend**:
   - Cấu hình các biến môi trường Redis qua `Settings` trong [config.py](file:///c:/Users/YOGA/Desktop/MyProjects/Schiffs-Code-Fda/schiffs-code-fda/backend/app/core/config.py).
   - Tạo mới file [redis.py](file:///c:/Users/YOGA/Desktop/MyProjects/Schiffs-Code-Fda/schiffs-code-fda/backend/app/core/redis.py) chứa class `RedisClient` quản lý connection pool và dependency `get_redis`.
   - Kết nối Redis khi server khởi chạy và đóng kết nối khi server tắt trong lifespan của [main.py](file:///c:/Users/YOGA/Desktop/MyProjects/Schiffs-Code-Fda/schiffs-code-fda/backend/main.py).
   - Tích hợp ping kiểm tra sức khỏe Redis vào API `/health`.

---

## Hướng dẫn sử dụng Redis trong Backend

Bạn có thể dễ dàng sử dụng Redis trong các endpoint của FastAPI bằng cách sử dụng `Depends(get_redis)`. Dưới đây là ví dụ minh họa cách viết API để lưu và lấy dữ liệu từ Redis cache:

### 1. Tạo Router ví dụ (hoặc tích hợp vào router có sẵn)

```python
from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis
from app.core.redis import get_redis

router = APIRouter()

@router.post("/cache-test")
async def set_cache(key: str, value: str, redis: Redis = Depends(get_redis)):
    # Lưu giá trị với thời gian hết hạn là 60 giây (TTL = 60)
    await redis.set(key, value, ex=60)
    return {"message": f"Đã lưu key '{key}' vào Redis thành công."}

@router.get("/cache-test/{key}")
async def get_cache(key: str, redis: Redis = Depends(get_redis)):
    value = await redis.get(key)
    if not value:
        raise HTTPException(status_code=404, detail="Key không tồn tại hoặc đã hết hạn")
    return {"key": key, "value": value}
```

### 2. Các hàm thông dụng với `redis.asyncio`
- `await redis.get(key)`: Lấy dữ liệu dạng string.
- `await redis.set(key, value, ex=seconds)`: Ghi dữ liệu kèm theo thời hạn hết hạn (TTL).
- `await redis.delete(key)`: Xóa key khỏi Redis.
- `await redis.exists(key)`: Kiểm tra xem key có tồn tại hay không.
- `await redis.incr(key)`: Tăng giá trị của key lên 1 đơn vị (hữu ích cho rate limiting hoặc lượt view).

---

## Kết quả kiểm tra sức khỏe hệ thống (Health Check)

Gọi endpoint `/health` từ API đã trả về thông tin kết nối thành công tới cả PostgreSQL và Redis:

```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected"
}
```