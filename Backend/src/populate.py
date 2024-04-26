import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2.elements import WKTElement
from init_db import *

fake = Faker()
NUM_ENTRIES = 10000
def populate_database():
    engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/smart_park_db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create random users
    users = []

    for i in range(NUM_ENTRIES):  # Adjust the number if necessary

        user = User(
            username= "user_" + str(i),
            password_hash=fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True).encode(),
            email= "test" +  str(i) + "@cooper.edu"
        )
        users.append(user)
    session.add_all(users)
    session.commit()

    # Create random cars
    cars = []
    for _ in range(10):  # Adjust the range for more cars
        car = Car(
            car_model=fake.company()
        )
        cars.append(car)
    session.add_all(cars)

    # Create random spots
    spots = []
    for _ in range(NUM_ENTRIES):  # Adjust the range for more spots
        lat = random.uniform(40.7011, 40.7850)  # Latitude range for Manhattan
        lon = random.uniform(-74.0100, -73.9490)  # Longitude range for Manhattan
        spot = Spot(
            location=WKTElement(f'POINT({lon} {lat})', srid=4326)
        )
        spots.append(spot)
    session.add_all(spots)

    # Commit to save users, cars, and spots
    session.commit()

    # Create relationships between users and cars
    owns = []
    for user in users:
        car = random.choice(cars)
        owns_relationship = Owns(
            user_id=user.user_id,
            car_id=car.car_id
        )
        owns.append(owns_relationship)
    session.add_all(owns)

    # Create parking history and current park status
    for spot in spots:
        user = random.choice(users)
        car = random.choice(cars)
        park_history = ParkHistory(
            user_id=user.user_id,
            spot_id=spot.spot_id,
            time_arrived=fake.past_datetime(),
            time_left=fake.date_time_between(start_date='-1y', end_date='now')
        )
        current_park = Park(
            spot_id=spot.spot_id,
            user_id=user.user_id,
            car_id=car.car_id,
            time_arrived=fake.past_datetime()
        )
        session.add(park_history)
        session.add(current_park)

    # Commit the relationships and park history
    session.commit()

    # Close session
    session.close()

    print("Database populated successfully.")

if __name__ == "__main__":
    initialize()
    populate_database()
