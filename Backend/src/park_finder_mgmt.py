from init_db import *
from sqlalchemy import func, cast
from geoalchemy2 import Geometry
from utils import create_session
from geoalchemy2.elements import WKTElement
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine
from sqlalchemy import delete

class ParkFinder_MGMT:
    def __init__(self, engine):
        self.engine = engine

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
        #delete all holds older then 10 minutes
        
  
        
        session.query(Hold).where(Hold.time_start < (datetime.now(timezone.utc) - timedelta(minutes=10))).delete()
      
        session.commit()
        
        
        valid_holds = session.query(Hold.spot_id)
        
    

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
            #make sure the spot has not been taken
            .outerjoin(Park, Spot.spot_id == Park.spot_id)
            .filter(Park.spot_id == None)
            .join(ParkHistory, Spot.spot_id == ParkHistory.spot_id)
            .filter(
                ParkHistory.time_left
                >= (datetime.now(timezone.utc) - timedelta(minutes=10))
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

    def create_hold(self, user_id: int, car_id: int, spot_id: int, time_start: datetime = None) -> bool:
        """
        obtain a temporary hold of  a free spot after a user selects it in the frontend
        Parameters:
        :user_id: user_id of indivual requesting a spot
        :car_id: the car_id of the user_id current car
        :spot_id: the spot_id of the spot the user wants to hold

        """
         
        session = create_session(self.engine) 
        
        session.query(Hold).where(Hold.time_start < (datetime.now(timezone.utc) - timedelta(minutes=10))).delete()
      
        session.commit()
        
       
        #if you all ready have a hold for  the spot prevent spot from being held 
        
        current_hold = session.query(Hold).filter(Hold.spot_id == spot_id).first()

        if current_hold:
            return False

        session.query(Hold).filter(Hold.user_id == user_id).delete()
        session.commit()
        # create a hold unix epoch time
        new_hold = Hold(
            user_id=user_id,
            car_id=car_id,
            spot_id=spot_id,
            time_start=time_start,
        )
        session.add(new_hold)
        session.commit()
        return True

#engine = create_engine("postgresql+psycopg2://user:password@localhost:5432/smart_park_db")
#park_finder_mgmt = ParkFinder_MGMT(engine=engine)
#park_finder_mgmt.create_hold(1, 1, 1)
#park_finder_mgmt.create_hold(1, 1, 1, datetime.fromtimestamp(0))
#z = park_finder_mgmt.park_find(0, 0, [ -77.062089, 38.8938 ])

#create a hold for user 1 spot 1 for unix epoch time
