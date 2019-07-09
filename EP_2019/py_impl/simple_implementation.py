from uuid import uuid4
import numpy as np


class Request:
    def __init__(self):
        """
        Request constructor

        :id: unique identifier
        :driver: assigned driver
        :lifetime: time to cancel the request if not put into progress
        :execution_time: how long a ride will take (simple movement proxy)
        """
        self.id = uuid4()
        self.driver_id = None
        self.remaining_waiting_time = 100
        # self.remaining_waiting_time = random.randint(60, 60*5)
        # self.fulfillment_time = random.randint(5*60, 30*60)
        self.fulfillment_time = 100

    def is_alive(self):
        """ Checks if request has some time  to exist or be fulfilled """
        return self.remaining_waiting_time > 0 and self.fulfillment_time > 0


class Taxi:
    def __init__(self):
        self.id = uuid4()
        self.is_occupied = False


class World:
    def __init__(self, runtime, spawn_chance, max_active, taxis):
        self.runtime = runtime
        self.age = 0
        self.request_spawn_chance = spawn_chance
        self.max_active_requests = max_active
        self.taxis = {
            "free": [Taxi() for _ in range(taxis)],
            "occupied": []
        }
        self.requests = {
            "pending": [],
            "progress": [],
            "finished": [],
            "cancelled": []
        }

    def maybe_spawn_request(self):
        """ Spawn a request with a chance """
        p = [1 - self.request_spawn_chance, self.request_spawn_chance]
        if (len(self.requests["pending"]) + len(self.requests["progress"]) < self.max_active_requests)\
                and np.random.choice([False, True], p=p):
            self.requests["pending"].append(Request())

    def distribute_unfulfilled_requests(self):
        """ Try to assign a request to a car """
        for r in self.requests["pending"]:
            if len(self.taxis["free"]) > 0:
                taxi = self.taxis["free"][0]
                taxi.is_occupied = True
                r.driver_id = taxi
                self.taxis["free"].remove(taxi)
                self.taxis["occupied"].append(taxi)
                self.requests["progress"].append(r)
        self.requests["pending"] = [r for r in self.requests["pending"] if r not in self.requests["progress"]]

    def update_requests(self):
        """ Count down to request state change """
        for r in self.requests["pending"]:
            r.remaining_waiting_time -= 1
        for r in self.requests["progress"]:
            r.fulfillment_time -= 1

    def cleanup_requests(self):
        """ Change state of the request """
        for r in self.requests["pending"]:
            if not r.is_alive():
                self.requests["cancelled"].append(r)
        self.requests["pending"] = [r for r in self.requests["pending"] if r not in self.requests["cancelled"]]

        for r in self.requests["progress"]:
            if not r.is_alive():
                self.requests["finished"].append(r)
                self.taxis["free"].append(r.driver_id)
                self.taxis["occupied"].remove(r.driver_id)
        self.requests["progress"] = [r for r in self.requests["progress"] if r not in self.requests["finished"]]

    def run_till_done(self):
        """ Main loop with all steps from the scenario """
        while self.age <= self.runtime:
            self.age += 1

            self.maybe_spawn_request()
            self.distribute_unfulfilled_requests()
            self.update_requests()
            self.cleanup_requests()

            # print("Age: {}/{}, Taxis: {} Occ/{} Free, Requests: {} Asnd/{} Wai/{} Cld/{} Fin".format(self.age,
            #                                                                                   self.runtime,
            #                                                                                   len(self.taxis["occupied"]),
            #                                                                                   len(self.taxis["free"]),
            #                                                                                   len(self.requests["pending"]),
            #                                                                                         len(self.requests["progress"]),
            #                                                                                         len(self.requests["cancelled"]),
            #                                                                                         len(self.requests["finished"])))

if __name__ == '__main__':
    world = World(86400, 0.2, 2000, 200)
    world.run_till_done()
