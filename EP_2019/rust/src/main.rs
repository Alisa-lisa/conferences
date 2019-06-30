use ggez::*;
use ggez::graphics::{DrawMode, Point2};
use rand::prelude::*;

use std::collections::HashMap;

mod user;
mod request;
mod driver;
mod clock;

fn is_equal(first: f32, second: f32) -> bool {
	let res = first.ceil() == second.ceil();
	res
}

// internal functions
struct MainState {
    rng: SmallRng,
    clock: clock::Clock,
    users: HashMap<u32, user::User>,
    cars: HashMap<u32, driver::Driver>,
    requests: Vec<request::Request>,
}

impl MainState {
    fn new(_ctx: &mut Context) -> GameResult<MainState> {
        let mut rng = SmallRng::from_rng(thread_rng()).unwrap();
        let clock = clock::Clock{lifetime: 1200, now: 0};
        let users = user::spawn(1, &mut rng);
        let cars = driver::spawn(1, &mut rng);
        let requests = Vec::new();
        let s = MainState{rng, clock, users, cars, requests};
        Ok(s)
    }
}

impl event::EventHandler for MainState {
    fn update(&mut self, _: &mut Context) -> GameResult<()> {
        // spawn a request if needed
        for (i, ref mut user) in self.users.iter_mut() {
            let req = user.update(&mut self.rng, self.clock.now);
            if req.is_some() {
                self.requests.push(req.unwrap());
            }
        }

        // helper vec of free drivers
        let mut free_drivers = driver::get_free_drivers(&mut self.cars);

        for r in self.requests.iter_mut() {
            println!("request's car {}", r);
            // no car assigned yet
            if !r.car_id.is_some() {
                // TODO: different assign function
                if free_drivers.len() > 0 {
                    let fd_id = free_drivers.pop();  
                    r.car_id = fd_id.clone();
                    self.cars.entry(fd_id.unwrap()).and_modify(|d| d.accept_request());
                    println!("now car is {}", r);
                }
            }

            // some car is assigned to this request
            // checking where the car is by location
            if !r.picked {
                println!("{}", "WTF");
                let car = r.car_id.clone().unwrap();
                if is_equal(self.cars.get(&(car.clone())).unwrap().pos.0, r.pickup.0) &&
                    is_equal(self.cars.get(&(car.clone())).unwrap().pos.1, r.pickup.1) {
                    dbg!("LOL");
                    r.picked = true;
                    self.users.entry(r.usr_id).and_modify(|u| u.picked = true); // picked attr is for graphics
                }
                else {
                    println!("{}", "broooom");
                    println!("{}", r);
                    self.cars.entry(car).and_modify(|d| d.step(r.pickup));
                }
            }
            // on the dropoff way
            else {
                println!("{}", "Should not be here");
                let car = r.car_id.clone().unwrap();
                if !(is_equal(self.cars.get(&(car)).unwrap().pos.0, r.dropoff.0) &&
                    is_equal(self.cars.get(&(car.clone())).unwrap().pos.1, r.dropoff.1)) {
                    self.cars.entry(car).and_modify(|d| d.step(r.dropoff));
                }
                // finish request when arrived
                else if is_equal(self.cars.get(&car).unwrap().pos.0, r.dropoff.0) &&
                    is_equal(self.cars.get(&(car.clone())).unwrap().pos.1, r.dropoff.1) {
                    r.status = request::Status::Finished;
                    self.cars.entry(car.clone()).and_modify(|d| d.occupied = false);
                    // teleport user =)
                    self.users.entry(r.usr_id).and_modify(|u| u.pos = r.dropoff);
                    self.users.entry(r.usr_id).and_modify(|u| u.determination = false);
                    self.users.entry(r.usr_id).and_modify(|u| u.picked = false);
                    self.users.entry(r.usr_id).and_modify(|u| u.current_request = None);
                }
            }
            r.update();
        }
        // let drivers pickup passengers. TODO: how to work properly with iterator?
        //tmp_drivers.drain();
        //self.requests.retain(|c| c.status == request::Status::Finished);

        self.clock.tick();

        Ok(())
    }

    fn draw(&mut self, ctx: &mut Context) -> GameResult<()> {
        graphics::clear(ctx);
        for (id, ref user) in self.users.iter() {
            if user.determination && !user.picked {
                graphics::set_color(ctx, graphics::Color::new(252.0, 20.0, 0.0, 1.0))?;
                graphics::circle(
                    ctx,
                    DrawMode::Fill,
                    Point2::new(user.pos.0, user.pos.1),
                    5.0,
                    2.0
                )?;
            }
            else if !user.determination {
                graphics::set_color(ctx, graphics::Color::new(0.0, 128.0, 0.0, 1.0))?;
                graphics::circle(
                    ctx,
                    DrawMode::Fill,
                    Point2::new(user.pos.0, user.pos.1),
                    5.0,
                    2.0
                )?;
            }
            else if user.determination && user.picked {
                // dissapear
            }
        }
        graphics::set_color(ctx, graphics::Color::new(255.0, 0.0, 0.0, 1.0))?;
        for (id, ref car) in self.cars.iter() {
            graphics::circle(
                ctx,
                DrawMode::Fill,
                Point2::new(car.pos.0, car.pos.1),
                5.0,
                2.0
            )?;
        }

        graphics::present(ctx);
        Ok(())
    }

}

pub fn main() {
    let c = conf::Conf::new();
    let ctx = &mut Context::load_from_conf("super_simple", "ggez", c).unwrap();
    let state = &mut MainState::new(ctx).unwrap();
    event::run(ctx, state).unwrap();
}
