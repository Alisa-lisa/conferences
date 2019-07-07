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


    def run(self):
        while not self.clock.is_last_tick():
            # spawn requests from users

            for p_id, p in self.passengers.items():
                req = p.update(self.world_x, self.world_y)
                if req is not None:
                    self.requests["pending"][req.id] = req

            print("tick {}".format(self.clock.now))
            print("pending requests {}".format(len(self.requests["pending"].keys())))

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

            # change state of the assigned requests and cars
            # TODO: put into one update state function
            for r_id in assigned_req:
                self.requests["progress"][r_id] = self.requests["pending"][r_id]
                del self.requests["pending"][r_id]

            for c_id in assigned_car:
                self.cars["occupied"][c_id] = self.cars["free"][c_id]
                del self.cars["free"][c_id]


            print("free cars left {}".format(self.cars["free"]))
            print("assigned requests {}".format(len(self.requests["progress"].keys())))
            print("pending requests {}".format(len(self.requests["pending"].keys())))


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
                if req.execution_time <= 0:
                    finished_req.append(req_id)
                    freed_cars.append(req.driver_id)
            cancelled_req = []
            for req_id, req in self.requests["pending"].items():
                if req.lifetime <= 0:
                    cancelled_req.append(req_id)
                    freed_cars.append(req.driver_id)


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

            print("fulfilled requests {}".format(len(self.requests["finished"].keys())))
            print("cancelled requests {}".format(len(self.requests["cancelled"].keys())))

            print(freed_cars)
            for c_id in freed_cars:
                self.cars["free"][c_id] = self.cars["occupied"][c_id]
                del self.cars["occupied"][c_id]




                        #     for req_id in self.active_req.keys():
        #         if not self.active_req[req_id].progress and not self.active_req[req_id].finished:
        #             if self.free_drivers:
        #                 new_request = self.active_req[req_id]
        #                 new_request.driver_id = self.free_drivers[0]
        #                 new_request.progress = True
        #                 self.active_req[req_id] = new_request
        #                 del self.free_drivers[0]
        #             else:
        #                 pass  # we wait
        #         else:
        #             # pickup
        #             new_driver = self.all_drivers[self.active_req[req_id].driver_id]
        #             new_driver.position = self.active_req[req_id].pickup
        #             self.all_drivers[self.active_req[req_id].driver_id] = new_driver
        #             self.active_req[req_id].picked = True
        #
        #             # deliver
        #             # update driver
        #             new_driver.position = self.active_req[req_id].destination
        #             new_driver.free = True
        #             self.all_drivers[self.active_req[req_id].driver_id] = new_driver  # not a smart update of a drivers structure
        #             self.free_drivers.append(self.active_req[req_id].driver_id)
        #             # update passenger
        #             new_passenger = self.passengers[self.active_req[req_id].passenger]
        #             new_passenger.position = self.active_req[req_id].destination
        #             self.passengers[self.active_req[req_id].passenger] = new_passenger
        #             # update request
        #             self.active_req[req_id].progress = False
        #             self.active_req[req_id].finished = True
        #             delivered.append(self.active_req[req_id].passenger)
        #
        #             # report request
        #             if self.active_req[req_id] not in self.requests[self.active_req[req_id].passenger]:
        #                 self.requests[self.active_req[req_id].passenger].append(self.active_req[req_id])
        #     self.awaiting = [x for x in self.awaiting if x not in delivered]
        #
        #     count -= 1
        # print("_______________________")
        # print("End state:")
        # for p, v in self.requests.items():
        #     print("Requests for passenger {}".format(p))
        #     for req in v:
        #         print("Request: {}".format(req.to_string()))


            # update simulation time
            self.clock.tick()
