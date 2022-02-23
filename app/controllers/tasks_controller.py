from http import HTTPStatus
from flask import request, current_app, jsonify

from app.models.tasks_model import TasksModel
from app.models.eisenhowers_model import EisenhowersModel

from sqlalchemy.exc import IntegrityError

from psycopg2.errors import UniqueViolation

from app.services.decorators import verify_values


@verify_values
def create():
    try:
        data = request.get_json()
        data['name'] = data.get('name').lower()
        data['description'] = data.get('description').lower()
  
        categories = data.pop('categories')
        categories = [categorie.lower() for categorie in categories]

        type_eisenhower = TasksModel.verify_classification(data)

        eisenhower = EisenhowersModel.query.filter_by(type=type_eisenhower).first()

        data['eisenhower_id'] = eisenhower.id
        
        task = TasksModel(**data)
 
        current_app.db.session.add(task)
        current_app.db.session.commit()

        return jsonify(dict(id=task.id, 
                    name=task.name, 
                    description=task.description, 
                    duration=task.duration,
                    classification=eisenhower.type,
                    categories=categories
                    )), HTTPStatus.CREATED

    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            return dict(msg="task already exists!"), HTTPStatus.CONFLICT
