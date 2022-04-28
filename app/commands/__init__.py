from flask import Flask

from .answers_commands import answers_cli
from .categories_commands import categories_cli
from .parents_commands import parents_cli
from .products_commands import products_cli
from .questions_commands import questions_cli


def init_app(app: Flask):
    app.cli.add_command(categories_cli())
    app.cli.add_command(parents_cli())
    app.cli.add_command(questions_cli())
    app.cli.add_command(products_cli())
    app.cli.add_command(answers_cli())
