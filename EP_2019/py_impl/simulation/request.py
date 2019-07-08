""" Basic data sctucture to tie a car and a user together """
import random


class Request:
    def __init__(self, id, passenger, pickup, destination):
        """
        Request constructor
        Fields:
        :picked: if the assigned car already has the passenger
        :finished: passenger was dropped off
        :lifetime: time to cancel the request if not put into progress
        :execution_time: how long a ride will take (simple movement proxy)

        :param id: unique identifier
        :param passenger: passenger id that spawned the request
        :param pickup: tuple position of the passenger to be picked up from
        :param destination: tuple position where passenger wants to go
        """
        self.id = id
        self.passenger = passenger
        self.destination = destination
        self.driver_id = -1
        self.progress = False
        self.picked = False
        self.finished = False
        self.lifetime = random.randint(60, 60*5)
        self.execution_time = random.randint(5*60, 30*60)
