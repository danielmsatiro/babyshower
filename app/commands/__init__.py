from flask import Flask

from .categories_commands import categories_cli
from .parents_commands import parents_cli


def init_app(app: Flask):
    app.cli.add_command(categories_cli())
    app.cli.add_command(parents_cli())
