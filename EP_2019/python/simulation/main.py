from car import Car, spawn_drivers
from passenger import spawn_passengers
from core import World, Clock

conf = {
    "x": 100,
    "y": 100
}

clock = Clock("2019-07-08T00:00:00", "2019-07-08T00:09:00")

if __name__ == '__main__':
    world = World([conf['x'], conf['y']], clock=clock)
    world.register_drivers(spawn_drivers(1, conf['x'], conf['y']))
    world.register_passengers(spawn_passengers(2, conf['x'], conf['y']))
    world.run()

# TODO: io reporting
# TODO: function dispatch logic
# TODO: improve driver acceptance behaviour
# TODO: improve driver spawn
# TODO: config
# TODO: add positions + filter