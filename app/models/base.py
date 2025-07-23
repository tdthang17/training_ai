from sqlalchemy import *
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, index=True, primary_key=True)
    create_at = Column(DateTime, default=func.now())
    update_at = Column(DateTime, default=func.now(), onupdate=func.now())