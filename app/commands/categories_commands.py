from app.configs.database import db
from app.models.category_model import CategoryModel
from flask.cli import AppGroup
from sqlalchemy.orm.session import Session


def categories_cli():
    category_group = AppGroup("categories", help="Create categories")

    categories_names_list = [
        "0 a 3 meses",
        "4 a 6 meses",
        "7 a 9 meses",
        "10 meses a 1 ano",
        "2 anos",
        "3 a 5 anos",
        "carrinhos",
        "roupas",
        "quarto do bebê",
        "cadeiras",
        "maternidade",
        "banho de bebê",
        "brinquedos",
        "lactação",
        "segurança para bebê",
        "saúde para bebê",
    ]

    categories_description_list = [
        "Tudo o que o seu bebê precisa dos 0 a 3 meses",
        "Tudo o que o seu bebê precisa dos 4 a 6 meses",
        "Tudo o que o seu bebê precisa dos 7 a 9 meses",
        "Tudo o que o seu bebê precisa dos 10 meses a 1 ano de idade",
        "Tudo o que o seu bebê precisa para os 2 anos de idade",
        "Tudo o que o seu bebê precisa de 3 a 5 anos de idade",
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
                    description=categories_description_list[x],
                )
            )

        session.add_all(categories)
        session.commit()

    return category_group
