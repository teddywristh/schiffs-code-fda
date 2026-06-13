import json

from redis.asyncio import Redis
from app.core.exceptions import OTPNotVerifiedException


async def verify_action_token(email: str, reason: str, token: str, redis: Redis) -> None:
    """Hàm kiểm tra OTP đã được xác thực hay chưa"""
    token_key = f"verified-token:{reason}:{email}"

    token = await redis.get(token_key)

    if not token or token.decode("utf-8") != token:
        raise OTPNotVerifiedException(detail="Yêu cầu chưa được xác thực hoặc token đã hết hạn")

    await redis.delete(token_key)
