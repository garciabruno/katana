from models import BusRoute


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
            result.append(
                {
                    "route_id": route.route_id,
                    "description": route.route_description,
                }
            )

        return result
