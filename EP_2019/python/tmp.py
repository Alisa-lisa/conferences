import random
from uuid import uuid4


def repr(in_dict):
    return "\n".join(v.to_string() for v in in_dict.values())


class Passenger:
    def __init__(self, position):
        self.id = uuid4()
        self.position = position

    def to_string(self):
        return "Passenger. Id: {}, position: {}".format(self.id, self.position)

    @staticmethod
    def spawn_passenger(passenger_id, position):
        return Passenger(id=passenger_id, position=position)

    @staticmethod
    def spawn_passengers(number, x, y):
        res = {}
        for i in range(1, number + 1):
            position = (random.randint(0, x), random.randint(0, y))
            res[i] = Passenger.spawn_passenger(i, position)
        return res

    def spawn_request(self, requestid, destination):
        return Request(id=requestid,
                       passenger=self.id,
                       pickup=self.position,
                       destination=destination)


class Request:
    def __init__(self, id, passenger, pickup, destination):
        self.id = id
        self.passenger = passenger
        self.pickup = pickup
        self.destination = destination
        self.driver_id = -1
        self.progress = False
        self.picked = False
        self.finished = False

    def to_string(self):
        return "Request. Id: {}, passenger: {}, driver: {}, progress: {}, picked: {}, finished: {}".format(self.id, self.passenger, self.driver_id, self.progress, self.picked, self.finished)


class Driver:
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.free = True

    def to_string(self):
        return "Driver. Id: {}, position: {}, free: {}".format(self.id, self.position, self.free)

    @staticmethod
    def spawn_driver(driver_id, position):
        return Driver(id=driver_id, position=position)

    @staticmethod
    def spawn_drivers(number, x, y):
        res = {}
        for i in range(1, number + 1):
            position = (random.randint(0, x), random.randint(0, y))
            res[i] = Driver.spawn_driver(i, position)
        return res

class World:
    def __init__(self, size):
        self.world_x = int(size[0])
        self.world_y = int(size[1])
        self.free_drivers, self.all_drivers, self.passengers, self.requests, self.active_req, self.awaiting = self.setup()

    def setup(self):
        all_drivers = Driver.spawn_drivers(5, self.world_x, self.world_y)
        free_drivers = list(all_drivers.keys())

        passengers = Passenger.spawn_passengers(5, self.world_x, self.world_y)
        all_requests = {}
        for pid in passengers.keys():
            all_requests[pid] = []
        active_requests = {}
        passengers_awaiting = []

        print("____________________")
        return free_drivers, all_drivers, passengers, all_requests, active_requests, passengers_awaiting

    def random_request_spawn(self):
        for passenger in self.passengers.keys():
            if passenger not in self.awaiting:
                if bool(random.choice([0, 1])):
                    req_id = 1
                    if self.active_req:
                        req_id = max(self.active_req.keys()) + 1
                    request = self.passengers[passenger].spawn_request(req_id, (random.randint(0, self.world_x), random.randint(0, self.world_x)))
                    self.active_req[req_id] = request
                    self.awaiting.append(passenger)

    def run(self):
        count = 100  # TODO: proper duration flag
        while count > 0:
            delivered = []
            # with a chance a passenger spawns a request. One request per passenger at a time
            self.random_request_spawn()
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


if __name__ == '__main__':
    world = World([100, 100])
    world.run()

# TODO: io reporting
# TODO: function dispatch logic
# TODO: improve driver acceptance behaviour
# TODO: improve driver spawn
# TODO: config
# TODO: add positions + filter