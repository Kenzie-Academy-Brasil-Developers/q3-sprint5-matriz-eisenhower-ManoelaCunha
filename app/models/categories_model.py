from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import String, Column, Integer

@dataclass
class CategoriesModel(db.Model):
    id: int
    name: str
    description: str
   
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String)

    def __init__(self, **kwargs) -> None:
        self.name = kwargs['name'].lower()
        self.description = kwargs['description'].lower()
