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
from app.core.exceptions import InvalidLoginException
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
    credentials_exception = InvalidLoginException()

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id)
    except JWTError as e:
        logger.error(f"Lỗi kiểm tra JWT: {str(e)}")
        raise credentials_exception

    user = await user_crud.get(db, id=int(token_data.user_id))

    if user is None:
        raise credentials_exception

    return user