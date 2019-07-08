""" Basic car class """
import random


class Car:
    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.free = True


def spawn_drivers(number, x, y):
    res = {}
    for i in range(1, number + 1):
        position = (random.randint(0, x), random.randint(0, y))
        res[i] = Car(id=i, position=position)
    return res
