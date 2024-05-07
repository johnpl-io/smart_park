# script made for simulating parking and leaving events
from simulate_nyc_db import *
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, func, cast
from geoalchemy2.elements import WKTElement
from geoalchemy2 import Geometry
import simpy
import logging
import random
from park_mgmt import Park_MGMT
from init_db import *

logging.basicConfig(level=logging.INFO)

nyc_engine = create_engine("postgresql+psycopg2://user:password@localhost:5432/nyc")
smart_park_engine = create_engine(
    "postgresql+psycopg2://user:password@localhost:5432/smart_park_db"
)
park_mgmt = Park_MGMT(smart_park_engine)




class Car:
    def __init__(
        self,
        user_id: int,
        car_id: int,
        env: simpy.Environment,
        minx: float,
        miny: float,
        maxx: float,
        maxy: float,
    ):
        """
        Parameters:
        :user_id: id of the user
        :car_id: id of the car
        :env: simpy environment
        :minx: minimum x coordinate of the bounding box
        :miny: minimum y coordinate of the bounding box
        :maxx: maximum x coordinate of the bounding box
        :maxy: maximum y coordinate of the bounding box"""
        self.user_id = user_id
        self.car_id = car_id
        self.minx, self.miny, self.maxx, self.maxy = minx, miny, maxx, maxy
        self.env = env

        self.action = env.process(self.run())
    
    def get_closest_point(self, location: tuple[float, float]):
        nyc_session = Session(nyc_engine)
        get_closest_point = (
            (
                nyc_session.query(
                    func.ST_X(
                        func.ST_Transform(
                            func.ST_ClosestPoint(
                                nyc_street.geom,
                                WKTElement(
                                    f"POINT({location[0]} {location[1]})", srid=26918
                                ),
                            ),
                            4326,
                        )
                    ),
                    func.ST_Y(
                        func.ST_Transform(
                            func.ST_ClosestPoint(
                                nyc_street.geom,
                                WKTElement(
                                    f"POINT({location[0]} {location[1]})", srid=26918
                                ),
                            ),
                            4326,
                        )
                    ),
                    nyc_street.id,
                    nyc_street.type,
                ).order_by(
                    nyc_street.geom.distance_centroid(
                        WKTElement(f"POINT({location[0]} {location[1]})", srid=26918)
                    )
                )
            )
            .limit(1)
            .first()
        )
        return get_closest_point
    def run(self):
        while True:
            logging.info(
                f"user {self.user_id} car {self.car_id} driving {self.env.now}"
            )

            yield self.env.timeout(random.randint(2, 10))

            x, y = random.uniform(self.minx, self.maxx), random.uniform(
                self.miny, self.maxy
            )
            get_closest_point = self.get_closest_point((x, y))

            logging.info(
                f"user {self.user_id} car {self.car_id} parking {self.env.now} at {get_closest_point[0]}, {get_closest_point[1]}"
            )
            park_mgmt.log_park(self.user_id, self.car_id, (get_closest_point[0], get_closest_point[1]))

            yield self.env.timeout(random.randint(1, 5))

            logging.info(
                f"user {self.user_id} car {self.car_id} leaving {self.env.now}"
            )
            park_mgmt.leave_park(self.user_id, self.car_id)
            yield self.env.timeout(random.randint(1, 2))



# get_closest as global

env = simpy.rt.RealtimeEnvironment(factor=0.5)
#env = simpy.Environment()

minx=584267.2673704254
miny=4508850.55155718
maxx=586273.4045800678
maxy=4510942.484684312

#get ten owners from owner table
session_smart_park = Session(smart_park_engine)
owners = (
    session_smart_park.query(Owns.user_id, Owns.car_id)
    .order_by(Owns.user_id)
    .limit(50)
    .all()
)

for i in owners:
    car = Car(i[0], i[1], env, minx, miny, maxx, maxy)
    env.process(car.run())

env.run()


#get random point on street

#get_closest_point_real = get_closest_point((584267.2673704254, 4508850.55155718))
#print(get_closest_point_real)