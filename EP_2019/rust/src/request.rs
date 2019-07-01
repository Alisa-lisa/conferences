//! Request object: keeps an eye on interaction between users and cars
use chrono::prelude::{DateTime, Utc};
use uuid::Uuid;
use std::fmt; 

#[derive(PartialEq, Debug, Clone)]
pub enum Status {
    // Request can be in several states of execution
    //
    // Open: no progress, car is not assigned
    // Progress: car is benig assigned and is moving
    // Finished: request is successfully closed, passenger moved
    // Cancelled: request expired before car assignment
    Open,
    Progress,
    Finished,
    Cancelled,
}

impl fmt::Display for Status {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
       match *self {
           Status::Open => write!(f, "open"),
           Status::Progress => write!(f, "progress"),
           Status::Finished => write!(f, "finish"),
           Status::Cancelled => write!(f, "cancell"),
       }
    }
}

#[derive(Debug, Clone)]
pub struct Request {
    // Main object controlling the logic flow
    //
    // id: unique identifyer of the Request
    // usr_id : u32 id uo user spawned this requrest
    // car_id: u32 id of the assigned car, is None untill assigned
    // status: enum progress of the request
    // pickup: tuple of f32 coordinates
    // dropoff: tuple of f32 coordinates
    // picked: bool is the passenger being transported
    // cerated_tick: u32 clock step when the request was spawned
    // lifetime: u32 how long a passenger can wait untill the request is assigned to a car
    pub id: u32,
    pub usr_id: u32,
    pub car_id: Option<u32>,
    pub status: Status,
    pub pickup: (f32, f32),
    pub dropoff: (f32, f32),
    pub picked: bool,
    pub created_tick: u32,
    pub lifetime: u32,
}

// implementing format trait for custom object
impl fmt::Display for Request {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
       if self.car_id.is_some() {
           let s = format!("{}", self.car_id.clone().unwrap());
           write!(f, "{}", s)
       }
       else {
           write!(f, "None")
       }
    }
}


impl Request {
    // move request to the next state (O->P->F)
    pub fn next_phase(&mut self) {
        if self.status == Status::Open {
            self.status = Status::Progress;
        }
        else if self.status == Status::Progress {
            self.status = Status::Finished;
        }
    }

    // cehck if the request changes states
    pub fn update(&mut self) {
        // no acceptance
        if self.status == Status::Open {
            // decrease lifetime value by tick
            self.lifetime -= 1;
            if self.lifetime <= 0 && self.status != Status::Progress {
                self.status = Status::Cancelled;
            }
        }
    }
}
