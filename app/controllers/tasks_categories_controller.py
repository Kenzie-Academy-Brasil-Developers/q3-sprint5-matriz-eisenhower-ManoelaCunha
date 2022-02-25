from http import HTTPStatus

from flask import current_app, jsonify

from app.models.categories_model import CategoriesModel


def select_all():
    base_query = current_app.db.session.query(CategoriesModel)
    categories = base_query.all()

    return jsonify(categories), HTTPStatus.OK
