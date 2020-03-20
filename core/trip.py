import time
from models import BusPos

class Trip(object):
    def __init__(self, session, bus_line_id, bus_internal_id, trip_delta=10):
        self.session = session
        self.bus_line_id = bus_line_id
        self.bus_internal_id = bus_internal_id
        self.trip_delta = trip_delta

    '''
    Return a bus' last positions for self.trip_delta in seconds (default: 10 seconds)
    '''
    @property
    def last_positions(self):
        delta_ts = time.time() - self.trip_delta

        query = self.session.query(BusPos).filter(
            BusPos.timestamp > delta_ts,
            BusPos.bus_internal_id == self.bus_internal_id,
            BusPos.bus_line_id == self.bus_line_id
        ).order_by(
            BusPos.timestamp.desc()
        )

        return query.all()
