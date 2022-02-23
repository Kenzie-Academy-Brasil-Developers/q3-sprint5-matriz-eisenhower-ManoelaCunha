from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import String, Column, Integer

@dataclass
class EisenhowersModel(db.Model):
    id: int
    type: str
   
    __tablename__ = "eisenhowers"

    id = Column(Integer, primary_key=True)
    type = Column(String(100))
