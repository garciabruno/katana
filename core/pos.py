import time
from models import BusPos

class Pos(object):
    def __init__(self, session, bus_line_id, time_delta=35):
        self.session = session
        self.bus_line_id = bus_line_id
        self.time_delta = time_delta

    @property
    def last_positions(self):
        ts_delta = int(time.time()) - self.time_delta

        last_positions = self.session.query(BusPos).filter(
            BusPos.timestamp > ts_delta,
            BusPos.bus_line_id == self.bus_line_id
        ).all()

        return last_positions


    @property
    def last_active_internals(self):
        return set([x.bus_internal_id for x in self.last_positions])
