""" World - container class tying all together """
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

class Clock:
    """
    Control simulation time line
    """
    def __init__(self, start, end):
        """
        Set simulation time line
        :param start: str datetime ISO
        :param end: str datetime ISO
        """
        self.step = 1
        self.unit = "s"
        self.start = parse(start)
        self.end = parse(end)
        self.now = 0
        self.num_ticks = self.get_steps()

    def get_steps(self):
        """
        Computes total amount of steps simulation has
        :return: int
        """
        return (self.end - self.start).seconds


    def tick(self):
        """
        Increase simulation time by 1 unit
        :return: None
        """
        self.now += 1

    def is_last_tick(self):
        """
        Check if clock can be stopped
        :return: bool
        """
        return self.now >= self.num_ticks

    def current_time_formatted(self):
        """
        Return current clock tick as string timestamp
        :return: str
        """
        m_r, s = divmod(self.now, 60)
        h_r, m = divmod(m_r, 60)
        d_r, h = divmod(h_r, 24)
        m_r, d = divmod(d_r, 30)
        return (self.start + relativedelta(days=d, hours=h, minutes=m, second=s)).isoformat()


class World:
    def __init__(self, size, clock):
        self.clock = clock
        self.world_x = int(size[0])
        self.world_y = int(size[1])
        self.cars = {
            "free": {},
            "occupied": {}
        }
        self.passengers = {}
        self.requests = {
            "pending": {},
            "progress": {},
            "finished": {},
            "cancelled": {}
        }

    def register_drivers(self, drivers):
        self.cars["free"] = drivers

    def register_passengers(self, passengers):
        self.passengers = passengers


    def run(self, log=True):
        while not self.clock.is_last_tick():
            # spawn requests from users
            for p_id, p in self.passengers.items():
                req = p.update(self.world_x, self.world_y)
                if req is not None:
                    self.requests["pending"][req.id] = req

            # start assigning pending requests to cars
            free_tmp = list(self.cars["free"].keys())
            assigned_req = []
            assigned_car = []
            for req_id, req in self.requests["pending"].items():
                if free_tmp:
                    id = free_tmp.pop(-1)
                    req.driver_id = id
                    req.progress = True
                    assigned_req.append(req.id)
                    assigned_car.append(id)
                    print(self.clock.now)
                    print("At {} Request {} was assigned to a car {}".format(self.clock.current_time_formatted(),
                                                                             req_id, id))

            # change state of the assigned requests and cars
            # TODO: put into one update state function
            for r_id in assigned_req:
                self.requests["progress"][r_id] = self.requests["pending"][r_id]
                del self.requests["pending"][r_id]

            for c_id in assigned_car:
                self.cars["occupied"][c_id] = self.cars["free"][c_id]
                del self.cars["free"][c_id]

            # TODO: put it into request update function
            # "move" requests that are in progress
            for req in self.requests["progress"].values():
                req.execution_time -= self.clock.step
            # update requests that can be cancelled
            for req in self.requests["pending"].values():
                req.lifetime -= self.clock.step

            # check on progress or cancellation
            finished_req = []
            freed_cars = []
            for req_id, req in self.requests["progress"].items():
                if req.execution_time == 0:
                    finished_req.append(req_id)
                    freed_cars.append(req.driver_id)
                    print(self.clock.now)
                    print("At {} Request {} was fulfilled".format(self.clock.current_time_formatted(), req_id))
            cancelled_req = []
            for req_id, req in self.requests["pending"].items():
                if req.lifetime == 0:
                    cancelled_req.append(req_id)
                    print(self.clock.now)
                    print("At {} Request {} was cancelled".format(self.clock.current_time_formatted(), req_id))

            # TODO: global update function
            for r_id in finished_req:
                if r_id in self.requests["progress"].keys():
                    self.requests["finished"][r_id] = self.requests["progress"][r_id]
                    del self.requests["progress"][r_id]
                elif r_id in self.requests["pending"].keys():
                    self.requests["cancelled"][r_id] = self.requests["pending"][r_id]
                    del self.requests["pending"][r_id]
                else:
                    print("WTF")

            # update cars state
            for c_id in freed_cars:
                self.cars["free"][c_id] = self.cars["occupied"][c_id]
                del self.cars["occupied"][c_id]

            self.clock.tick()
