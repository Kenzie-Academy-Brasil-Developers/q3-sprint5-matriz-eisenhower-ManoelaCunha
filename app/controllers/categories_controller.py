from http import HTTPStatus

from flask import current_app, jsonify, request
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

from app.models.categories_model import CategoriesModel


def create():
    try:
        data = request.get_json()
            
        category = CategoriesModel(**data)

        current_app.db.session.add(category)
        current_app.db.session.commit()
     
        return jsonify(category), HTTPStatus.CREATED

    except KeyError as e:
        return dict(error=f"Missing key '{e.args[0]}'"), HTTPStatus.BAD_REQUEST

    except AttributeError:
        return dict(msg="The value must be a string!"), HTTPStatus.BAD_REQUEST

    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            return dict(msg="category already exists!"), HTTPStatus.CONFLICT

def update(id):
    try:
        data = request.get_json()

        base_query = current_app.db.session.query(CategoriesModel)
        
        category = base_query.get(id)
  
        for key, value in data.items():
            setattr(category, key, value.lower())
        
        current_app.db.session.add(category)
        current_app.db.session.commit()

        return jsonify(dict(
            id=category.id,
            name=category.name,
            description=category.description
        )), HTTPStatus.OK

    except AttributeError:
        return dict(msg="category not found!"), HTTPStatus.NOT_FOUND

def delete(id):  
    try:
        base_query = current_app.db.session.query(CategoriesModel)
                    
        category = base_query.get(id)

        current_app.db.session.delete(category)
        current_app.db.session.commit()

        return jsonify(category), HTTPStatus.NO_CONTENT
    
    except UnmappedInstanceError:
        return dict(msg="category not found!"), HTTPStatus.NOT_FOUND
