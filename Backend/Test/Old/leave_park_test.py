import sys
import os
sys.path.insert(0, os.path.abspath(
                    os.path.join('..', 'src')
                    ))

from log_park import *
from leave_park import *
from init_db import *
from utils import setup_db
import hashlib

from shapely.geometry import LineString
from geoalchemy2.shape import from_shape

import pytest


#This function tests the case where the user leaves his parking spot
#which is in the middle of the street and didn't have any cars adjacent to them

#From 3 entries in the spots table we should then have 1 entry after the user leaves
#and one entry in the ParkHistory table

def test_leave_middle():

    session, user, car = setup_db()

    street_start = (0, 0)
    street =  LineString([street_start, get_park_EP(street_start, 5, 0)])


    street = from_shape(street, srid = 4326)
    
    new_street = Spot(region= street)

    session.add(new_street)

    session.commit()

    log_parking(user.user_id, 
                     car.car_id,
                     (0, 1e-5), 0)
    
    
    leave_park(user.user_id, car.car_id)

    spots = session.query(Spot)

    spots = [spot for spot in spots]

    park_logs = session.query(ParkHistory)

    park_logs = [park_log for park_log in park_logs]

    parks = session.query(Park)

    parks = [park for park in parks]


    assert len(spots) == 1 and len(park_logs) == 1 and len(parks) == 0


#This function tests the case when the user leaves a parking 
#space when they are parked right between two cars
#Initially we should have 3 entries in our park table
#and then 2 after the car leaves and 3 entries in our spot table

def test_leave_btwn_cars():

    session, user_1, car = setup_db()

    street_start = (0, 0)
    street =  LineString([street_start, get_park_EP(street_start, 5, 0)])


    street = from_shape(street, srid = 4326)
    
    new_street = Spot(region= street)

    session.add(new_street)

    password = "password"

    #for this test case we will need to create 3 test users
    user_2 = User(username = "test01",
            password_hash = hashlib.sha256(password.encode()).digest(), 
            email = "test1@test.com")
    
    session.add(user_2)

    user_3 = User(username = "test02",
            password_hash = hashlib.sha256(password.encode()).digest(), 
            email = "test2@test.com")
    
    session.add(user_3)

    session.commit()


    log_parking(user_1.user_id, 
                     car.car_id,
                     (0, 0),0)
    
    log_parking(user_2.user_id, 
                     car.car_id,
                     (0, 0.0000179663056824*2),0)
    
    log_parking(user_3.user_id, 
                     car.car_id,
                     (0, 0.0000179663056824),0)
    

    leave_park(user_2.user_id,
               car.car_id)
    
    spots = session.query(Spot)
    spots = [spot for spot in spots]

    assert len(spots) == 3

    park_logs = session.query(ParkHistory)
    park_logs = [park_log for park_log in park_logs]
    
    assert len(park_logs) == 1

    parks = session.query(Park)
    parks = [park for park in parks]
    
    assert len(parks) == 2
    
    

    