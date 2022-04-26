from flask_jwt_extended import jwt_required, get_jwt_identity


current_parent = get_jwt_identity()


def pick_parents():
   ...

def new_parents():
    ...

# @jwt_required()
def update_parents(parent_id):
    # current_parent.cpf == parent_id 
    ...

# @jwt_required()
def delete_parents(parent_id):
    ...

