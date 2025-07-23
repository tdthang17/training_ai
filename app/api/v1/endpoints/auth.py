from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas
from app.api import deps
from app.services.auth_service import auth_service
from app.models.token_blacklist import TokenBlacklist
from app.database import get_db
router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token_for_user(user)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.User)
def read_users_me(
    current_user: schemas.User = Depends(deps.get_current_active_user)
):
    """
    Get current user
    """
    return current_user


@router.post("/logout")
def logout(token: str = Depends(deps.oauth2_scheme),
           db: Session = Depends(deps.get_db)):
    """
    Logout user by blacklisting the token
    """
    db.add(TokenBlacklist(token=token))
    db.commit()
    return {"message": "Successfully logged out"}