from http import HTTPStatus

from app.configs.database import db
from app.models.cities_model import CityModel
from flask import request
from ipdb import set_trace
from sqlalchemy import desc, true
from sqlalchemy.orm import Query, Session


def retrieve():
    session: Session = db.session
    response: Query = session.query(CityModel).all()
    params = dict(request.args.to_dict().items())

    page = int(params.get("page", 1)) - 1
    per_page = int(params.get("per_page", 8))

    if params.get("city") and params.get("state"):
        response: Query = (
            session.query(CityModel)
            .filter(CityModel.city.ilike(f"%{params.get('city')}%"))
            .filter(CityModel.state.ilike(f"%{params.get('state')}%"))
            .all()
        )
    elif params.get("city"):
        response: Query = (
            session.query(CityModel)
            .filter(CityModel.city.ilike(f"%{params.get('city')}%"))
            .offset(page * per_page)
            .limit(per_page)
            .all()
        )
    elif params.get("state"):
        response: Query = (
            session.query(CityModel)
            .filter(CityModel.state.ilike(f"%{params.get('state')}%"))
            .order_by(desc(CityModel.capital))
            .offset(page * per_page)
            .limit(per_page)
            .all()
        )
    cities = []
    for city in response:
        city = city.__dict__
        city.pop("_sa_instance_state")
        city.pop("geom")
        cities.append(city)

    return {"cities": cities}, HTTPStatus.OK
