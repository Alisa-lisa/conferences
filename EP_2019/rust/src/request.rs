/**
 * Request object: keeps an eye on interaction between users and cars
 * */
use chrono::prelude::{DateTime, Utc};
use uuid::Uuid;
use std::fmt; 

#[derive(PartialEq, Debug, Clone)]
pub enum Status {
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
    pub id: String,
    pub usr_id: u32,
    pub car_id: Option<u32>,
    pub status: Status,
    pub pickup: (f32, f32),
    pub dropoff: (f32, f32),
    pub created: chrono::DateTime<Utc>,
    pub picked: bool,
    pub created_tick: u32,
    pub lifetime: u32,
}

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
    pub fn next_phase(&mut self) {
        if self.status == Status::Open {
            self.status = Status::Progress;
        }
        else if self.status == Status::Progress {
            self.status = Status::Finished;
        }
    }

    pub fn cancel(&mut self) {
        self.status = Status::Cancelled;
    }

    pub fn update(&mut self) {
        // cehcks if the request changes states
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
