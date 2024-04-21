import math
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from geoalchemy2.shape import from_shape
from geoalchemy2.elements import WKBElement

from shapely.geometry import LineString, MultiLineString
from shapely import wkb, difference
from shapely.ops import linemerge

from init_db import *
from utils import geodesic_length


MIN_PARKING_SPACE = 2


def get_park_EP(location: tuple[float, float], 
               length: float, 
               theta: float) -> tuple[float, float]:
    
    """This function, given the location of the user in the driver's seat and the
    length and orientation of their car, determines the region that the car
    occupies. Each parked car is represented as a line segment in our database
    since the length of the car is all we need to determine if a car can fit
    in a space. 
    
    Parameters:
    :param location: The location (latitude, longitude) of the user who is in the driver seat of the car. 
    :param length: The length of the car in meters
    :param theta: The orientation of the car in degrees with respect to the positive x axis

    Returns:
    :return: A tuple representing the latitude and longitude of the endpoint of the line segment represented by the car.
    """

    #radius of Earth in meters as according to: https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html

    r_earth = 6378137

    #Calculate change in position due to car's orientation

    dy = length* math.sin(math.radians(theta))
    dx = length* math.cos(math.radians(theta))

    #the latitude and longitude coordinates of the end of the car are then (formula for this
    #was found here: https://stackoverflow.com/questions/7477003/calculating-new-longitude-latitude-from-old-n-meters)

    new_lat = location[0] + (dy / r_earth)*(180 / math.pi)
    new_long = location[1] + (dx / r_earth)*(180 / math.pi) / math.cos(math.radians(location[0]))

    
    return (new_lat, new_long)



def split_region(parking_region: WKBElement , 
                  overlap_region: WKBElement) -> tuple[WKBElement, WKBElement, WKBElement]:

    """This function splits the available parking space into at most 3 regions: the parking region,
    the available region in front of the parking region, and the available region behind the parking region

    Parameters
    :param parking_region: The geography object representing the region that the user parked in
    :param overlap_region: The geography object representing the available parking space that overlaps with the parking region

    Returns:
    :return: A tuple containing the the three geography objects that represent the regions that were split as a result of the parking
    """

    if not overlap_region:
        return parking_region, None, None

    #We will first convert the regions to shapely objects so that we can perform operations on them without using the database

    parking_region = wkb.loads(str(parking_region), hex = True)
    overlap_region = wkb.loads(str(overlap_region), hex = True)


    #then we want to get the part of the overlap_region that exists outside of the parking region

    regions = difference(overlap_region, parking_region)


    #we at most will have two split regions from this
    if type(regions) == MultiLineString:
        region_1, region_2 = regions.geoms
    else:
        region_1 = regions

        #we make the second region something that takes up no space
        region_2 = LineString([(0, 0), (0, 0)])
    
    regions = [region_1, region_2]


    #sort the regions by their length
    regions.sort(key = lambda x: x.length, reverse = True)

    free_region_1 = None
    free_region_2 = None

    #if both regions are sufficiently small (regions[0].length > regions[1] so only need to check regions[0].length)
    if geodesic_length(regions[0].coords[0], regions[0].coords[1]) < MIN_PARKING_SPACE:

        #then parking region effectively takes up entire overlap_region
        parking_region = linemerge(parking_region.union(overlap_region))


    
    else:
        #if the smaller available region is sufficiently small and exists
        if 0 < geodesic_length(regions[1].coords[0], regions[1].coords[1]) < MIN_PARKING_SPACE:

            parking_region = linemerge(parking_region.union(regions[1]))

        
        
        elif regions[1].length > 0:
            
            #else that available region is big enough to be its own parking region
            free_region_2 = from_shape(regions[1], srid=4326)
        
        #and the first free region  would also be large enough as well
        free_region_1 = from_shape(regions[0], srid=4326)
    
    parking_region = from_shape(parking_region, srid=4326)


    return parking_region, free_region_1, free_region_2






def log_parking(user_id: int, 
                car_id: int, 
                location: tuple[float, float],
                theta: float) -> None:
    
    """This function updates the database when a user parks their car. It first checks
    to see if the parking region overlaps with any of the free regions in our spots table
    If it does then the overlapping region is subtracted from the free region and if 
    the resulting remaining free region is too small for any car to park in, it is added to
    the parking region since the car effectively takes up that reigon as well. An entry in 
    the park table is also made.

    Parameters:
    :param user_id: The ID of the user (primary key in the user table).
    :param car_id: The ID of the car (primary key in the car table).
    :param location: The latitude and longitude of the driver (tuple of floats).
    :param theta: The orientation of the car in degrees from the positive x-axis.
    """

    engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/smart_park_db')
    Session = sessionmaker(bind=engine)
    session = Session()

    #we query the cars table to get the length of the car
    car_length = session.query(Car.len).filter(Car.car_id == car_id).limit(1).one_or_none()

    #and then create the linestring object representing the region that the car is parked in
    parking_region = LineString([location, get_park_EP(location, car_length, theta)])


    #convert the linestring into a geography object
    parking_region = from_shape(parking_region, srid=4326)

    #now we need to check if the parking_region overlaps with any of the available regions in our
    #spots table
    
    #since this is an expensive operation we first should remove any spot ids that are already occupied

    occupied_spots = session.query(Park.spot_id).subquery()

    #If the spot is in our Park table then we filter it out
    available_spots = session.query(Spot).outerjoin(
        occupied_spots, Spot.spot_id == occupied_spots.c.spot_id
    ).filter(occupied_spots.c.spot_id == None)

    #then we check if the parking region intersects with the available regions.
    #At most, we will only ever have at most one overlapping spot so we stop searching after
    #we have found one overlapping spot
    overlapping_spot = available_spots.filter(func.ST_Intersects
                                                  (Spot.region, parking_region)).limit(1).one_or_none()
    
    #if no overlap at all
    if not overlapping_spot:
        
        #this is a completely new spot so we simply add a new spot and park entry
        new_spot = Spot(region = parking_region)
        session.add(new_spot)

        session.commit()

        new_park = Park(
            spot_id = new_spot.spot_id,
            user_id = user_id,
            car_id = car_id
        )
        session.add(new_park)
        session.commit()
        return
    
    parking_region, free_region_1, free_region_2 = split_region(parking_region, overlapping_spot.region)

    #if free_region_1 and free_region_2 are None we change overlapping spot entry region to be parking_region

    #if everything is not None we make overlapping spot entry region to be free_region_1 and then make two new entries
    #for parking_region and free_region_2

    #if free_region_2 is not None then we make overlapping spot entry region free_region_1 and make new entry for 
    #parking_region


    if free_region_1 or free_region_2:
        
        #since free_region_1 is larger than free_region_2 to get here free_region_1 has to be sufficiently
        #large enough for some car to fit in it

        #we update the overlapping_spot region to be free_region_1
        overlapping_spot.region = free_region_1

        #make a new spot for the parking region
        new_spot = Spot(region = parking_region)

        session.add(new_spot)

        session.commit()

        #and a new park entry
        new_park = Park(
            spot_id = new_spot.spot_id,
            user_id = user_id,
            car_id = car_id
        )

        if free_region_2:

            
            #and likewise if free_region_2 is large enough we make a spot for it
            new_spot = Spot(region=free_region_2)

            session.add(new_spot)

            session.commit()

    else:
        
        #if we're here then that means that either the car tried to park in between two cars and it was a 
        #pretty tight fit or the car parked right next to another car and was really close to it and the 
        #other side of the car is either not registered in our database yet or is the end of the street
        
        #either way we make the region of the overlapping_spot parking_region which had become
        #the union between parking_region and the overlapping_spot
        overlapping_spot.region = parking_region

        new_park = Park(
            spot_id = overlapping_spot.spot_id,
            user_id = user_id,
            car_id = car_id
        )

    session.add(new_park)


    session.commit()