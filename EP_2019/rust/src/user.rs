/**
 * User logic, update, value function
 */
use rand::prelude::*;
use std::collections::HashMap;
use num::clamp;
use uuid::Uuid;
use chrono::{Utc};

use crate::request;

pub struct User {
    pub id: u32,
    pub determination: bool,
    pub pos: (f32, f32),
    pub picked: bool,
    pub current_request: Option<String>,
}

impl User {
    /** choose random location on the map not equal to current position */
    pub fn want_to_drive(&mut self, rng: &mut SmallRng) -> (f32, f32) {
        let mut dest = (rng.gen_range(0.0, 800.0), rng.gen_range(0.0, 600.0));
        while dest.0 == self.pos.0 && dest.1 == self.pos.1 {
            dest = (rng.gen_range(0.0, 800.0), rng.gen_range(0.0, 600.0));
        }
        self.determination = true;
        dest
    }

    pub fn random_walk(&mut self, rng: &mut SmallRng) {
        let should_move_x_axis = rng.gen_bool(1.0 / 10.0);
        let should_move_y_axis = rng.gen_bool(1.0 / 10.0);
        if should_move_x_axis {
            let new_x_pos = self.pos.0 + rng.choose(&[-1.0, 1.0]).unwrap();
            self.pos.0 = clamp(new_x_pos, 0.0, 800.0);
        }
        else if should_move_y_axis {
            let new_y_pos = self.pos.1 + rng.choose(&[-1.0, 1.0]).unwrap();
            self.pos.1 = clamp(new_y_pos, 0.0, 600.0) as f32;
        }
    }

    pub fn spawn_request(&mut self, rng: &mut SmallRng, tick: u32) -> request::Request {
        // create a request if decided to go somewhere
        let dest = self.want_to_drive(rng);
        let req = request::Request{id: Uuid::new_v4().to_string(),
            usr_id: self.id,
            car_id: None,
            status: request::Status::Open,
            pickup: self.pos, dropoff: dest, 
            created: Utc::now(),
            picked: false,
            created_tick: tick,
            lifetime: rng.gen_range(300, 620)};
        req
    }

    pub fn update(&mut self, rng: &mut SmallRng, tick: u32) -> Option<request::Request> {
        let mut res = None;
        if !self.determination {
            let take_a_car = rng.gen_bool(1.0 / 1.0);
            if !take_a_car {
                self.random_walk(rng);
            }
            else {
                let req = self.spawn_request(rng, tick);
                self.determination = true;
                self.current_request = Some(req.clone().id);
                res = Some(req);
            }
        }
        res
    }
}

pub fn spawn(number: u32, rng: &mut SmallRng) -> HashMap<u32, User> {
    let mut res = HashMap::new();
    for u in 1..number+1 {
        res.insert(u, User{id: u, determination: false, 
            pos: (rng.gen_range(0.0, 800.0), 
                  rng.gen_range(0.0, 600.0)), 
            picked: false, current_request: None});

    }
    res
}
