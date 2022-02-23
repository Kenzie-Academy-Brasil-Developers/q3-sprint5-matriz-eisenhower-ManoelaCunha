from flask import Blueprint
from app.controllers import tasks_controller

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

bp.post("")(tasks_controller.create)
