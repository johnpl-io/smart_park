from init_db import *
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import create_engine, func, cast
from sqlalchemy.sql import exists
from utils import create_session


def get_cars(user_id):
    session = create_session()

    spot_alias = aliased(Spot)

    
    combined_query = (
    session.query(
        Car.car_id,
        Car.car_model,
        Car.car_img,
        spot_alias.location.ST_AsText().label('park_location')
    )
    .join(Owns, Owns.car_id == Car.car_id)
    .outerjoin(Park, (Park.car_id == Car.car_id) & (Park.user_id == Owns.user_id))
    .outerjoin(spot_alias, Park.spot_id == spot_alias.spot_id)
    .filter(Owns.user_id == user_id)
    )

    results = combined_query.all() 

    results = [dict(zip(["car_id", "model", "image_path", "location"], 
                        result)) for result in results]
    
    return results

def get_models():

    session = create_session()

    results = (session.query(Car.car_model)).all()
    
    return [result[0] for result in results]


def find_cars(search_term):
    session = create_session()

    results = (session.query(Car.car_id, Car.car_model, Car.car_img)
               .filter(Car.car_model.ilike(f'{search_term}%')))
    
    results = [dict(zip(["car_id", "model", "image_path"], 
                        result)) for result in results]
    
    return results

def register(user_id, car_id):
    session = create_session()

    new_ownership = Owns(user_id=user_id, car_id=car_id)

    session.add(new_ownership)

    session.commit()