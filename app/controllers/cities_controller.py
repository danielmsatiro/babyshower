from flask import request
from ipdb import set_trace
from http import HTTPStatus

from sqlalchemy import desc, true
from app.configs.database import db
from sqlalchemy.orm import Query, Session
from app.models.cities_model import CityModel


def retrieve():
    session: Session = db.session
    response: Query = session.query(CityModel).all()
    params = dict(request.args.to_dict().items())

    page = int(params.get("page", 1)) - 1
    per_page = int(params.get("per_page", 8))

    if params.get("city") and params.get("state"):
        response: Query = (
            session.query(CityModel)
            .filter_by(city=params.get("city"))
            .filter_by(state=params.get("state"))
            .all()
        )
    elif params.get("city"):
        response: Query = (
            session.query(CityModel)
            .filter_by(city=params.get("city"))
            .offset(page * per_page)
            .limit(per_page)
            .all()
        )
    elif params.get("state"):
        response: Query = (
            session.query(CityModel)
            .filter_by(state=params.get("state"))
            .order_by(desc(CityModel.capital))
            .offset(page * per_page)
            .limit(per_page)
            .all()
        )
    cities = []
    for city in response:
        city: CityModel
        city = {
            "code_ibge": city.code_ibge,
            "city": city.city,
            "capital": city.capital,
            "code_uf": city.code_uf,
            "uf": city.uf,
            "state": city.state,
            "latitude": city.latitude,
            "longitude": city.longitude,
        }
        cities.append(city)
    return {"cities": cities}, HTTPStatus.OK
