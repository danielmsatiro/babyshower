from copy import deepcopy
from http import HTTPStatus

from sqlalchemy.util.langhelpers import constructor_copy
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.parent_model import ParentModel
from sqlalchemy.orm import Session, Query
from app.configs.database import db

def pick_parents():
    response: Query = db.session.query(ParentModel)
    response = response.all()
    return jsonify(response), HTTPStatus.OK
    

def new_parents():
  
    data: dict = request.get_json()
    
    parent = ParentModel(**data)
    
    # parent_serializer = deepcopy(parent)
    session: Session = db.session
    
    session.add(parent)
    # parent.id = parent.cpf
    session.commit()
    print(parent)
    # parent_serializer.pop('_sa_instance_state')
    
    return jsonify(parent), HTTPStatus.CREATED 
    

# @jwt_required()
def update_parents(parent_cpf):
    data: dict = request.get_json()
    session: Session = db.session

    parent: Query = session.query(ParentModel)
    parent = parent.filter_by(cpf=parent_cpf).first()

    for key, value in data.items():
        setattr(parent, key, value)

    session.add(parent)

    session.commit()

    return jsonify(parent)

# @jwt_required()
def delete_parents(parent_cpf):
    session: Session = db.session
    base_query: Query = session.query(ParentModel)

    parent = base_query.filter_by(cpf=parent_cpf).first()

    session.delete(parent)
    session.commit()

    return "", HTTPStatus.NO_CONTENT