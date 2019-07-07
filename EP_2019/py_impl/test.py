import unittest
from simulation.core import Clock, World
from simulation.car import spawn_drivers
from simulation.passenger import spawn_passengers


class TestClock(unittest.TestCase):

    def test_tick(self):
        clk = Clock("2019-07-08T00:00:00", "2019-07-09T00:00:00")
        self.assertEqual(clk.now, 0)

        clk.tick()
        self.assertEqual(clk.now, 1)


    def test_representation(self):
        clk = Clock("2019-07-08T00:00:00", "2019-07-09T00:00:00")
        for _ in range(10):
            clk.tick()
        self.assertEqual(clk.current_time_formatted(), "2019-07-08T00:00:10")


class TestSimulation(unittest.TestCase):

    def test_run_world(self):
        clock = Clock("2019-07-08T00:00:00", "2019-07-08T00:00:10")
        world = World([100, 100], clock=clock)
        world.register_drivers(spawn_drivers(1, 100, 100))
        world.register_passengers(spawn_passengers(2, 100, 100))
        self.assertFalse(world.requests["pending"])

        world.run(log=False)

        self.assertTrue(world.requests["pending"] or world.requests["progress"])


if __name__ == '__main__':
    unittest.main()
