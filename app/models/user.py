from sqlalchemy import * 
from sqlalchemy.orm import declarative_base, relationship
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(50), unique=True, nullable=False, index=True)
    fullname = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_update = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))


    role = relationship("Role", back_populates="users")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
    

    