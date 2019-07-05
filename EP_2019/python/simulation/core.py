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
        return (self.start + relativedelta(second=self.now)).isoformat()


class World:
    def __init__(self, size, clock):
        self.clock = clock
        self.world_x = int(size[0])
        self.world_y = int(size[1])
        self.all_drivers = {}
        self.free_drivers = []
        self.passengers = {}
        self.requests = {
            "pending": {},
            "progress": {},
            "finished": {}
        }

    def register_drivers(self, drivers):
        self.all_drivers = drivers
        self.free_drivers = list(self.all_drivers.keys())

    def register_passengers(self, passengers):
        self.passengers = passengers


    def run(self):
        while not self.clock.is_last_tick():

            for p_id, p in self.passengers:
                req = p.update()
                if req is not None:
                    self.requests["pending"][req.id] = req


            for req_id, req in self.requests["pending"].items():


            # assign driver to a request
            for req_id in self.active_req.keys():
                if not self.active_req[req_id].progress and not self.active_req[req_id].finished:
                    if self.free_drivers:
                        new_request = self.active_req[req_id]
                        new_request.driver_id = self.free_drivers[0]
                        new_request.progress = True
                        self.active_req[req_id] = new_request
                        del self.free_drivers[0]
                    else:
                        pass  # we wait
                else:
                    # pickup
                    new_driver = self.all_drivers[self.active_req[req_id].driver_id]
                    new_driver.position = self.active_req[req_id].pickup
                    self.all_drivers[self.active_req[req_id].driver_id] = new_driver
                    self.active_req[req_id].picked = True

                    # deliver
                    # update driver
                    new_driver.position = self.active_req[req_id].destination
                    new_driver.free = True
                    self.all_drivers[self.active_req[req_id].driver_id] = new_driver  # not a smart update of a drivers structure
                    self.free_drivers.append(self.active_req[req_id].driver_id)
                    # update passenger
                    new_passenger = self.passengers[self.active_req[req_id].passenger]
                    new_passenger.position = self.active_req[req_id].destination
                    self.passengers[self.active_req[req_id].passenger] = new_passenger
                    # update request
                    self.active_req[req_id].progress = False
                    self.active_req[req_id].finished = True
                    delivered.append(self.active_req[req_id].passenger)

                    # report request
                    if self.active_req[req_id] not in self.requests[self.active_req[req_id].passenger]:
                        self.requests[self.active_req[req_id].passenger].append(self.active_req[req_id])
            self.awaiting = [x for x in self.awaiting if x not in delivered]

            count -= 1
        print("_______________________")
        print("End state:")
        for p, v in self.requests.items():
            print("Requests for passenger {}".format(p))
            for req in v:
                print("Request: {}".format(req.to_string()))