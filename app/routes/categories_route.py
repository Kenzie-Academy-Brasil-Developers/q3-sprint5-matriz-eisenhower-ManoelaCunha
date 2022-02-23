from nis import cat
from flask import Blueprint
from app.controllers import categories_controller

bp = Blueprint("categories", __name__, url_prefix="/categories")

bp.post("")(categories_controller.create)

bp.patch("/<int:id>")(categories_controller.update)

bp.delete("/<int:id>")(categories_controller.delete)
