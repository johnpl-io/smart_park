from init_db import *
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from geoalchemy2.shape import from_shape

from shapely.geometry import Polygon, MultiPolygon, LineString
from shapely import wkb, symmetric_difference
import math

MIN_PARKING_SPACE = -1

engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/smart_park_db')
Session = sessionmaker(bind=engine)
session = Session()

conn = engine.connect()


def get_region(location: tuple[int, int], length: int) -> list[tuple[int, int],
                                                               tuple[int, int]]:
    

    r_earth = 6378*1e3
    new_latitude = (location[0] + (length/r_earth)*(180/math.pi), location[1])
    #new_longitude = location[1] + (dimensions[1]/r_earth)*(180/math.pi)*math.cos(location[0]*math.pi/180)

    '''
    region = [location,
              (new_latitude, location[1]),
               (new_latitude, new_longitude),
               (location[0], new_longitude)]
               '''
    region = [location, new_latitude]
    
    return region
    

def split_regions(parked_region, overlap_region):

    parked_region = wkb.loads(str(parked_region), hex = True)
    overlap_region = wkb.loads(str(overlap_region), hex = True)

    print(parked_region)
    print(overlap_region)

    regions = overlap_region.symmetric_difference(parked_region)
    
    regions = list(regions.geoms)
    

    
    #we need to extract each geometry from the multipolygon that is space_remaining
    #and then find the area of each one
    #and if any of them are less than MIN_PARKING_SPACE, we merge it with parked_region and make that
    #free_region_1 or free_region_2
    #if we have one larger than that, we would set it to be free_region_1 and the second to be
    #free_region_2 (if it's larger) and keep parked_region as is


    regions.sort(key = lambda x: x.length, reverse = False)

    free_region_1 = None
    free_region_2 = None
    
    if regions[0].area < MIN_PARKING_SPACE and regions[1].area < MIN_PARKING_SPACE:
        
        parked_region = overlap_region
    

    else:
        if regions[0].area < MIN_PARKING_SPACE:
            parked_region = parked_region.union(regions[0])
        else:
            free_region_2 = from_shape(regions[0], srid=4326)
    
        free_region_1 = from_shape(regions[1], srid=4326)


    return parked_region, free_region_1, free_region_2
    

def log_user_parking(uid: int, cid: int, location: tuple[int, int]):

    #first get the dimensions of the user's car

    dimensions = session.query(Car.len).filter(Car.car_id == cid)

    length = [dim for dim in dimensions][0][0]


    #then from the car's dimensions we will approximate the space occupied by the car
    parked_region = LineString(get_region(location, length))

    print(parked_region)

    
    parked_region = from_shape(parked_region, srid=4326)

    
    
   
    #more efficient to only look at spots not in park table
    overlapping_spot = session.query(Spot).filter(
                                          func.ST_Intersects(Spot.region, parked_region)
                                          )
    
    overlapping_spot = [spot for spot in overlapping_spot]

    
    
    if not overlapping_spot:

        ##if no overlapping spots, we have a new spot!
        ##we add it to spot table and make entry in park table

        new_spot = Spot(region= parked_region)

        session.add(new_spot)

        new_park = Park(
            spot_id = new_spot.spot_id,
            user_id = uid,
            car_id = cid
        )

        session.add(new_park)
        session.commit()
        return

    overlapping_spot = overlapping_spot[0]
    parked_region, free_region_1, free_region_2 = split_regions(parked_region, overlapping_spot.region)

    #if parked_region is None then that means we update the spot entry for overlapping region to be 
    #free_region_1, then if free_region_2 exists, we make a new spot entry for that. Finally, 
    #we make a park entry for overlapping_region

    #if parked_region is not None and both free regions are None, then that means
    #we just make a park entry for overlapping_region

    #if parked_region is not None and free_region_1 is not None, we modify overlapping_spot
    #to have free_region_1 as its region, make a new spot for parked_region and a new park entry
    #for parked_region

    #if everything is not None, update overlapping_region to free_region_1, parked_region
    #gets a spot and a park entry, and free_region_2 gets a spot entry


    parked_region = from_shape(parked_region, srid=4326)
    if not parked_region:
        overlapping_spot.region = free_region_1

        if free_region_2:

            new_spot = Spot(region = free_region_2)
            session.add(new_spot)
        
        new_park = Park(
            spid = overlapping_spot.spot_id,
            user_id = uid,
            car_id = cid
        )
    
    elif not (free_region_1 or free_region_2):
        new_park = Park(
            spot_id = overlapping_spot.spot_id,
            user_id = uid,
            car_id = cid
        )

    else:

        overlapping_spot.region = free_region_1
        if free_region_2:

            new_spot = Spot(region = free_region_2)
            session.add(new_spot)
        
        new_spot = Spot(region = parked_region)
        session.add(new_spot)

        new_park = Park(
            spot_id = new_spot.spot_id,
            user_id = uid,
            car_id = cid
        )

    session.add(new_park)
    session.commit()