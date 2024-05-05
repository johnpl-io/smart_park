from init_db import *
from sqlalchemy.orm import aliased
from utils import create_session


class Car_MGMT:
    def __init__(self, engine):
        self.engine = engine

    def get_cars(self, user_id):
        session = create_session(self.engine)
        spot_alias = aliased(Spot)

        combined_query = (
            session.query(
                Car.car_id,
                Car.car_model,
                Car.car_img,
                spot_alias.location.ST_AsText().label("park_location"),
            )
            .join(Owns, Owns.car_id == Car.car_id)
            .outerjoin(
                Park, (Park.car_id == Car.car_id) & (Park.user_id == Owns.user_id)
            )
            .outerjoin(spot_alias, Park.spot_id == spot_alias.spot_id)
            .filter(Owns.user_id == user_id)
        )
        results = combined_query.all()

        results = [
            dict(zip(["car_id", "model", "image_path", "location"], result))
            for result in results
        ]

        return results

    def get_models(self):
        session = create_session(self.engine)
        results = (session.query(Car.car_model)).all()

        return [result[0] for result in results]

    def find_cars(self, search_term):
        session = create_session(self.engine)
        results = session.query(Car.car_id, Car.car_model, Car.car_img).filter(
            Car.car_model.ilike(f"{search_term}%")
        )

        results = [
            dict(zip(["car_id", "model", "image_path"], result)) for result in results
        ]

        return results

    def register(self, user_id, car_id):
        session = create_session(self.engine)
        try:
            new_ownership = Owns(user_id=user_id, car_id=car_id)
            session.add(new_ownership)

            session.commit()
            return True
        except:
            return False
