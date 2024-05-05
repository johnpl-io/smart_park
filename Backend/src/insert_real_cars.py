import os
from tqdm import tqdm
import json5
from sqlalchemy import create_engine
from init_db import *


def insert_real_cars():
    engine = create_engine(
        "postgresql+psycopg2://user:password@localhost:5432/smart_park_db"
    )
    session = Session(bind=engine)
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
                                    width = None  # Set to None if conversion fails
                            length_str = dimensions.get("Length")
                            if length_str:
                                try:
                                    len = float(length_str)
                                except ValueError:
                                    len = None  # Set to None if conversion fails
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


insert_real_cars()
