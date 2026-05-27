from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.user_model import User
from app.schemas.user_schema import UserCreate

class CRUDUser(CRUDBase[User]):
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Truy vấn người dùng bằng Email bất đồng bộ"""
        result = await db.execute(select(self.model).where(self.model.email == email))
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate, hashed_password: str) -> User:
        """Tạo mới một người dùng vào Database"""
        db_obj = User(
            email=obj_in.email,
            password_hashed=hashed_password,
            is_activate=True
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

# Khởi tạo một thực thể dùng chung (Singleton) cho toàn ứng dụng
user_crud = CRUDUser(User)