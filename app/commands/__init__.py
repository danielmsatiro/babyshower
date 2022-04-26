from flask import Flask
from .categories_commands import categories_cli


def init_app(app: Flask):
    app.cli.add_command(categories_cli())
