/// main module binding everyting together
use std::collections::HashMap;
use rand::prelude::*;
use uuid::Uuid;
use chrono::{DateTime, NaiveDateTime, FixedOffset};

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
    pub number_ticks: u64,
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
        let delta = (e - s);
        let clock = Clock{step: 1, unit: "s".to_string(), start: s, end: e, now: 0, number_ticks: delta.num_seconds() as u64};
        clock
    }

    pub fn tick(&mut self) {
        // Move step further on the timeline
        self.now = self.now + self.step as u64;
    }

    pub fn is_last_tick(&mut self) -> bool {
        // Checks if the are any steps left on the timeline
        self.now == self.number_ticks
    }

    pub fn current_time_formatted(&mut self) -> String {
        // Present current step as a human readable String
        //
        // Return date time string in RFC_3399 format
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
        for (i, car) in self.cars.iter() {
            free_cars.push(i.clone());
        }
        //let mut ocuppied_cars = Vec::new();
        let mut pending = Vec::new();
        let mut progress = Vec::new();
        //let mut finished = Vec::new();
        // Main loop of the simulation
        while !self.clock.is_last_tick() {
            // spawn requests from free users
            for (p_id, ref mut p) in self.passengers.iter_mut() {
                if !p.awaiting {
                    let request = p.update(&mut rng, 100, 100);
                    if request.is_some() {
                        let req = request.unwrap();
                        let id = req.id.clone();
                        self.requests.insert(id.clone(), req);
                        pending.push(id.clone());
                        if log {
                            println!("At {} request {} was created by passenger {}", self.clock.now, id.clone(), p_id);
                        }
                    }
                }
            }

            // start assigning requests to cars
            for r_id in &pending {
                // try to assign a request
                if free_cars.len() > 0 {
                    let car_id = free_cars.pop();
                    let print_id = car_id.clone().unwrap();
                    self.cars.entry(print_id.clone()).and_modify(|c| c.free = false);
                    self.requests.entry(*r_id).and_modify(|r| r.progress = true);
                    self.requests.entry(*r_id).and_modify(|r| r.car_id = car_id);
                    progress.push(r_id.clone());
                    if log {
                        println!("At {} Request {} was assigned to a car {}", self.clock.now, r_id.clone(), print_id);
                    }
                }
                // if no cars available reduce lifetime
                else {
                    let req = self.requests.get(r_id).unwrap().lifetime.clone();
                    if req > 0 {
                        let tick = self.clock.step.clone() as u64;
                        self.requests.entry(*r_id).and_modify(|r| r.lifetime -= tick);
                    }
                    // cancell
                    else {
                        self.requests.entry(*r_id).and_modify(|r| r.finished = true);
                        let p = self.requests.get(r_id).unwrap().passenger.clone();
                        self.passengers.entry(p).and_modify(|p| p.awaiting = false);
                        if log {
                            println!("At {} Request {} was cancelled", self.clock.now, r_id);
                        }
                    }
                }
            }
            // start progress on pending and assigned requests
            for (r_id, mut req) in self.requests.iter_mut() {
                if req.progress {
                    // reduce execution time or stop request execution
                    if req.execution_time <= 0 {
                        req.finished = true;
                        self.cars.entry(req.car_id.clone().unwrap()).and_modify(|c| c.free = true);
                        if log {
                            println!("At {} Request {} was fulfilled", self.clock.now, r_id);
                        }
                    }
                    else {
                        req.execution_time -= self.clock.step as u64;
                    }
                }
            }
            self.clock.tick();
        }
    }
}
