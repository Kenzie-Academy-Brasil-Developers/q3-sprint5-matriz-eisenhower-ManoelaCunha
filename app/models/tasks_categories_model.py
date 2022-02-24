from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey

@dataclass
class TasksCategoriesModel(db.Model):
    task_id: int
    category_id: int
   
    __tablename__ = "tasks_categories"

    id = Column(Integer, primary_key=True)

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    task = relationship("TasksModel", back_populates="task_category", uselist=False)

    category = relationship("CategoriesModel", back_populates="task_category", uselist=False)
   