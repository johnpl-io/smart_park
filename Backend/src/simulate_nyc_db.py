from sqlalchemy import (
    Column,
    Integer,
    String,
)

from sqlalchemy import (
    Integer,
    String,
    Column,
)
from sqlalchemy.orm import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()


class nyc_street(Base):
    """
    This class represents the nyc_streets table for orm
    
    """
    __tablename__ = "nyc_streets"
    # id 8 bit integer
    id = Column(Integer, primary_key=True)
    geom = Column(Geometry(geometry_type="MultiLineString", srid=26918), nullable=True)
    # one way varchar(10)
    oneway = Column(String(10), nullable=True)
    type = Column(String(50), nullable=True)

    def __repr__(self):
        return f"nyc_street(id={self.id}, geom={self.geom}, oneway={self.oneway}, type={self.type})"

