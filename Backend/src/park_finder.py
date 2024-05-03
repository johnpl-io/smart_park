
from init_db import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, cast
from geoalchemy2 import  Geography, Geometry
from geoalchemy2.functions import ST_X, ST_Y 
from utils import create_session
import random
import numpy as np
import matplotlib
from geoalchemy2.elements import WKTElement
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter
from io import BytesIO
import base64
from datetime import datetime, timedelta



def park_find(user_id: int, car_id: int, location: tuple[float, float])-> list[int, int , int, float, datetime]:

    session = create_session()
    """
find a parking spot given a user and a specific location 
a spot must have been recently left and close to the user
    Parameters:
    :user_id: user_id of indivual requesting a spot. 
    :car_id: the car_id of the user_id current car
    :location: location of area where spot is

    Returns:
    :return: A tuple representing the latitude and longitude of the endpoint of the line segment represented by the car.
    """ 

    #find closest points that have recently been left for now it simply picks ten closest poinst
    get_closest = (
    session.query(Spot.spot_id, func.ST_Y(cast(Spot.location, Geometry)), func.ST_X(cast(Spot.location, Geometry)), func.ST_Distance(Spot.location,WKTElement(f'POINT({location[0]} {location[1]})')),  ParkHistory.time_left)
    .join(ParkHistory, Spot.spot_id == ParkHistory.spot_id)
    .filter(ParkHistory.time_left >= datetime.now() - timedelta(days=10))
    .order_by(Spot.location.cast(Geometry).distance_centroid(WKTElement(f'POINT({location[0]} {location[1]})', srid=4326))
    
    ).limit(10)
    )

    return get_closest


    
    
#z = park_find(0, 0, [ -77.062089, 38.8938 ])
