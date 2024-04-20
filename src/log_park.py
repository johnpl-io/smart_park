
def get_region(location: tuple[float, float], 
               length: float, 
               theta: float) -> list[tuple[float, float],
                                     tuple[float, float]]:
    
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

    returns: the start and end point of the line segment represented by the user's parked car
    """
    pass


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

