from sqlalchemy import create_engine, Column, Integer, Float, String, TIMESTAMP, ForeignKey, func

from sqlalchemy.dialects.postgresql import BYTEA

from sqlalchemy.orm import relationship, sessionmaker, declarative_base, Session
from geoalchemy2 import Geography
from sqlalchemy.schema import CreateSchema


Base = declarative_base()



class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(BYTEA, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    created_on = Column(TIMESTAMP, nullable=False, default=func.now())


    owns = relationship("Owns", back_populates="user", cascade="all, delete")
    park_history = relationship("ParkHistory", back_populates="user", cascade="all, delete")
    park = relationship("Park", back_populates="user", cascade = "all, delete")

class Car(Base):
    __tablename__ = 'cars'
    
    car_id = Column(Integer, primary_key=True)
    
    #width = Column(Float, nullable=False)
    len = Column(Float, nullable=False)
    
    owns = relationship("Owns", back_populates="car")
    park = relationship("Park", back_populates="car")

class Owns(Base):
    __tablename__ = 'owns'
    
    user_id = Column(Integer, ForeignKey('users.user_id',  ondelete='CASCADE'), primary_key=True)
    car_id = Column(Integer, ForeignKey('cars.car_id',  ondelete='CASCADE'), primary_key=True)
    
    user = relationship("User", back_populates="owns")
    car = relationship("Car", back_populates="owns")

class Spot(Base):
    __tablename__ = 'spot'
    
    spot_id = Column(Integer, primary_key=True)
    region = Column(Geography('LINESTRING', srid=4326))
    park = relationship("Park", back_populates="spot")

class ParkHistory(Base):
    __tablename__ = 'park_history'
    
    phid = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
                                         
    region = Column(Geography('LINESTRING', srid=4326))
    time_arrived = Column(TIMESTAMP, nullable=False)
    time_left = Column(TIMESTAMP, nullable=False, default=func.now())
    
    user = relationship("User", back_populates="park_history")

class Park(Base):
    __tablename__ = 'park'
    pid = Column(Integer, primary_key=True)
    
    spot_id = Column(Integer, ForeignKey('spot.spot_id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    car_id = Column(Integer, ForeignKey('cars.car_id', ondelete='CASCADE'))
    
    time_arrived = Column(TIMESTAMP, nullable=False, default=func.now())
    
    spot = relationship("Spot", back_populates="park")
    user = relationship("User", back_populates="park")
    car = relationship("Car", back_populates="park")

class Violation(Base):
    __tablename__ = 'violation'
    
    violation_id = Column(Integer, primary_key=True)
    region = Column(Geography('LINESTRING', srid=4326))
    
    starting = Column(TIMESTAMP, nullable=False)
    ending = Column(TIMESTAMP, nullable=False)


engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/smart_park_db')


Base.metadata.reflect(bind=engine)

for table_name in list(Base.metadata.tables) + list(Base.metadata.tables):
    if table_name != "spatial_ref_sys":
        try:
            Base.metadata.tables[table_name].drop(bind=engine, checkfirst=True)
        except:
            continue

Base.metadata.create_all(engine)

session = Session(engine)
connection = engine.connect()
