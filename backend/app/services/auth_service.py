from pydantic_settings.sources.providers import secrets
from app.core.exceptions import InvalidOTPException
import json
import secrets

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from fastapi.security import OAuth2PasswordRequestForm

from app.crud.user_crud import user_crud
from app.core.security import verify_password, create_access_token
from app.core.exceptions import (
    InvalidLoginException,
    UserNotFoundException,
    EmailAlreadyExistsException,
    OTPExpiredException,
    OTPOverInputException
)

class AuthService:
    async def authenticate_user(self, db: AsyncSession, form_data: OAuth2PasswordRequestForm) -> dict:
        """Nghiệp vụ xác thực thông tin đăng nhập và cấp Token"""
        # 1. Tìm người dùng bằng Email thông qua CRUD
        user = await user_crud.get_by_email(db, email=form_data.username)

        # 2. Kiểm tra sự tồn tại, trạng thái kích hoạt và đối chiếu mật khẩu băm
        if not user or not user.is_activate or not await verify_password(form_data.password, user.password_hashed):
            raise InvalidLoginException()

        # 3. Khởi tạo mã Token (Access Token) cấp cho người dùng
        access_token = create_access_token(subject=user.id, is_developer=user.is_developer)
        return {
            "access_token": access_token, 
            "token_type": "bearer"
        }

    async def send_otp_email(self, email: str, reason: str, db: AsyncSession, redis: Redis):
        """Nghiệp vụ gửi mã OTP"""
        existed_user = await user_crud.get_by_email(db, email=email)

        if reason == "verify-email":
            if existed_user:
                raise EmailAlreadyExistsException()
        elif reason == "change-password":
            if not existed_user:
                raise UserNotFoundException()

        code = "".join(secrets.choice("0123456789") for _ in range(6))

        print(f"[OTP DEV ONLY] Mã OTP cho {email} với {reason} là: {code}")

        payload = json.dumps({"code": code, "attempts": 0})

        await redis.set(f"otp:{reason}:{email}", payload, ex=300)

        return {
            "status": "success",
            "message": f"OTP đã được gửi tới {email}"
        }


    async def verify_otp_email(self, email: str, reason: str, otp: str, redis: Redis):
        """Nghiệp vụ xác minh mã OTP"""
        redis_key = f"otp:{reason}:{email}"

        otp_data = await redis.get(redis_key)

        if not otp_data:
            raise OTPExpiredException()

        otp_data = json.loads(otp_data)

        if otp_data.get("attempts", 0) >= 5:
            await redis.delete(redis_key)
            raise OTPOverInputException()

        if otp_data["code"] != otp:
            otp_data["attempts"] = otp_data.get("attempts", 0) + 1
            remain = 5 - otp_data["attempts"]
            await redis.set(redis_key, json.dumps(otp_data), ex=300)
            raise InvalidOTPException(detail=f"Mã OTP không chính xác.\n Bạn còn {remain} lần thử.")

        verification_token = secrets.token_hex(16)

        await redis.set(f"verified-token:{reason}:{email}", verification_token, ex=300)
        await redis.delete(redis_key)

        return {
            "status": "success",
            "message": "OTP verified successfully",
            "verified_token": verification_token
        }


# Khởi tạo thực thể dùng chung
auth_service = AuthService()