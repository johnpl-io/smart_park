from init_db import *
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, joinedload

import math
from functools import reduce


MIN_PARKING_SPACE = 2


def leave_park(user_id: int, car_id: int) -> None:
    """This function updates the database when a user leaves a parking space by merging
    any adjacent free spots to the newly available parking space

    Parameters:
    :param user_id: The ID of the user (primary key in the user table).
    :param car_id: The ID of the car (primary key in the car table).
    """

    engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/smart_park_db')
    Session = sessionmaker(bind=engine)
    session = Session()

    #we query the database to get the spot id, time the user parked, and the region
    #that the user occupied by filtering for user_id and car_id

    park_info = (session.query(Park.time_arrived, Spot)
                 .join(Spot, Park.spot_id == Spot.spot_id)
                 .filter(Park.user_id == user_id, Park.car_id == car_id)
                 .limit(1)
                 .options(joinedload(Park.spot))
                 .one_or_none())
    
    #create a log in the park history table
    park_log = ParkHistory(user_id = user_id,
                              region = park_info.Spot.region,
                              time_arrived = park_info.time_arrived)
    
    session.add(park_log)


    ##if car was parked in between two cars then we don't delete since there wouldn't be any available spots to merge the newly freed up
    #parking space with

    #now we search for available regions that are adjacent to parking region. We should at most get two regions (in front
    #and behind car for this). Possibly important: Distances are likely measured between centers of regions

    merge_spots = (session.query(Spot)
                   .filter(func.ST_DWithin(Spot.region, park_info.Spot.region, MIN_PARKING_SPACE))
                   .filter(Spot.spot_id != park_info[0]).limit(2).all())
    
    

    #if there are available regions    
    if merge_spots:

        #we delete the freed up spot from the spot table which in turn causes a cascade delete in the park table
        session.delete(park_info.Spot)
        
        #get the available regions including the newly freed up region
        regions = [region.region for region in merge_spots] + [park_info.Spot.region]

        #it looks like unions can only be done on geometry objects: https://postgis.net/docs/ST_Union.html
        #so the regions need to be converted temporarily to geometries and then merged together

        geometry_regions = [func.ST_GeomFromWKB(func.ST_AsBinary(region)) for region in regions]

        #we then merge the regions together. Sometimes due to rounding errors, the union function might think that 
        #two adjacent line segments are disjoint so you need to give it a margin of error so it knows when it's ok to merge them together
        #Since a degree of latitude (which I think is larger than longitude) is roughly 111,111 meters, 
        #a threshold of 1e-7 would be at most 1.11 centimeters so it shouldn't cause any incorrect unions
        merged_geometry = reduce(lambda x, y: func.ST_Simplify(func.ST_LineMerge(func.ST_Union(x,y)), 1e-7 ), geometry_regions)

        merge_region_geom = session.query(merged_geometry).one()[0]

        #we then convert back into a geography object
        merge_region = func.ST_GeogFromWKB(merge_region_geom)
        
        #if we had multiple available regions we delete one of them since they were all merged together
        if len(merge_spots) == 2:
            session.delete(merge_spots[1])
        
        #and finally we update the merged region
        merge_spots[0].region = merge_region

    session.commit()