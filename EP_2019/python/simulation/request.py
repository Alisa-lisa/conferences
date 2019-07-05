""" Basic data sctucture to tie a car and a user together """

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
        return "Id: {}, passenger: {}, " \
               "driver: {}," \
               " progress: {}, " \
               "picked: {}, " \
               "finished: {}".format(self.id,
                                     self.passenger,
                                     self.driver_id,
                                     self.progress,
                                     self.picked,
                                     self.finished)
