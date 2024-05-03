from sqlalchemy import create_engine, Column, Integer, Float, String, TIMESTAMP, ForeignKey, func

from sqlalchemy.dialects.postgresql import BYTEA

from sqlalchemy.orm import relationship, sessionmaker, declarative_base, Session
from geoalchemy2 import Geography
from sqlalchemy.schema import CreateSchema
from sqlalchemy import PrimaryKeyConstraint

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
    
    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username}, email={self.email})"
    
    

class Car(Base):
    __tablename__ = 'cars'
    
    car_id = Column(Integer, primary_key=True)
    car_model = Column(String, nullable=False)
    
    width = Column(Float, nullable=True)
    len = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    
    owns = relationship("Owns", back_populates="car")
    park = relationship("Park", back_populates="car")

    def __repr__(self):
        return f"Car(car_id={self.car_id}, car_model={self.car_model})"
    

class Owns(Base):
    __tablename__ = 'owns'
    
    user_id = Column(Integer, ForeignKey('users.user_id',  ondelete='CASCADE'), primary_key=True)
    car_id = Column(Integer, ForeignKey('cars.car_id',  ondelete='CASCADE'), primary_key=True)
    
    user = relationship("User", back_populates="owns")
    car = relationship("Car", back_populates="owns")

    def __repr__(self):
        return f"Owns(user_id={self.user_id}, car_id={self.car_id})"

class Spot(Base):
    __tablename__ = 'spot'
    
    spot_id = Column(Integer, primary_key=True)
    location = Column(Geography('POINT', srid=4326))
    park = relationship("Park", back_populates="spot", cascade="all, delete-orphan")
    parked = relationship("ParkHistory", back_populates="spot", cascade="all, delete")

    def __repr__(self):
        return f"Spot(spot_id={self.spot_id}, location={self.location})"
    


class ParkHistory(Base):
    __tablename__ = 'park_history'
    
    phid = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))

    spot_id = Column(Integer, ForeignKey('spot.spot_id', ondelete='CASCADE')) 

    time_arrived = Column(TIMESTAMP, nullable=False)
    time_left = Column(TIMESTAMP, nullable=False, default=func.now())

    spot = relationship("Spot", back_populates="parked")

    user = relationship("User", back_populates="park_history")

def __repr__(self):
    return f"ParkHistory(phid={self.phid}, user_id={self.user_id}, spot_id={self.spot_id}, time_arrived={self.time_arrived}, time_left={self.time_left})"

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

    def __repr__(self):
        return f"Park(pid={self.pid}, spot_id={self.spot_id}, user_id={self.user_id}, car_id={self.car_id}, time_arrived={self.time_arrived})"

class Hold(Base):
    __tablename__ = 'hold'
    __table_args__ = (PrimaryKeyConstraint("user_id", "car_id", "spot_id"), {})
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'))
    car_id = Column(Integer, ForeignKey('cars.car_id', ondelete='CASCADE'))
    spot_id = Column(Integer, ForeignKey('spot.spot_id', ondelete='CASCADE'))
    time_start = Column(TIMESTAMP, nullable=False, default=func.now())

    def __repr__(self):
        return f"Hold(user_id={self.user_id}, spot_id={self.spot_id}, time_start={self.time_start})"
"""
class Violation(Base):
    __tablename__ = 'violation'
    
    violation_id = Column(Integer, primary_key=True)
    region = Column(Geography('LINESTRING', srid=4326))
    
    starting = Column(TIMESTAMP, nullable=False)
    ending = Column(TIMESTAMP, nullable=False)
"""

def initialize() -> None:
    engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/smart_park_db')


    Base.metadata.reflect(bind=engine)

    for table_name in list(Base.metadata.tables) + list(Base.metadata.tables):
        if table_name != "spatial_ref_sys":
            try:
                Base.metadata.tables[table_name].drop(bind=engine, checkfirst=True)
            except:
                continue

    Base.metadata.create_all(engine)



#drop all data tables
def drop_tables() -> None:
    engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/smart_park_db')
    Base.metadata.drop_all(engine)

