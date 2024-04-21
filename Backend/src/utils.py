import math

def geodesic_length(coord1: tuple[float, float], coord2: tuple[float, float]) -> float:
    """This function calculates the geodesic length between two points

    Parameters:
    :param coord1: The first point in (lat, long) coordinates
    :param coord2: The second point in (lat, long) coordinates

    Returns:
    :return: The distance (in meters) between two coordinates
    """

    #radius of Earth in meters as according to: https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html

    r_earth = 6378137

    return math.acos(
        math.sin(coord1[0])*math.sin(coord2[0]) + 
        math.cos(coord1[0])*math.cos(coord2[0])*math.cos(coord2[1] - coord1[1])
    )*r_earth
