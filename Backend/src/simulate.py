#script made for simulating parking and leaving events 
from simulate_nyc_db import *
from sqlalchemy.orm import  sessionmaker,  Session
from sqlalchemy import create_engine, func, cast
from geoalchemy2.elements import WKTElement
from geoalchemy2 import Geometry
nyc_engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/nyc')
nyc_session = Session(nyc_engine)
class Simulation():

    def get_closest_point(self, location: tuple[float, float])-> tuple[float, float]:
        get_closest_point = (
                nyc_session.query(
                nyc_street.id, 
                func.ST_X(func.ST_Transform(func.ST_ClosestPoint(nyc_street.geom, WKTElement(f'POINT({location[0]} {location[1]})', srid=26918)), 4326)),
                func.ST_Y(func.ST_Transform(func.ST_ClosestPoint(nyc_street.geom, WKTElement(f'POINT({location[0]} {location[1]})', srid=26918)), 4326))
                )
            
            .order_by(nyc_street.geom.distance_centroid(WKTElement(f'POINT({location[0]} {location[1]})', srid=26918)))

        ).limit(1).first()
        return get_closest_point
    

def car(env):

    while True:

        print('Start parking at %d' % env.now)

        parking_duration = 5

        yield env.timeout(parking_duration)


        print('Start driving at %d' % env.now)

        trip_duration = 2

        yield env.timeout(trip_duration)

        