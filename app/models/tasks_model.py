from dataclasses import dataclass
from typing import List
from app.configs.database import db
from sqlalchemy.orm import relationship
from sqlalchemy import String, Column, Integer, ForeignKey

@dataclass
class TasksModel(db.Model):
    keys = ['id', 'name', 'description', 'duration']

    id: int
    name: str
    description: str
    duration: int
   
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
  
    eisenhower_id = Column(Integer, ForeignKey("eisenhowers.id"), nullable=False)

    eisenhower = relationship("EisenhowersModel", back_populates="task", uselist=False)

    @staticmethod
    def verify_classification(data):
     
        if data['importance'] == 1 and data['urgency'] == 1:
            type = 'Do It First'

        if data['importance'] == 1 and data['urgency'] == 2:
            type = 'Delegate It'

        if data['importance'] == 2 and data['urgency'] == 1:
            type = 'Schedule It'

        if data['importance'] == 2 and data['urgency'] == 2:
            type = 'Delete It'

        return type
        