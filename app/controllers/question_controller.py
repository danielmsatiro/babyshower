def get_product_questions(product_id: int):
    return {"msg": "Rota GET perguntas do produto"}

def create_question(product_id: int):
    return {"msg": "Rota POST perguntas do produto"}

def update_question(question_id: int):
    return {"msg": "Rota PATCH perguntas do produto"}

def delete_question(question_id: int):
    return {"msg": "Rota DEL perguntas do produto"}