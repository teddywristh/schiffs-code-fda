from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    nickname: str
    password: str

class UserResponse(UserBase):
    id: int
    nickname: str
    is_active: Optional[bool] = True
    is_developer: Optional[bool] = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True