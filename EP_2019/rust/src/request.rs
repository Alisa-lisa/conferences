use chrono::prelude::{DateTime, Utc};
use uuid::Uuid;


#[derive(PartialEq)]
enum Status {
    Open,
    Progress,
    Finished,
    Cancelled,
}

pub struct Request {
    pub id: String,
    pub status: Status,
    pub pickup: (f32, f32),
    pub dropoff: (f32, f32),
    pub created: chrono::DateTime<Utc>,
}

impl Request {
    pub fn new(pickup: (f32, f32), dropoff: (f32, f32)) -> Request {
        Request{id: Uuid::new_v4().to_string(), status: Status::Open,
        pickup: pickup, dropoff: dropoff, created: Utc::now()}
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
}
