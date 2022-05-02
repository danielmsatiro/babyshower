from json import load
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, Boolean
from geoalchemy2.types import Geometry
from app.configs.database import db
from sqlalchemy.orm import Query, Session
from geoalchemy2 import func
from dataclasses import dataclass
from sqlalchemy.orm import relationship


@dataclass
class CityModel(db.Model):
    _tablename_ = "cities"

    point_id: int = Column(Integer, primary_key=True, autoincrement=True)
    codigo_ibge: int = Column(Integer)
    nome_municipio: str = Column(String)
    capital: str = Column(Boolean, default=False)
    codigo_uf: int = Column(Integer)
    uf: str = Column(String)
    estado: str = Column(String(30))
    longitude: float = Column(Float)
    latitude: float = Column(Float)
    geom: str = Column(Geometry("Point"))

    def get_cities_within_radius(self, radius=50000):
        session: Session = db.session
        query: Query = session.query(CityModel)
        cities = query.filter(
            func.ST_DistanceSphere(CityModel.geom, self.geom) < radius
        ).all()
        return cities

    @classmethod
    def create_all(cls):
        with open("app/commands/cities.json", "r") as json_file:
            database = load(json_file)
            for city in database:
                city: dict
                session: Session = db.session
                longitude = city["longitude"]
                latitude = city["latitude"]
                geo = "POINT({} {})".format(longitude, latitude)
                city.update({"geom": geo})
                city = CityModel(**city)
                session.add(city)
                session.commit()
