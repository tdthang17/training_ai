from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas

class UserService:
    def create_user(self, db: Session, user_in: schemas.UserCreate) -> schemas.User:
        # Check if user already exists
        user = crud.user.get_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system."
            )
        
        user = crud.user.get_by_username(db, username=user_in.username)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this username already exists in the system."
            )
        
        # Validate role if provided
        if user_in.role_id:
            role = crud.role.get(db, id=user_in.role_id)
            if not role:
                raise HTTPException(
                    status_code=400,
                    detail="The specified role does not exist."
                )
        
        user = crud.user.create(db, obj_in=user_in)
        return user
    
    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[schemas.User]:
        return crud.user.get_multi(db, skip=skip, limit=limit)
    
    def get_user(self, db: Session, user_id: int) -> Optional[schemas.User]:
        return crud.user.get(db, id=user_id)
    
    def update_user(self, db: Session, user_id: int, user_in: schemas.UserUpdate) -> schemas.User:
        user = crud.user.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        # Check email uniqueness if being updated
        if user_in.email and user_in.email != user.email:
            existing_user = crud.user.get_by_email(db, email=user_in.email)
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )
        
        # Check username uniqueness if being updated
        if user_in.username and user_in.username != user.username:
            existing_user = crud.user.get_by_username(db, username=user_in.username)
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="Username already taken"
                )
        
        return crud.user.update(db, db_obj=user, obj_in=user_in)
    
    def delete_user(self, db: Session, user_id: int) -> schemas.User:
        user = crud.user.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return crud.user.remove(db, id=user_id)

user_service = UserService()
