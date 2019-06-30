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
    pub status: Status,
    pub pickup: (f32, f32),
    pub dropoff: (f32, f32),
    pub created: chrono::DateTime<Utc>,
    pub created_tick: u32,
    pub lifetime: u32,
}

impl Request {
    pub fn new(pickup: (f32, f32), dropoff: (f32, f32)) -> Request {
        Request{id: Uuid::new_v4().to_string(), status: Status::Open,
        pickup: pickup, dropoff: dropoff, created: Utc::now(), created_tick: 0, 
        lifetime: 900}
    }

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

    pub fn update(&mut self) -> Request {
        println!("Status {}", self.status);
        if self.status == Status::Open {
            // decrease lifetime value by tick
            self.lifetime -= 1;
            if self.lifetime <= 0 && self.status != Status::Progress {
                self.status = Status::Cancelled;
            }
        }
        println!("Lifetime left: {}", self.lifetime);
        println!("Current status: {}", self.status);
        let mut res = self.clone();
        res
    }
}
