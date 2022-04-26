from flask.cli import AppGroup
from app.configs.database import db
from app.models.category_model import CategoryModel
from sqlalchemy.orm.session import Session


def categories_cli():
    category_group = AppGroup("categories", help="Create categories")

    categories_names_list = [
        "até 3 meses", "até 6 meses", "até 9 meses", "até 1 ano", "até 2 anos",
        "de 3 a 5 anos", "carrinhos", "roupas", "quarto do bebê", "cadeiras",
        "maternidade", "banho de bebê", "brinquedos",
        "lactação", "segurança para bebê", "saúde para bebê"]

    categories_description_list = [
        "Tudo o que o seu bebê precisa até os seus 3 meses",
        "Tudo o que o seu bebê precisa até os seus 6 meses",
        "Tudo o que o seu bebê precisa até os seus 9 meses",
        "Tudo o que o seu bebê precisa até os seus 1 ano de idade",
        "Tudo o que o seu bebê precisa até os seus 2 anos de idade",
        "Tudo o que o seu bebê precisa de 3 a 5 anos",
        "Carrinhos para o seu bebê",
        "Roupas para o seu bebê",
        "Acessórios para o quarto do seu bebê",
        "Cadeiras de sol, de carro etc. para ser usada pelo bebê",
        "Acessórios para a maternidade",
        "Acessórios para o banho de bebê do seu bebê",
        "Brinquedos para o seu bebê",
        "Acessórios para alimentação e amamentação",
        "Acessórios para a segurança do bebê",
        "Acessórios para a saúde do bebê",
    ]

    @category_group.command("create")
    def create_categories():
        session: Session = db.session
        categories = []

        for x in range(len(categories_names_list)):
            categories.append(
                CategoryModel(
                    name=categories_names_list[x],
                    description=categories_description_list[x]
                    ))

        session.add_all(categories)
        session.commit()

    return category_group
