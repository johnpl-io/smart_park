from init_db import *
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

import math
from functools import reduce

#user leaves parking region, we find all regions within a certain distance of the parking region
#(does it check from the center of the line or edge has to be center). If dist(region - park_len) - park_len/2 < epsilon
#and region is free (not in park table) we merge, delete park region spot id and from park table adjust region to be
#region union park region


MIN_PARKING_SPACE = 2


def leave_park(user_id: int, car_id: int):
    engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/smart_park_db')
    Session = sessionmaker(bind=engine)
    session = Session()

    park_info = session.query(Park.spot_id, Park.time_arrived).filter(Park.user_id == user_id and Park.car_id == car_id).first()
    
    
    obj = session.query(Spot).filter(Spot.spot_id == park_info[0]).first()

    parked_spot = ParkHistory(user_id = user_id,
                              region = obj.region,
                              time_arrived = park_info[1])
    
    session.add(parked_spot)

    parked_region = obj.region

    ##if car was parked in between two cars then we don't delete

    #now search for regions within certain distance of parking region

    merge_spots = session.query(Spot).filter(func.ST_DWithin(Spot.region, parked_region, MIN_PARKING_SPACE)).filter(Spot.spot_id != park_info[0]).all()



    #at most there should be two regions here
    
    if merge_spots:
        session.delete(obj)

        regions = [region.region for region in merge_spots] + [parked_region]

        geometry_regions = [func.ST_GeomFromWKB(func.ST_AsBinary(region)) for region in regions]

        merged_geometry = reduce(lambda x, y: func.ST_Simplify(func.ST_LineMerge(func.ST_Union(x,y)), 1e-7 ), geometry_regions)

        merge_region_geom = session.query(merged_geometry).one()[0]

        merge_region = func.ST_GeogFromWKB(merge_region_geom)
        if len(merge_spots) == 2:
            session.delete(merge_spots[1])
        
        merge_spots[0].region = merge_region

    session.commit()