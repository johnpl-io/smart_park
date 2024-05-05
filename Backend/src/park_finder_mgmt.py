from init_db import *
from sqlalchemy import func, cast
from geoalchemy2 import Geometry
from utils import create_session
from geoalchemy2.elements import WKTElement
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine


class ParkFinder_MGMT:
    def __init__(self, engine):
        self.engine = create_engine(
            "postgresql+psycopg2://user:password@localhost:5432/nyc"
        )

    def park_find(
        self, user_id: int, car_id: int, location: tuple[float, float]
    ) -> list[int, int, int, float, datetime]:
        session = create_session(self.engine)
        """
        find a parking spot given a user and a specific location 
        a spot must have been recently left and close to the user
        Parameters:
        :user_id: user_id of indivual requesting a spot
        :car_id: the car_id of the user_id current car
        :location: location of area where spot is

        Returns:
        :return: A tuple representing the latitude and longitude of the endpoint of the line segment represented by the car.
        """

        # find closest points that have recently been left for now it simply picks ten closest poinst
        # first check if there are any holds over 10 minutes old
        # get all holds
        valid_holds = session.query(Hold.spot_id).filter(
            Hold.time_start >= (datetime.now(timezone.utc) - timedelta(minutes=10))
        )
        get_closest = (
            session.query(
                Spot.spot_id,
                func.ST_X(cast(Spot.location, Geometry)),
                func.ST_Y(cast(Spot.location, Geometry)),
                func.ST_Distance(
                    Spot.location, WKTElement(f"POINT({location[0]} {location[1]})")
                ),
                ParkHistory.time_left,
            )
            .join(ParkHistory, Spot.spot_id == ParkHistory.spot_id)
            .filter(
                ParkHistory.time_left
                >= (datetime.now(timezone.utc) - timedelta(days=10))
            )
            .filter(Spot.spot_id.notin_(valid_holds))
            .order_by(
                Spot.location.cast(Geometry).distance_centroid(
                    WKTElement(f"POINT({location[0]} {location[1]})", srid=4326)
                )
            )
            .limit(10)
        ).all()
        session.close()
        return get_closest

    def create_hold(self, user_id: int, car_id: int, spot_id: int):
        """
        obtain a temporary hold of  a free spot after a user selects it in the frontend
        Parameters:
        :user_id: user_id of indivual requesting a spot
        :car_id: the car_id of the user_id current car
        :spot_id: the spot_id of the spot the user wants to hold

        """
        session = create_session(self.engine)
        # create a hold unix epoch time
        new_hold = Hold(
            user_id=user_id,
            car_id=car_id,
            spot_id=spot_id,
            time_start=datetime.now(timezone.utc),
        )
        session.add(new_hold)
        session.commit()


# park_finder_mgmt = ParkFinder_MGMT()
# z = park_finder_mgmt.park_find(0, 0, [ -77.062089, 38.8938 ])
