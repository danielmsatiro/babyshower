from json import load
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, Boolean
from geoalchemy2.types import Geometry
from app.configs.database import db


class CityModel(db.Model):
    _tablename_ = "cities"

    point_id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_ibge = Column(Integer)
    nome_municipio = Column(String)
    capital = Column(Boolean, default=False)
    codigo_uf = Column(Integer)
    uf = Column(String)
    estado = Column(String(30))
    longitude = Column(Float)
    latitude = Column(Float)
    geom = Column(Geometry('Point'))

    @classmethod
    def get_cities_within_radius(cls, city):
        return f"""Return all cities within radius of {city} and {cls.geo}."""

    @classmethod
    def create_all(cls, limite):
        with open("app/commands/cities.json", "r") as json_file:
            database = load(json_file)
            for x in range(int(limite)):
                data: dict = database[x]
                session: Session = db.session
                longitude = data["longitude"]
                latitude = data["latitude"]
                geo = "POINT({} {})".format(longitude, latitude)
                data.update({"geom": geo})
                city = CityModel(**data)
                session.add(city)
                session.commit()
