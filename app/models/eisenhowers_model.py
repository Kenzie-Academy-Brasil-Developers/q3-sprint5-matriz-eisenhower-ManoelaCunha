from dataclasses import dataclass

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.configs.database import db


@dataclass
class EisenhowersModel(db.Model):
    id: int
    type: str
   
    __tablename__ = "eisenhowers"

    id = Column(Integer, primary_key=True)
    type = Column(String(100))

    task = relationship("TasksModel", back_populates="eisenhower", uselist=True)
    