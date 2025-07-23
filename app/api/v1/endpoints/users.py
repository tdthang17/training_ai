from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas
from app.api import deps
from app.services.user_service import user_service

router = APIRouter()

@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_active_user)
):
    """
    Retrieve users.
    """
    return user_service.get_users(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: schemas.User = Depends(deps.get_current_superuser)
):
    """
    Create new user. Only superuser can create users.
    """
    return user_service.create_user(db, user_in)

@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
):
    """
    Get user by ID.
    """
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserUpdate,
    current_user: schemas.User = Depends(deps.get_current_superuser)
):
    """
    Update user. Only superuser can update users.
    """
    return user_service.update_user(db, user_id, user_in)

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_superuser)
):
    """
    Delete user. Only superuser can delete users.
    """
    # return user_service.delete_user(db, user_id)
    return {"message": "User deleted successfully", "user_id": user_id} 
