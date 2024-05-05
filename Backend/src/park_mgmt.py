from init_db import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, cast
from geoalchemy2 import  Geography, Geometry
from geoalchemy2.functions import ST_X, ST_Y 
from utils import create_session
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from geoalchemy2.elements import WKTElement
from scipy.ndimage.filters import gaussian_filter
from io import BytesIO
import base64



def log_park(user_id: int, car_id: int, location: tuple[float, float]):

    session = create_session()

    current_location = WKTElement(f'POINT({location[0]} {location[1]})', srid=4326)
    

    nearby_spot_id = (session.query(Spot.spot_id)
                      .filter(~Spot.park.any())
                      .filter(func.ST_DWithin(
                          current_location,
                          Spot.location,
                          0.5)).first())
                   
    if nearby_spot_id:
        spot_id = nearby_spot_id[0]
    else:
        new_spot = Spot(location = current_location)

        session.add(new_spot)

        session.commit()

        spot_id = new_spot.spot_id


    new_park = Park(spot_id = spot_id, 
                    user_id = user_id,
                    car_id = car_id)
    
    session.add(new_park)
    session.commit()

    session.close()


def leave_park(user_id: int, car_id: int):

    session = create_session()

    park = (session.query(Park)
                 .filter(Park.user_id == user_id, Park.car_id == car_id)
                 .limit(1)
                 .one_or_none())
    

    park_log = ParkHistory(user_id = user_id,
                              spot_id = park.spot_id,
                              time_arrived = park.time_arrived)
    

    session.add(park_log)

    session.delete(park)

    session.commit()

    session.close()


def check_park(user_id: int, car_id: int):
    session = create_session()

    try:
        result = (session.query(func.ST_X(cast(Spot.location, Geometry)),
                                func.ST_Y(cast(Spot.location, Geometry)))
                  .join(Park, Park.spot_id == Spot.spot_id)
                  .filter(Park.user_id == user_id, Park.car_id == car_id)
                  .one_or_none())

        if result == None:
            return False, None

        longitude, latitude = result
        return True, (longitude, latitude)
    finally:
        session.close()

def load_parks(sw_lat, sw_lon, ne_lat, ne_lon):

    """
    Retrieves the positions of all parked cars within the specified rectangular region.
    
    Parameters:
    sw_lat (float): Latitude of the South-West corner.
    sw_lon (float): Longitude of the South-West corner.
    ne_lat (float): Latitude of the North-East corner.
    ne_lon (float): Longitude of the North-East corner.
    
    Returns:
    list of tuples: Each tuple contains (latitude, longitude) of a parked spot.
    """

    session = create_session()

    try:
        results = session.query(
            Spot.spot_id,
            func.ST_Y(Spot.location.cast(Geometry)).label('latitude'),
            func.ST_X(Spot.location.cast(Geometry)).label('longitude')
        ).join(
            Park, Park.spot_id == Spot.spot_id
        ).filter(
            func.ST_Contains(
                func.ST_MakeEnvelope(sw_lon, sw_lat, ne_lon, ne_lat, 4326).cast(Geometry),
                Spot.location.cast(Geometry)
            )
        ).all()

        # Return list of tuples (id, latitude, longitude)

        parkings = ([(result.latitude, result.longitude) for result in results])

        

        bounds = {"min_lon": min([parking[1] for parking in parkings]),
              "max_lon":  max([parking[1] for parking in parkings]),
              "min_lat": min([parking[0] for parking in parkings]),
              "max_lat": max([parking[0] for parking in parkings])}
        
        return create_heatmap(parkings, bounds)
    finally:
        session.close()

def create_heatmap(data, bounds):

    resolution = 1024

    x = np.linspace(bounds['min_lon'], bounds['max_lon'], resolution)
    y = np.linspace(bounds['min_lat'], bounds['max_lat'], resolution)
    x_grid, y_grid = np.meshgrid(x, y)
    heatmap = np.zeros_like(x_grid)


    lon_indices = np.searchsorted(x, [pt[1] for pt in data])
    lat_indices = np.searchsorted(y, [pt[0] for pt in data])

    valid = (lon_indices >= 0) & (lon_indices < resolution) & (lat_indices >= 0) & (lat_indices < resolution)
    np.add.at(heatmap, (lat_indices[valid], lon_indices[valid]), 1)
    
    heatmap = gaussian_filter(heatmap, sigma=16)

    plt.imshow(heatmap, extent=(bounds['min_lon'], bounds['max_lon'], bounds['min_lat'], bounds['max_lat']), origin='lower', cmap='hot')
    plt.axis('off') 
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)  # Save with transparent background

    plt.close()
    buf.seek(0)

    
    base64_string = base64.b64encode(buf.read()).decode('utf-8')

    
    return base64_string, bounds