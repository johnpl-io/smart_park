import sys
import os
from init_db import *
import math
from sqlalchemy.orm import  sessionmaker,  Session
from sqlalchemy import create_engine

import hashlib

def geodesic_length(coord1: tuple[float, float], coord2: tuple[float, float]) -> float:
    """This function calculates the geodesic length between two points

    Parameters:
    :param coord1: The first point in (lat, long) coordinates
    :param coord2: The second point in (lat, long) coordinates

    Returns:
    :return: The distance (in meters) between two coordinates
    """

    #radius of Earth in meters as according to: https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html

    r_earth = 6378137

    return math.acos(
        math.sin(coord1[0])*math.sin(coord2[0]) + 
        math.cos(coord1[0])*math.cos(coord2[0])*math.cos(coord2[1] - coord1[1])
    )*r_earth


def setup_db() -> tuple[Session, User, Car]:
    """This function is used for setting up the database for testing purposes.

    Returns: 
    :return: A tuple containining the session object and the user and car created
    """

    #set up the connection to the database
    engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/smart_park_db')
    
    Session = sessionmaker(bind=engine)
    session = Session()

    #drop all rows in each table. Because of how our database is set up
    #dropping just these two tables will drop everything in our database

    session.query(User).delete()
    session.query(Car).delete()
    session.query(Spot).delete()


    password = "password"

    #we then create the test user
    user = User(username = "test00",
            password_hash = hashlib.sha256(password.encode()).digest(), 
            email = "test@test.com")
    
    session.add(user)
    
    #and the user's car
    car = Car(len = 2)
    
    session.add(car)

    session.commit()

    return session, user, car
