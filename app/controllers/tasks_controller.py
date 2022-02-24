from http import HTTPStatus
from flask import request, current_app, jsonify

from app.models.tasks_model import TasksModel
from app.models.eisenhowers_model import EisenhowersModel

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

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

        task = TasksModel(**data)

        type_eisenhower = task.verify_classification()

        eisenhower = EisenhowersModel.query.filter_by(type=type_eisenhower).first()

        task.eisenhower_id = eisenhower.id
     
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


def update(id):
    try:
        data = request.get_json()

        name = [value.lower() for key, value in data.items() if key == 'name']
        if name:
            data['name'] = name[0]
        
        base_query = current_app.db.session.query(TasksModel)
 
        task = base_query.get(id)

        for key, value in data.items():
            setattr(task, key, value)

        type_eisenhower = task.verify_classification()

        eisenhower = EisenhowersModel.query.filter_by(type=type_eisenhower).first()

        task.eisenhower_id = eisenhower.id

        current_app.db.session.add(task)
        current_app.db.session.commit()

        return jsonify(
            dict(id=task.id, 
                    name=task.name, 
                    description=task.description, 
                    duration=task.duration,
                    classification=eisenhower.type
                    #categories=
                    )), HTTPStatus.OK

    except AttributeError:
        return dict(msg="task not found!"), HTTPStatus.NOT_FOUND
    
    except UnboundLocalError:
        return dict(msg="Invalid value!"), HTTPStatus.BAD_REQUEST


def delete(id):
    try:
        base_query = current_app.db.session.query(TasksModel)
                    
        category = base_query.get(id)

        current_app.db.session.delete(category)
        current_app.db.session.commit()

        return jsonify(category), HTTPStatus.NO_CONTENT
    
    except UnmappedInstanceError:
        return dict(msg="task not found!"), HTTPStatus.NOT_FOUND
