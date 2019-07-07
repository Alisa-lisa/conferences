from car import Car, spawn_drivers
from passenger import spawn_passengers
from core import World, Clock

conf = {
    "x": 100,
    "y": 100
}

clock = Clock("2019-07-08T00:00:00", "2019-07-09T00:00:00")

if __name__ == '__main__':
    world = World([conf['x'], conf['y']], clock=clock)
    world.register_drivers(spawn_drivers(1, conf['x'], conf['y']))
    world.register_passengers(spawn_passengers(2, conf['x'], conf['y']))
    world.run(log=False)
