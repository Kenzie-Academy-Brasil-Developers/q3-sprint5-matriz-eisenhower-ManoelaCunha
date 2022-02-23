from flask import Flask
from environs import Env
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

env = Env()
env.read_env()

def init_app(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = env("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    db.init_app(app)
    app.db = db

    from app.models.categories_model import CategoriesModel
    from app.models.tasks_model import TasksModel
    from app.models.eisenhowers_model import EisenhowersModel
