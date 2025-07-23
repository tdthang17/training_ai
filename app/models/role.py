from sqlalchemy import * 
from sqlalchemy.orm import declarative_base, relationship
from .base import BaseModel

class Role(BaseModel):
    __tablename__ = "roles"
    __table_args__ = {'extend_existing': True}

    name = Column(String(50), index=True, unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)

    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(name='{self.name}')>"
    

