import json

from redis.asyncio import Redis
from app.core.exceptions import OTPExpiredException, OTPNotVerifiedException


async def verify_otp(redis: Redis, key: str) -> None:
    """Hàm kiểm tra OTP đã được xác thực hay chưa"""
    verify_result = await redis.get(key)

    if not verify_result:
        raise OTPExpiredException()

    verify_result = json.loads(verify_result)

    if not verify_result.get("verified", False):
        raise OTPNotVerifiedException()

    await redis.delete(key)

