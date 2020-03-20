from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BusLine(Base):
    __tablename__ = "bus_lines"
    id = Column(Integer, primary_key=True)
    line_id = Column(Integer)
    email = Column(String)


class BusRoute(Base):
    __tablename__ = "bus_routes"
    id = Column(Integer, primary_key=True)
    bus_line_id = Column(Integer)
    route_id = Column(Integer)
    route_description = Column(String)


class BusRoutePos(Base):
    __tablename__ = "bus_route_pos"
    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, ForeignKey("bus_routes.route_id"), nullable=False)
    lat = Column(String)
    lon = Column(String)


class BusPos(Base):
    __tablename__ = "bus_pos"
    id = Column(Integer, primary_key=True)
    bus_line_id = Column(Integer, ForeignKey("bus_lines.line_id"), nullable=False)
    bus_internal_id = Column(Integer)
    lat = Column(String)
    lon = Column(String)
    orientation = Column(Integer)
    timestamp = Column(Integer)


class BusStop(Base):
    __tablename__ = "bus_stops"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("bus_route.route_id"), nullable=False)
    lat = Column(String)
    lon = Column(String)
    stop_code = Column(String)


class BusTrip(Base):
    __tablename__ = "bus_trip"
    id = Column(Integer, primary_key=True)
    bus_line_id = Column(Integer, ForeignKey("bus_lines.line_id"), nullable=False)
    bus_internal_id = Column(Integer)
    route_id = Column(Integer, ForeignKey("bus_route.route_id"), nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)
