import sys
import os
sys.path.insert(0, os.path.abspath(
                    os.path.join('..', 'src')
                    ))

from log_park import *
from leave_park import *
from init_db import *
from utils import setup_db

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

    print(parks)

    assert len(spots) == 1 and len(park_logs) == 1 and len(parks) == 0


    