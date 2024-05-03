import os
from tqdm import tqdm
import json5
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from init_db import *

def insert_real_cars():
    engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/smart_park_db')
    session = sessionmaker(bind=engine)
    directory = "car_json_dumps"
    file_list = os.listdir(directory)
    trange = file_list
    for filename in tqdm(pbar := tqdm(file_list)):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            models = []
            with open(filepath, "r") as file:
                data = json5.load(file)
                for car in data["models"]:
                    model = Car(
                        car_model=car.get("model_name"),
                        height=car.get("Dimensions").get("Height"),
                        width=car.get("Dimensions").get("Width"),
                        length=car.get("Dimensions").get("Length"),
                    )
                    models.append(model)
                session.add_all(models)
                session.commit()


insert_real_cars()