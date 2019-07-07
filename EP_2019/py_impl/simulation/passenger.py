""" Passenger class that spawns reauests """
from uuid import uuid4
from simulation.request import Request
import random


class Passenger:
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.awaiting = False

    def update(self, x, y):
        """
        Passenger does something, right now spawns request with a random chance
        :return: None or Request
        """

        if not self.awaiting:
            if bool(random.choice([0, 1])):
                self.awaiting = True
                return Request(uuid4(),
                               self.id,
                               self.position,
                               (random.randint(0, x), random.randint(0, y)))
            return None

def spawn_passengers(number, x, y):
    res = {}
    for i in range(1, number + 1):
        res[i] = Passenger(i,(random.randint(0, x), random.randint(0, y)))
    return res
