import time
from models import BusPos


class Pos(object):
    def __init__(self, session, bus_line_id, time_delta=35):
        self.session = session
        self.bus_line_id = bus_line_id
        self.time_delta = time_delta

    @property
    def ts_delta(self):
        return int(time.time()) - self.time_delta

    @property
    def last_positions(self):
        last_pos_all = self.session.query(BusPos).filter(
            BusPos.timestamp > self.ts_delta,
            BusPos.bus_line_id == self.bus_line_id
        ).all()

        return [x.as_dict() for x in last_pos_all]

    @property
    def last_active_internals(self):
        return set([x['bus_internal_id'] for x in self.last_positions])

    def get_last_internal_positions(self, bus_internal_id):
        # TODO: Make a geofence around every route's first position
        # and ignore data from inside the fence

        last_pos_internals = self.session.query(BusPos).filter(
            BusPos.timestamp > self.ts_delta,
            BusPos.bus_line_id == self.bus_line_id,
            BusPos.bus_internal_id == bus_internal_id
        ).all()

        return [x.as_dict() for x in last_pos_internals]
