from http import HTTPStatus

from flask import current_app, jsonify, request

from psycopg2.errors import UniqueViolation

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.models.categories_model import CategoriesModel
from app.models.eisenhowers_model import EisenhowersModel
from app.models.tasks_categories_model import TasksCategoriesModel
from app.models.tasks_model import TasksModel

from app.services.decorators import verify_values


@verify_values
def create():
    try:
        data = request.get_json()
        data['name'] = data.get('name').lower()
        data['description'] = data.get('description').lower()

        categories = data.pop('categories')

        task = TasksModel(**data)

        type_eisenhower = task.verify_classification()

        eisenhower = EisenhowersModel.query.filter_by(type=type_eisenhower).first()

        task.eisenhower_id = eisenhower.id
       
        for value in categories:  
            category = CategoriesModel.query.filter_by(name=value.lower()).first()
   
            if category == None: 
                new_data = dict(name=value.lower(), description="")

                new_category = CategoriesModel(**new_data)
                current_app.db.session.add(new_category)

                task.categories.append(new_category)
                current_app.db.session.add(task)
                current_app.db.session.commit()

            else:
                task.categories.append(category)
                current_app.db.session.add(task)
                current_app.db.session.commit()

        return jsonify(dict(
            id=task.id,
            name=task.name,
            description=task.description,
            duration=task.duration,
            classification=eisenhower.type,
            categories=[category.lower() for category in categories]
        )), HTTPStatus.CREATED

    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            return dict(msg="task already exists!"), HTTPStatus.CONFLICT


@verify_values
def update(id):
    try:
        data = request.get_json()
        
        base_query_categories: Query = (
            current_app.db.session.query(CategoriesModel.name)
            .select_from(TasksCategoriesModel)
            .join(CategoriesModel)
            .join(TasksModel)
            .filter(TasksModel.id == id)
        )
     
        categories = ["".join(category) for category in base_query_categories.all()]

        base_query_tasks = current_app.db.session.query(TasksModel)
        
        task = base_query_tasks.get(id)

        for key, value in data.items():
            if key == 'name' or key == 'description':
                value = value.lower()

            setattr(task, key, value)

        type_eisenhower = task.verify_classification()

        eisenhower = EisenhowersModel.query.filter_by(type=type_eisenhower).first()
    
        current_app.db.session.add(task)
        current_app.db.session.commit()

        return jsonify(dict(
            id=task.id,
            name=task.name, 
            description=task.description,
            duration=task.duration,
            classification=eisenhower.type,
            categories=categories
        )), HTTPStatus.OK
        
    except AttributeError:
        return dict(msg="task not found!"), HTTPStatus.NOT_FOUND


def delete(id):
    try:
        base_query = current_app.db.session.query(TasksModel)
                    
        category = base_query.get(id)

        current_app.db.session.delete(category)
        current_app.db.session.commit()

        return jsonify(category), HTTPStatus.NO_CONTENT
    
    except UnmappedInstanceError:
        return dict(msg="task not found!"), HTTPStatus.NOT_FOUND
