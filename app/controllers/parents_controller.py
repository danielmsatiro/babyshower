from copy import deepcopy
from http import HTTPStatus

from sqlalchemy.util.langhelpers import constructor_copy
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.parent_model import ParentModel
from sqlalchemy.orm import Session, Query
from app.configs.database import db

def pick_parents():

    # parent_serializer = [
    #     parent.__dict__
    #     for parent
    #     in parent
    # ]

    # [
    #     parent.pop('_sa_instance_state')
    #     for parent
    #     in parent_serializer
    # ]
    ...
    

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
def update_parents(parent_id):
    ...

# @jwt_required()
def delete_parents(parent_id):
    ...

