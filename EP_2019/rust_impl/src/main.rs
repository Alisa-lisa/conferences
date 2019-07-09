use std::collections::HashMap;
use rand::prelude::*;


mod core;
mod request;
mod passenger;
mod car;

fn main() {
    let mut rng = SmallRng::from_rng(thread_rng()).unwrap();
    let clock = core::Clock::new("2019-07-08T00:00:00+00:00", "2019-07-09T00:00:00+00:00");
    let mut world = core::World{clock: clock, x: 100, y: 100, cars: HashMap::new(), passengers: HashMap::new(), requests: HashMap::new()};
    for i in 1..201 {
        world.register_car(car::Car{id: i as u32, pos: (rng.gen_range(0, 100), rng.gen_range(0, 100)), free: true});
    }
    for i in 1..2001 {
        world.register_passenger(passenger::Passenger{id: i, awaiting: false, position: (rng.gen_range(0, 100), rng.gen_range(0, 100))});
    }
    world.run(false);
}
