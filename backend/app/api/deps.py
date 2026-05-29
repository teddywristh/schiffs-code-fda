from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.user_model import User
from app.schemas.token_schema import TokenData
from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import InvalidLoginException, NotDeveloperException
from app.crud.user_crud import user_crud

secret_key=settings.SECRET_KEY
algorithm=settings.ALGORITHM

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth_scheme)
) -> User:
    """
    Hàm xác thực danh tính của user qua token
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise InvalidLoginException()

        token_data = TokenData(user_id=user_id)
    except JWTError as e:
        logger.error(f"Lỗi kiểm tra JWT: {str(e)}")
        raise InvalidLoginException()

    user = await user_crud.get(db, id=int(token_data.user_id))

    if user is None:
        raise InvalidLoginException()

    return user

async def get_current_developer(
        current_user: User = Depends(get_current_user)
) -> User:
    """
    Hàm xác thực danh tính của developer qua token
    """
    if not current_user.is_developer:
        raise NotDeveloperException()
    return current_user