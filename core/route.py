from models import BusRoute, BusRoutePos, BusStop


class Route(object):
    def __init__(self, session, bus_line_id):
        self.session = session
        self.bus_line_id = bus_line_id

    @property
    def routes(self):
        routes = self.session.query(BusRoute).filter(
            BusRoute.bus_line_id == self.bus_line_id
        ).all()

        result = []

        for route in routes:
            result.append(route.as_dict())

        return result

    def get_route(self, route_id):
        route = self.session.query(BusRoute).filter(
            BusRoute.route_id == route_id
        ).first()

        if route is None:
            return {}

        return route.as_dict()

    def get_route_positions(self, route_id):
        routes = self.session.query(BusRoutePos).filter(
            BusRoutePos.route_id == route_id
        ).order_by(
            BusRoutePos.id.asc()
        ).all()

        result = []

        for route in routes:
            result.append(route.as_dict())

        return result

    def get_route_stops(self, route_id):
        stops = self.session.query(BusStop).filter(
            BusStop.route_id == route_id
        ).order_by(
            BusStop.id.asc()
        ).all()

        result = []

        for stop in stops:
            result.append(stop.as_dict())

        return result
