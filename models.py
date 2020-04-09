from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BusLine(Base):
    __tablename__ = "bus_lines"
    id = Column(Integer, primary_key=True)
    line_id = Column(Integer)
    line_description = Column(String)


class BusRoute(Base):
    __tablename__ = "bus_routes"
    id = Column(Integer, primary_key=True)
    bus_line_id = Column(Integer)
    route_id = Column(Integer)
    route_description = Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BusRoutePos(Base):
    __tablename__ = "bus_route_pos"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("bus_routes.route_id"), nullable=False)
    lat = Column(String)
    lon = Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BusPos(Base):
    __tablename__ = "bus_pos"
    id = Column(Integer, primary_key=True)
    bus_line_id = Column(Integer, ForeignKey("bus_lines.line_id"), nullable=False)
    bus_internal_id = Column(Integer)
    lat = Column(String)
    lon = Column(String)
    orientation = Column(Integer)
    timestamp = Column(Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BusStop(Base):
    __tablename__ = "bus_stops"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("bus_routes.route_id"), nullable=False)
    lat = Column(String)
    lon = Column(String)
    stop_code = Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BusTrip(Base):
    __tablename__ = "bus_trip"
    id = Column(Integer, primary_key=True)

    bus_line_id = Column(Integer)
    bus_internal_id = Column(Integer)

    route_id = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)
    last_pos_timestamp = Column(Integer, default=0)
