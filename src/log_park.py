
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
                location: tuple[float, float]):
    
    
    pass

