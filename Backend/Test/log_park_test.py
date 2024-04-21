import sys
import os
sys.path.insert(0, os.path.abspath(
                    os.path.join('..', 'src')
                    ))

from log_park import *
from init_db import *

from shapely.geometry import LineString, MultiLineString
from geoalchemy2.shape import from_shape
from shapely import wkb
from shapely.ops import unary_union

from sqlalchemy.orm import  sessionmaker,  Session
from sqlalchemy import create_engine
from sqlalchemy import func

import math
import hashlib
import pytest
import time



engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/smart_park_db')
    
Session = sessionmaker(bind=engine)
session = Session()

password = "password"

#we create the test user
user = User(username = "test00",
            password_hash = hashlib.sha256(password.encode()).digest(), 
            email = "test@test.com")
    
session.add(user)
    
car = Car(len = 2)
    
session.add(car)



        

#This function tests the case when the user parks in the middle of a region that's available
#and registered in the database
#In the end we should have three spots and one entry in our park table


def test_park_middle_1():

    session.query(Spot).delete()
    session.query(Park).delete()

    session.commit()

    street_start = (0, 0)
    street =  LineString([street_start, get_park_EP(street_start, 100, 0)])


    street = from_shape(street, srid = 4326)
    
    new_street = Spot(region= street)

    session.add(new_street)

    session.commit()

    log_parking(user.user_id, 
                     car.car_id,
                     (0, 1e-5), 0)
    
    spots = session.query(Spot)

    spots = [spot for spot in spots]

    assert len(spots) == 3

    park = session.query(Park)

    park = [park for park in park]

    assert len(park) == 1

    session.commit()
    

#This function tests the case when the user parks in between two cars. 
#We should have three spots and one entry in our park table
def test_park_middle_2():

    session.query(Spot).delete()
    session.query(Park).delete()

    session.commit()

    street_start = (0, 0)
    street =  LineString([street_start, get_park_EP(street_start, 5, 0)])


    street = from_shape(street, srid = 4326)
    
    new_street = Spot(region= street)

    session.add(new_street)

    session.commit()
    log_parking(user.user_id, 
                     car.car_id,
                     (0, 0),0)
    
    log_parking(user.user_id, 
                     car.car_id,
                     (0, 0.0000179663056824*2),0)
    
    log_parking(user.user_id, 
                     car.car_id,
                     (0, 0.0000179663056824),0)
    
    spots = session.query(Spot)

    spots = [spot for spot in spots]

    assert len(spots) == 3

    park = session.query(Park)

    park = [park for park in park]

    assert len(park) == 3

    session.commit()

#This function tests the case where a car parks in a completely new location
#We should have one spot and one entry in our park table
def test_new_park():
    session.query(Spot).delete()
    session.query(Park).delete()
    session.commit()

    log_parking(user.user_id, 
                     car.car_id,
                     (0, 0),0)
    
    session.commit()
    
    spots = session.query(Spot)

    spots = [spot for spot in spots]

    assert len(spots) == 1

    park = session.query(Park)

    park = [park for park in park]

    assert len(park) == 1

