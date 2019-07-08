use std::collections::HashMap;
use rand::prelude::*;


mod core;
mod request;
mod passenger;
mod car;

fn main() {
    //let clock = core::Clock::create("2019-07-06T00:00:00", "2019-07-06T00:00:05");
    let mut rng = SmallRng::from_rng(thread_rng()).unwrap();
    let mut clock = core::Clock{step: 1, unit: "s".to_string(), start: "2019-07-06T00:00:00".to_string(), end: "2019-07-06T00:02:00".to_string(), now: 0, number_ticks: 120};
    let mut world = core::World{clock: clock, x: 100, y: 100, cars: HashMap::new(), passengers: HashMap::new(), requests: HashMap::new()};
    for i in 1..201 {
        world.register_car(car::Car{id: i as u32, pos: (rng.gen_range(0, 100), rng.gen_range(0, 100)), free: true});
    }
    for i in 1..2001 {
        world.register_passenger(passenger::Passenger{id: i, awaiting: false, position: (rng.gen_range(0, 100), rng.gen_range(0, 100))});
    }

    world.run();
}
