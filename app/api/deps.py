from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.core.security import decode_access_token
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")              # Decoding the token to get the username
    if username is None:
        raise credentials_exception
    
    user = crud.user.get_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    # return current_user

    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
