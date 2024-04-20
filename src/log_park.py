import math
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from geoalchemy2.shape import from_shape
from shapely.geometry import LineString

from init_db import *


WKBElement = geoalchemy2.elements.WKBElement
MIN_PARKING_SPACE = -1


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

    pass


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
    car_length = session.query(Car.len).filter(Car.car_id == car_id).first()[0]

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
    

    parking_region, free_region_1, free_region_2 = split_region(parking_region, overlapping_spot.region)


    
    
    
    
