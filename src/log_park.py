import math

def get_park_EP(location: tuple[float, float], 
               length: float, 
               theta: float) -> tuple[float, float]:
    
    """This function, given the location of the user in the driver's seat and the
    length and orientation of their car, determines the region that the car
    occupies. Each parked car is represented as a line segment in our database
    since the length of the car is all we need to determine if a car can fit
    in a space. 
    
    :param location: The location (latitude, longitude) of the user who is in 
    the driver seat of the car. 

    :param length: The length of the car in meters

    :param theta: The orientation of the car in degrees with respect to the positive
    x axis

    returns: the end point of the line segment represented by the user's parked car
    """

    #radius of Earth in meters as according to: https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html

    r_earth = 6378.137*1e3

    #since the car is at an angle, the change in x and y are:

    dy = length*math.sin(theta)
    dx = length*math.cos(theta)

    #the latitude and longitude coordinates of the end of the car are then (formula for this
    #was found here: https://stackoverflow.com/questions/7477003/calculating-new-longitude-latitude-from-old-n-meters)

    new_lat = location[0] + (dy / r_earth)*(180 / math.pi)
    new_long = location[1] + (dx / r_earth)*(180 / math.pi) / math.cos(location[0]*math.pi/180)

    return (new_lat, new_long)



def log_parking(user_id: int, 
                car_id: int, 
                location: tuple[float, float],
                theta: float):
    
    """This function updates the database when a user parks their car. It first checks
    to see if the parking region overlaps with any of the free regions in our spots table
    If it does then the overlapping region is subtracted from the free region and if 
    the resulting remaining free region is too small for any car to park in, it is added to
    the parking region since the car effectively takes up that reigon as well. An entry in 
    the park table is also made.

    :param: user_id: The id of the user (primary key of the user table)
    
    :param car_id: The id of the car (primary key of car table)

    :param location: The location (latitude, longitude) of the user who is in 
    the driver seat of the car. 

    :param theta: The orientation of the car in degrees with respect to the positive
    x axis
    """

    
    
    pass

