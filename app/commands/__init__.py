from flask import Flask

from .categories_commands import categories_cli
from .parents_commands import parents_cli
from .products_commands import products_cli
from .questions_commands import questions_cli
from .cities_commands import cities_cli

categories_names_list = [
    "Bebê conforto para bebês de 3 meses",
    "Bebê conforto para bebês de 6 meses",
    "Bebê conforto para bebês de 9 meses",
    "Bebê conforto para bebês de 1 ano",
    "Bebê conforto para bebês de 2 anos",
    "Bebê conforto para crianças de 3 a 5 anos",
    "carrinhos",
    "roupas",
    "acessórios",
    "mamães",
    "roupa de banho para bebê",
    "brinquedos",
    "lactação",
    "segurança",
    "saúde",
]


def init_app(app: Flask):
    app.cli.add_command(categories_cli())
    app.cli.add_command(parents_cli())
    app.cli.add_command(questions_cli())
    app.cli.add_command(products_cli())
    app.cli.add_command(cities_cli())