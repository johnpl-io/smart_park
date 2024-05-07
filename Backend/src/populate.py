import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from geoalchemy2.elements import WKTElement
from init_db import *
import os
import numpy as np
from tqdm import tqdm
import json5

fake = Faker()
NUM_ENTRIES = 10000


def insert_real_cars():
    engine = create_engine(
        "postgresql+psycopg2://user:password@localhost:5432/smart_park_db"
    )
    session = Session(bind=engine)
    directory = "car_json_dumps"

    file_list = os.listdir(directory)
    trange = file_list
    for filename in tqdm(pbar := tqdm(file_list), 'insert cars'):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            models = []
            with open(filepath, "r") as file:
                data = json5.load(file)
                for car in data["models"]:

                    # not the most elegant way to handle missing data

                    height, width, len = None, None, None

                    if car.get("technical_specs"):
                        dimensions = car["technical_specs"].get("DIMENSIONS")

                        if dimensions:
                            height_str = dimensions.get("Height")
                            if height_str:
                                try:
                                    height = float(height_str)
                                except ValueError:
                                    height = None

                            width_str = dimensions.get("Width")

                            if width_str:
                                try:
                                    width = float(width_str)
                                except ValueError:
                                    width = None 
                            
                            length_str = dimensions.get("Length")
                            if length_str:
                                try:
                                    len = float(length_str)
                                except ValueError:
                                    len = None  

                    # check if img is empty dict
                    if car.get("img") == {}:
                        img = None
                    else:
                        img = car.get("img")

                    model = Car(
                        car_model=car.get("model_name"),
                        height=height,
                        width=width,
                        len=len,
                        car_img=img,
                    )
                    models.append(model)
                session.add_all(models)
                session.commit()

def populate_database():
    engine = create_engine(
        "postgresql+psycopg2://user:password@localhost:5432/smart_park_db"
    )
    session = sessionmaker(bind=engine)()

    # Create random users
    users = []
    
    for i in tqdm(
        range(NUM_ENTRIES), desc="adding users"
    ):  # Adjust the number if necessary

        user = User(
            username="user_" + str(i),
            password_hash=fake.password(
                length=12,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).encode(),
            email="test" + str(i) + "@cooper.edu",
        )
        users.append(user)
    session.add_all(users)
    session.commit()
    

    insert_real_cars()

    sampled_cars = session.query(Car.car_id).limit(1000).all()


    
    # Create relationships between users and cars
    owns = []

    for index in tqdm(range(len(users)), "adding owns relationships to cars"):
        owns_relationship = Owns(user_id=users[index].user_id, car_id=random.choice(sampled_cars)[0])
        owns.append(owns_relationship)

    session.add_all(owns)
    session.commit()



    # Close session
    session.close()


    print("Database populated successfully.")


if __name__ == "__main__":
    initialize()
    populate_database()
