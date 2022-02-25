from http import HTTPStatus
from flask import current_app, jsonify

from app.models.tasks_model import TasksModel
from app.models.categories_model import CategoriesModel
from app.models.tasks_categories_model import TasksCategoriesModel



def select_all():
    categories = CategoriesModel.query.all()
   

    return jsonify(categories), HTTPStatus.OK