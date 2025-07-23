from sqlalchemy import Column, Integer, String, DateTime
from .base import BaseModel
from datetime import datetime


class TokenBlacklist(BaseModel):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<TokenBlacklist(token='{self.token}')>"