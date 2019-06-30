use rand::prelude::*;
use std::collections::HashMap;
use crate::request;

#[derive(Clone, Debug)]
pub struct Driver {
    pub id: u32,
    pub pos: (f32, f32),
    pub occupied: bool,
}

impl Driver {
    // helper function to identify the direction and make a step
    pub fn step(&mut self, dest: (f32, f32)) {
        println!("Old location {}/{}", self.pos.0, self.pos.1);
        let x_direction = dest.0 as i32 - self.pos.0 as i32;
        if x_direction != 0 {
            if x_direction < 0 {
                self.pos.0 -= 1.0 as f32;
            }
            else {
                self.pos.0 += 1.0 as f32;
            }
        }
        let y_direction = dest.1 as i32 - self.pos.1 as i32;
        if y_direction != 0 {
            if y_direction < 0 {
                self.pos.1 -= 1.0 as f32;
            }
            else {
                self.pos.1 += 1.0 as f32;
            }
        }
        println!("New location {}/{}", self.pos.0, self.pos.1);
    }

    pub fn accept_request(&mut self) {
        self.occupied = true
    }

}

pub fn spawn(number: u32, rng: &mut SmallRng) -> HashMap<u32, Driver> {
    let mut res = HashMap::new();
    for d in 1..number+1 {
        res.insert(d, Driver{id: d, pos: (rng.gen_range(0.0, 800.0), rng.gen_range(0.0, 600.0)), occupied: false});
    }
    res
}

/** collect all driver ids that are currently free */
pub fn get_free_drivers(drivers: &mut HashMap<u32, Driver>) -> Vec<u32> {
    let mut res = Vec::new();
    for (id, ref driver) in drivers.iter() {
        if !driver.occupied {
            res.push(*id);
        }
    }
    res
}
