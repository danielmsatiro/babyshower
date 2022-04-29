import click
from app.configs.database import db
from app.models.cities_model import CityModel
from flask.cli import AppGroup


def cities_cli():
    city_group = AppGroup("cities", help="Create cities")

    @city_group.command("create")
    @click.argument("quantity")
    def create_cities(quantity):
        CityModel.create_all(quantity)

    return city_group
