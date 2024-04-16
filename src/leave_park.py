from init_db import *
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from geoalchemy2.shape import from_shape

from shapely.geometry import LineString
from shapely import wkb
import math
from shapely.ops import unary_union

#user leaves parking region, we find all regions within a certain distance of the parking region
#(does it check from the center of the line or edge has to be center). If dist(region - park_len) - park_len/2 < epsilon
#and region is free (not in park table) we merge, delete park region spot id and from park table adjust region to be
#region union park region


MIN_PARKING_SPACE = -1


def leave_park(user_id: int, car_id: int):
    engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/smart_park_db')
    Session = sessionmaker(bind=engine)
    session = Session()

    spot_id = session.query(Park.spot_id).filter(User.user_id == user_id and Car.car_id == car_id).first()

    obj = session.query(Spot).filter(Spot.spot_id == spot_id)

    parked_region = obj.region
    session.delete(obj)

    #now search for regions within certain distance of parking region

    merge_spots = session.query(Spot).filter(func.ST_DWithin(Spot.region, parked_region, MIN_PARKING_SPACE).all())


    #at most there should be two regions here
    
    if merge_spots:

        merge_region =unary_union( [region.region for region in merge_spots] + [parked_region])

        if len(merge_spots) == 2:
            session.delete(merge_spots[1])
        
        merge_spots[0].region = merge_region

    session.commit()