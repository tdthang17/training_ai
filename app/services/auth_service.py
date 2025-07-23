from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.security import create_access_token
from app.core.config import settings

class AuthService:
    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[schemas.User]:
        user = crud.user.authenticate(db, username=username, password=password)
        if not user:
            return None
        if not crud.user.is_active(user):
            return None
        return user
    
    def create_access_token_for_user(self, user: schemas.User) -> str:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return access_token

auth_service = AuthService()