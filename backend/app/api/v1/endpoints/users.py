from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import user_service
from app.api.deps import get_current_user
from app.models.user_model import User

router = APIRouter()

@router.post("", response_model=ApiResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Đăng ký người dùng mới"""
    user = await user_service.register_new_user(db, user_in=user_in)
    return ApiResponse(
        message="Đăng ký tài khoản thành công",
        data=user
    )


@router.get("/me", response_model=ApiResponse[UserResponse])
async def read_user_me(
    current_user: User = Depends(get_current_user)
):
    """Thông tin cá nhân"""
    return ApiResponse(
        message="Lấy thông tin cá nhân thành công",
        data=current_user
    )