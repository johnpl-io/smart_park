from init_db import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from geoalchemy2 import  Geography
from utils import create_session



def log_park(user_id: int, car_id: int, location: tuple[float, float]):

    session = create_session()

    new_spot = Spot(location = func.ST_Point(location[0], location[1], type_ = Geography))

    session.add(new_spot)

    session.commit()

    new_park = Park(spot_id =new_spot.spot_id, 
                    user_id = user_id,
                    car_id = car_id)
    
    session.add(new_park)
    session.commit()


def leave_park(user_id: int, car_id: int):

    session = create_session()

    park = (session.query(Park)
                 .filter(Park.user_id == user_id, Park.car_id == car_id)
                 .limit(1)
                 .one_or_none())
    

    park_log = ParkHistory(user_id = user_id,
                              spot_id = park.spot_id,
                              time_arrived = park.time_arrived)
    

    session.add(park_log)

    session.delete(park)

    session.commit()
