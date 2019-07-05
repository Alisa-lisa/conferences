""" Passenger class that spawns reauests """
from uuid import uuid4
from .request import Request
import random


class Passenger:
    def __init__(self, position):
        self.id = uuid4()
        self.position = position
        self.awaiting = False

    def to_string(self):
        return "Passenger. Id: {}, position: {}".format(self.id, self.position)

    @staticmethod
    def spawn_passenger(passenger_id, position):
        p = Passenger(position)
        p.id = passenger_id
        return p

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

    def update(self):
        """
        Passenger does something, right now spawns request with a random chance
        :return: None or Request
        """

        if not self.awaiting:
            if bool(random.choice([0, 1])):
                self.awaiting = True
                return self.spawn_request(uuid4(),
                                          (random.randint(0, self.world_x),
                                          random.randint(0, self.world_x)))
            return None