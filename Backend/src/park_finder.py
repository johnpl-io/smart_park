
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



def park_find(user_id: int, spot_id: int, location: tuple[float, float]):

    session = create_session()
    """
find a parking spot given a user and a specific location 
a spot must have been recently left and close to the user
    
    """ 

    #find closest points that have recently been left
    get_closest = (
    session.query(Spot.spot_id, ParkHistory.time_left, func.ST_Distance(Spot.location,WKTElement(f'POINT({location[0]} {location[1]})')))
    .join(ParkHistory, Spot.spot_id == ParkHistory.spot_id)
    .filter(ParkHistory.time_left >= datetime.now() - timedelta(days=10))
    .order_by(Spot.location.cast(Geometry).distance_centroid(WKTElement(f'POINT({location[0]} {location[1]})', srid=4326))
    
    ).limit(10)
    )


    return get_closest


    
    
#park_find(0, 0, [-59.1175, 100.6280])

