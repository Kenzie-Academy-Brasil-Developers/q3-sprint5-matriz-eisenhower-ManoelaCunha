from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy.orm import relationship
from sqlalchemy import String, Column, Integer, ForeignKey

@dataclass
class TasksModel(db.Model):
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
   
    def verify_classification(self):
        if self.importance == 1 and self.urgency == 1:
            type = 'Do It First'

        if self.importance == 1 and self.urgency == 2:
            type = 'Delegate It'

        if self.importance == 2 and self.urgency == 1:
            type = 'Schedule It'

        if self.importance == 2 and self.urgency == 2:
            type = 'Delete It'

        return type
        