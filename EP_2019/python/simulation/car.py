""" Basic car class """

class Car:
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
