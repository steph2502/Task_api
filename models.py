from sqlalchemy import Column,String,Integer,Boolean
from database import Base

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer,primary_key=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)