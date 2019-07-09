from simulation.car import spawn_drivers
from simulation.passenger import spawn_passengers
from simulation.core import World, Clock

conf = {
    "x": 100,
    "y": 100,
    "drivers": 200,
    "users": 1000,
    "start": "2019-07-08T00:00:00",
    "end": "2019-07-08T00:01:00"
}

clock = Clock(conf["start"], conf["end"])

if __name__ == '__main__':
    world = World([conf['x'], conf['y']], clock=clock)
    world.register_drivers(spawn_drivers(conf["drivers"], conf['x'], conf['y']))
    world.register_passengers(spawn_passengers(conf["users"], conf['x'], conf['y']))
    world.run(log=False)
