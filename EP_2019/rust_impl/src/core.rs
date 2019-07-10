/// main module binding everyting together
use std::collections::HashMap;
use rand::prelude::*;
use uuid::Uuid;
use chrono::{DateTime, FixedOffset};

use crate::car;
use crate::passenger;
use crate::request;

pub struct Clock {
    /// Clock is responsible for the timeline of the simulation
    ///
    /// ### Parameters:
    /// - step: u16 smallest time unit step on the time line
    /// - unit: String time unit applicable for the step
    /// - start: chrono::DateTime start of the simulation time line
    /// - end: chrono::DateTime end of the simulation time line
    /// - now: u64 index of the current step on the timeline
    /// - number_ticks: u64 total number of steps the simulation will be running
    pub step: u16,
    pub unit: String,
    // pub start: String,
    //pub end: String,
    pub start: DateTime<FixedOffset>,
    pub end: DateTime<FixedOffset>,
    pub now: u64,
    pub max_number_ticks: u64,
}

impl Clock {
    /// Proper Clock creation withh all values set
    ///
    /// Parameters:
    /// - start: String date time in RFC 3339 format
    /// - end: String date time in RFC 3339 format
    ///
    /// Return: Clock
    pub fn new(start: &str, end: &str) -> Clock {
        let s = DateTime::parse_from_rfc3339(&start).expect("Parsing went wrong");
        let e = DateTime::parse_from_rfc3339(&end).expect("Parsing went wrong");
        let delta = e - s;
        println!("{}", delta.num_seconds());
        let clock = Clock{step: 1, unit: "s".to_string(), start: s, end: e, now: 0, max_number_ticks: delta.num_seconds() as u64};
        clock
    }

    /// Move step further on the timeline
    pub fn tick(&mut self) {
        self.now = self.now + self.step as u64;
    }

    /// Checks if the are any steps left on the timeline
    pub fn is_finished(&mut self) -> bool {
        self.now >= self.max_number_ticks
    }

    /// Present current step as a human readable String
    ///
    /// Return date time string in RFC_3399 format
    pub fn current_time_formatted(&mut self) -> String {
        format!("Tick {} is {}", self.now, "TODO")
    }
}

pub struct World {
    /// World is a container bindign everyting together
    ///
    /// ### Parameters:
    /// - clock: Clock to keep track of the timeline
    /// - x: u32 width of the box
    /// - y: u32 height of the box
    /// - cars: HashMap<u32, Car> all cars present in the simulation
    /// - passenger: HashMap<u32, Passenger> all passenger present in the simulation
    /// - requests: HashMap<uuid, Request> all requests created by the passengers
    pub clock: Clock,
    pub x: u32,
    pub y: u32,
    pub cars: HashMap<u32, car::Car>,
    pub passengers: HashMap<u32, passenger::Passenger>,
    pub requests: HashMap<Uuid, request::Request>,
}

impl World {
    pub fn register_car(&mut self, car: car::Car) {
        // Create supply for simulation
        self.cars.insert(car.id.clone(), car);
    }

    pub fn register_passenger(&mut self, passenger: passenger::Passenger) {
        // Create demand for simulation
        self.passengers.insert(passenger.id.clone(), passenger);
    }

    pub fn run(&mut self, log: bool) {
        let mut rng = SmallRng::from_rng(thread_rng()).unwrap();
        // helper structures to operate on ids similar to python way
        let mut free_cars = Vec::new();
        for (i, _car) in self.cars.iter() {
            free_cars.push(i.clone());
        }
        let mut pending: Vec<Uuid> = Vec::new();
        let mut requests_in_progress: Vec<Uuid> = Vec::new();
        let mut finished: Vec<Uuid> = Vec::new();
        // Main loop of the simulation
        while !self.clock.is_finished() {
            // spawn requests from free users
            for (p_id, ref mut p) in self.passengers.iter_mut() {
                if !p.awaiting {
                    let request = p.update(&mut rng, 100, 100);
                    if request.is_some() {
                        let req = request.unwrap();
                        self.requests.insert(req.id.clone(), req.clone());
                        pending.push(req.id.clone());
                        if log {
                            println!("At {} request {} was created by passenger {}", self.clock.now, req.id.clone(), p_id);
                        }
                    }
                }
            }

            // start assigning requests to cars
            for r_id in pending.iter_mut() {
                // try to assign a request
                if free_cars.len() > 0 {
                    let car_id = free_cars.pop().unwrap();
                    self.cars.entry(car_id).and_modify(|c| c.free = false);
                    self.requests.entry(*r_id).and_modify(|r| r.in_progress = true);
                    self.requests.entry(*r_id).and_modify(|r| r.car_id = Some(car_id));
                    requests_in_progress.push(r_id.clone());
                    if log {
                        println!("At {} Request {} was assigned to a car {}", self.clock.now, r_id.clone(), car_id.clone());
                    }
                }
                // if no cars available reduce lifetime
                let lifetime = self.requests.get(&r_id).unwrap().lifetime;
                if lifetime > 0 {
                    let tick = self.clock.step.clone() as u64;
                    self.requests.entry(*r_id).and_modify(|r| r.lifetime -= tick);
                    dbg!(lifetime);
                }
                // cancell
                else {
                    self.requests.entry(*r_id).and_modify(|r| r.finished = true);
                    finished.push(*r_id);
                    let p = self.requests.get(&r_id.clone()).unwrap().passenger.clone();
                    self.passengers.entry(p).and_modify(|p| p.awaiting = false);
                    if log {
                        println!("At {} Request {} was cancelled", self.clock.now, r_id);
                    }
                }
            }
            // start requests_in_progress on assigned requests
            for r_id in requests_in_progress.iter() {
                let req = self.requests.get(r_id).unwrap();
                // finish
                println!("Request in progress {} with lifetime {}", r_id.clone(), req.clone().execution_time);
                if req.execution_time <= 0 {
                    let car_id = req.car_id.unwrap();
                    free_cars.push(car_id.clone());
                    finished.push(r_id.clone());
                    self.requests.entry(*r_id).and_modify(|r| r.finished=true);
                    if log {
                        println!("At {} Request {} was fulfilled", self.clock.now, r_id);
                    }
                }
                // "move"
                else {
                    let tick = self.clock.step as u64;
                    self.requests.entry(*r_id).and_modify(|r| r.execution_time -= tick);
                }
            }

            requests_in_progress.retain(|r| finished.contains(r));
            pending.retain(|r| finished.contains(r) || requests_in_progress.contains(r));

 /*                      if self.clock.now % 50 == 0 {
                         dbg!(self.cars.len());
                         dbg!(self.passengers.len());
                         dbg!(self.requests.len());
                         dbg!(free_cars.len());
                         dbg!(pending.len());
                         dbg!(requests_in_progress.len());
                         dbg!(finished.len());
                         dbg!(self.clock.now);
                         }
 */                        
            self.clock.tick();
        }
    }
}
