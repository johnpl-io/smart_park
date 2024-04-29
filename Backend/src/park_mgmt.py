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
from scipy.ndimage.filters import gaussian_filter
from io import BytesIO
import base64



def log_park(user_id: int, car_id: int, location: tuple[float, float]):

    session = create_session()

    new_spot = Spot(location = func.ST_Point(location[0], location[1], type_ = Geography))

    session.add(new_spot)

    session.commit()

    new_park = Park(spot_id =new_spot.spot_id, 
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

        latitude, longitude = result
        return True, (latitude, longitude)
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
    x = np.linspace(bounds['min_lon'], bounds['max_lon'], 512)
    y = np.linspace(bounds['min_lat'], bounds['max_lat'], 512)
    x_grid, y_grid = np.meshgrid(x, y)
    heatmap = np.zeros_like(x_grid)

    for lat, lon in data:
        ix = np.searchsorted(x, lon)
        iy = np.searchsorted(y, lat)
        if 0 <= ix < 1024 and 0 <= iy < 1024:
            heatmap[iy, ix] += 1
    
    heatmap = gaussian_filter(heatmap, sigma=16)

    plt.imshow(heatmap, extent=(bounds['min_lon'], bounds['max_lon'], bounds['min_lat'], bounds['max_lat']), origin='lower', cmap='hot')
    plt.axis('off') 
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)  # Save with transparent background

    plt.close()
    buf.seek(0)

    
    base64_string = base64.b64encode(buf.read()).decode('utf-8')

    
    return base64_string, bounds