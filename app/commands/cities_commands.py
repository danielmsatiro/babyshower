import click
from app.configs.database import db
from app.models.cities_model import CityModel
from flask.cli import AppGroup


def cities_cli():
    city_group = AppGroup("cities", help="Create cities")

    @city_group.command("create")
    def create_cities():
        CityModel.create_all()

    return city_group
