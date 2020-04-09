import time
import numpy

from logger import log
from models import BusTrip

from core.pos import Pos
from core.route import Route

from geopy.distance import geodesic
from sklearn.linear_model import LinearRegression


class LinearRegressionException(Exception):
    pass


class Trip(object):
    def __init__(self, session, bus_line_id, bus_internal_id):
        self.session = session
        self.bus_line_id = bus_line_id
        self.bus_internal_id = bus_internal_id

        self.route_handler = Route(self.session, self.bus_line_id)

    '''
    Return a trip object related to a bus_internal_id
    '''
    @property
    def last_trip(self):
        return self.session.query(BusTrip).filter(
            BusTrip.bus_internal_id == self.bus_internal_id,
            BusTrip.bus_line_id == self.bus_line_id
        ).first()

    @property
    def last_trip_timedelta(self):
        # We don't have record a previously recorded trip.
        # Assume a default value of 10 minutes worth of data in seconds

        if self.last_trip is None:
            return 10 * 60

        # Return the amount of seconds passed since the last trip has
        # ended so we don't overlap data from one trip to the other

        return time.time() - self.last_trip.last_pos_timestamp

    '''
    Return movement delta for the last known trip or the last few minutes worth of data

    returns a list of (TimeSince, Distance)
    '''
    # TODO: Add support for possible only-weekend routes
    @property
    def last_movement_data(self):
        routes = self.route_handler.routes

        # Pick the bus' line first route position to get deltas from
        # This will later determine if a bus is heading towards or away from there

        route_id = routes[0].get('route_id')
        route_positions = self.route_handler.get_route_positions(route_id)

        # Get lat and lon for the route's start point
        first_route_pos = (
            float(route_positions[0]['lat']),
            float(route_positions[0]['lon'])
        )

        movement_datas = list()

        pos_handler = Pos(
            self.session,
            self.bus_line_id,
            self.last_trip_timedelta
        )

        last_positions = pos_handler.get_last_internal_positions(
            self.bus_internal_id
        )

        if len(last_positions) < 2:
            # We need at least 2 historical points
            return movement_datas

        for last_pos_data in last_positions:
            last_pos = (
                float(last_pos_data['lat']),
                float(last_pos_data['lon'])
            )

            # Calculate distance between main route's start point and current historical point
            distance = geodesic(first_route_pos, last_pos)
            # Calculate time since first historical point and current historical point in seconds
            timesince = last_pos_data['timestamp'] - last_positions[0]['timestamp']

            movement_data = (timesince, distance)
            movement_datas.append(movement_data)

        return movement_datas

    '''
    Returns coeficient and intercept for last movement data
    using a linear regression model
    y = a*x + b where a = coeficient and b = intercept
    '''
    @property
    def linear_regression_model(self):
        movement_data = self.last_movement_data

        if not len(movement_data):
            raise LinearRegressionException

        x = numpy.array([x[0] for x in movement_data]).reshape((-1, 1))
        y = numpy.array([x[1].meters for x in movement_data]).reshape((-1, 1))

        model = LinearRegression().fit(x, y)
        _ = model.score(x, y)

        return (model.coef_.item(0), model.intercept_.item(0))

    def calculate_internal_bus_route(self):
        routes = self.route_handler.routes

        try:
            # Get coeficient for last movement data
            coef, _ = self.linear_regression_model
        except LinearRegressionException:
            # We couldn't fit a linear regression model,
            # return a default non-existant route
            return 0

        # If points are trending to get closer to the main route's
        # first position, then the route this bus is taking is the *opposite*

        if coef < 0:
            return routes[-1]['route_id']

        # Otherwise the bus is taking the main route
        return routes[0]['route_id']
