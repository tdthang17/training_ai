from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Role])
def read_roles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_active_user)
):
    """
    Retrieve roles.
    """
    return crud.role.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Role)
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: schemas.RoleCreate,
    current_user: schemas.User = Depends(deps.get_current_superuser)
):
    """
    Create new role. Only superuser can create roles.
    """
    role = crud.role.get_by_name(db, name=role_in.name)
    if role:
        raise HTTPException(
            status_code=400,
            detail="The role with this name already exists in the system."
        )
    return crud.role.create(db, obj_in=role_in)

@router.get("/{role_id}", response_model=schemas.Role)
def read_role(
    role_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_active_user)
):
    """
    Get role by ID.
    """
    role = crud.role.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role