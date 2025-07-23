from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from .role import Role

class UserBase(BaseModel):
    email: EmailStr
    username: str
    fullname: str
    is_active: bool = True
    is_superuser: bool = False
    role_id: Optional[int] = None

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    fullname: str
    password: str
    role_id: Optional[int] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    fullname: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    role_id: Optional[int] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class User(UserInDB):
    role: Optional[Role] = None