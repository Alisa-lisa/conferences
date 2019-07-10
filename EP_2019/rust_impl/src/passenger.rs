use rand::prelude::*;
use uuid::Uuid;

use crate::request;

pub struct Passenger {
    // Passenger object
    //
    // id: u32 unique identifyer of the user
    // awaiting: bool user wants a car
    // position: (u32, u32)
    // current_request: optional id of the request that this user opned
    pub id: u32,
    pub awaiting: bool,
    pub position: (u32, u32),
}

impl Passenger {
    pub fn update(&mut self, rng: &mut SmallRng, x: u32, y: u32) -> Option<request::Request> {
        // update function called in env::update
        //
        // Return optional request
        //
        // rng: SmallRng to choose to take a taxi to a destination
        // tick: u32 clock.now for request ceration if needed
        let mut res = None;
        if !self.awaiting {
            if rng.gen_bool(1.0 / 5.0) {
                self.awaiting = true;
                res = Some(request::Request{id: Uuid::new_v4(),
                passenger: self.id.clone(),
                car_id: None,
                in_progress: false,
                picked: false,
                finished: false,
                lifetime: rng.gen_range(60, 300) as u64,
                execution_time: rng.gen_range(300, 1800) as u64,
                pickup: self.position.clone(),
                destination: (rng.gen_range(0, x), rng.gen_range(0, y))});
            }
        }
        res
    }
}

