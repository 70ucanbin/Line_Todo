from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Task(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key=True, index=True)
    time_limit = Column(DateTime)
    to_user = Column(String)
    details = Column(String)
    by_user = Column(String)

    # def __init__(self, id=None, time_limit=None, to_user=None, by_user=None):
    #     self.id = id
    #     self.time_limit = time_limit
    #     self.to_user = to_user
    #     self.by_user = by_user

    def __repr__(self):
        return '<Task id:{} to_user:{} by_user:{}>'.format(
            self.id, 
            self.to_user, 
            self.by_user
        )