from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class RoleInDB(RoleBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Role(RoleInDB):
    pass