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

    def get_cities_within_radius(self, radius):
        session: Session = db.session
        query: Query = session.query(CityModel)
        cities = query.filter(
            func.ST_DistanceSphere(CityModel.geom, self.geom) < radius
        ).all()
        return cities

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
                print(type(city.geom))
                print((city.geom))
                print((city))
                # break
                session.add(city)
                session.commit()
