
from sqlalchemy import Boolean, Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

from config import Settings

Base = declarative_base()

class Task(Base):

    __tablename__ = 'task'

    id = Column(Integer, primary_key=True,autoincrement=True)
    push_id = Column(String(length=255))
    is_active = Column(Boolean, default=True)
    deadline = Column(DateTime)
    to_user = Column(String(length=255))
    task_details = Column(String(length=255))
    by_user = Column(String(length=255))

    def __init__(self,push_id=None, deadline=None, to_user=None, task_details=None, by_user=None):
        self.push_id = push_id
        self.deadline = deadline
        self.to_user = to_user
        self.task_details = task_details
        self.by_user = by_user


engine = create_engine(Settings.db_path, echo=True)
Base.metadata.create_all(bind=engine)