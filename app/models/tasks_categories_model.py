from dataclasses import dataclass

from sqlalchemy import Column, ForeignKey, Integer

from app.configs.database import db


@dataclass
class TasksCategoriesModel(db.Model):
    task_id: int
    category_id: int
   
    __tablename__ = "tasks_categories"

    id = Column(Integer, primary_key=True)

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
   