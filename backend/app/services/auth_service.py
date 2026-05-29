from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.crud.user_crud import user_crud
from app.core.security import verify_password, create_access_token
from app.core.exceptions import InvalidLoginException

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

# Khởi tạo thực thể dùng chung
auth_service = AuthService()