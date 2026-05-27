from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.token_schema import Token
from app.services.auth_service import auth_service

router = APIRouter()

@router.post("", response_model=Token)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    # Ủy quyền toàn bộ logic xác thực và sinh Token cho auth_service
    return await auth_service.authenticate_user(db, form_data=form_data)