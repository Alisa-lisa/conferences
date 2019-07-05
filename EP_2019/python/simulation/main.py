from .car import Car
from .passenger import Passenger
from .core import World, Clock

HEIGHT = 100
WIDTH =100

clock = Clock("2019-07-08T00:00:00", "2019-07-08TOO:O2:00")

if __name__ == '__main__':
    world = World([WIDTH, HEIGHT], clock=clock)
    world.register_drivers(Car.spawn_drivers(5, WIDTH, HEIGHT))
    world.register_passengers(Passenger.spawn_passengers(15, WIDTH, HEIGHT))
    world.run()

# TODO: io reporting
# TODO: function dispatch logic
# TODO: improve driver acceptance behaviour
# TODO: improve driver spawn
# TODO: config
# TODO: add positions + filter