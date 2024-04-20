import sys
import os
sys.path.insert(0, os.path.abspath(
                    os.path.join('..', 'src')
                    ))
from log_park import *
from init_db import *
from shapely.geometry import Polygon, LineString
from geoalchemy2.shape import from_shape
import hashlib

import pytest



engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/smart_park_db')
Session = sessionmaker(bind=engine)
session = Session()

def test_park_middle():

    password = "password"
    user = User(username = "test00",
                password_hash = hashlib.sha256(password.encode()).digest(), 
                email = "test@test.com")
    
    session.add(user)
    
    car = Car(len = 2)
    
    session.add(car)

    street_start = (0, 0)
    street =  LineString(get_region(street_start, 5))

    print(street)

    street = from_shape(street, srid = 4326)
    

    new_street = Spot(region= street)

    session.add(new_street)

    session.commit()
    

    log_user_parking(user.user_id, 
                     car.car_id,
                     (1e-5, 0))
    
    spots = session.query(Spot)

    spots = [spot for spot in spots]

    assert len(spots) == 3

    



    




    

    

