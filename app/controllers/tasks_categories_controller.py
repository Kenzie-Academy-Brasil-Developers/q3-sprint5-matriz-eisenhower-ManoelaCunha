from http import HTTPStatus

from flask import current_app, jsonify

from app.models.categories_model import CategoriesModel


def select_all():
    categories = CategoriesModel.query.all()
   

    return jsonify(categories), HTTPStatus.OK