use ggez::*;
use ggez::graphics::{DrawMode, Point2};
use rand::prelude::*;
use rand::seq::SliceRandom;
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
        let mut clock = clock::Clock{lifetime: 1200, now: 0};
        let mut users = user::spawn(1, &mut rng);
        let mut cars = driver::spawn(1, &mut rng);
        let mut requests = Vec::new();
        let mut s = MainState{rng, clock, users, cars, requests};
        Ok(s)
    }
}

impl event::EventHandler for MainState {
    fn update(&mut self, ctx: &mut Context) -> GameResult<()> {
        for (i, ref mut user) in self.users.iter_mut() {
            let req = user.update(&mut self.rng, self.clock.now);
            if req.is_some() {
                self.requests.push(req.unwrap());
            }
            else {
                if user.current_request.is_some() {
                }
            }
        }
        // helper vec of free drivers
        let mut free_drivers = driver::get_free_drivers(&mut self.cars);
        println!("{}", free_drivers.len());
        for con in self.requests.iter_mut() {
            if !con.car_id.is_some() {
                // TODO: fix this one. contratcs wait if no driver is there
                let mut fd_id = free_drivers.pop();
                if fd_id.is_some() {
                    con.car_id = fd_id.clone();
                    self.cars.entry(fd_id.unwrap()).and_modify(|d| d.accept_request());
                }
            }
            else {

                if is_equal(self.cars.get(&(con.car_id.clone().unwrap())).unwrap().pos.0, con.pickup.0) &&
                    is_equal(self.cars.get(&(con.car_id.clone().unwrap())).unwrap().pos.1, con.pickup.1) {
                        con.picked = true;
                        self.users.entry(con.usr_id).and_modify(|u| u.picked = true);
                    }
                // driving logic
                // 1. pickup the passenger
                if !con.picked {
                    self.cars.entry(con.car_id.unwrap()).and_modify(|d| d.step(con.pickup));

                }
                else {
                    // 2. get user to destination
                    if !(is_equal(self.cars.get(&(con.car_id.clone().unwrap())).unwrap().pos.0, con.dropoff.0) &&
                         is_equal(self.cars.get(&(con.car_id.clone().unwrap())).unwrap().pos.1, con.dropoff.1)) {
                        self.cars.entry(con.car_id.unwrap()).and_modify(|d| d.step(con.dropoff));
                    }
                    // finish request when arrived
                    else if is_equal(self.cars.get(&(con.car_id.clone().unwrap())).unwrap().pos.0, con.dropoff.0) &&
                        is_equal(self.cars.get(&(con.car_id.clone().unwrap())).unwrap().pos.1, con.dropoff.1) {
                            con.status = request::Status::Finished;
                            self.cars.entry(con.car_id.unwrap()).and_modify(|d| d.occupied = false);
                            // teleport user =)
                            self.users.entry(con.usr_id).and_modify(|u| u.pos = con.dropoff);
                            self.users.entry(con.usr_id).and_modify(|u| u.determination = false);
                            self.users.entry(con.usr_id).and_modify(|u| u.picked = false);
                        }
                }
            }
        }
        // let drivers pickup passengers. TODO: how to work properly with iterator?
        //tmp_drivers.drain();
        self.requests.retain(|c| c.status == request::Status::Finished);

        self.clock.tick();

        Ok(())
    }

    fn draw(&mut self, ctx: &mut Context) -> GameResult<()> {
        graphics::clear(ctx);
        for (id, ref user) in self.users.iter() {
            if user.determination {
                graphics::set_color(ctx, graphics::Color::new(252.0, 20.0, 0.0, 1.0))?;
                graphics::circle(
                    ctx,
                    DrawMode::Fill,
                    Point2::new(user.pos.0, user.pos.1),
                    5.0,
                    2.0
                )?;
            }
            else {
                graphics::set_color(ctx, graphics::Color::new(0.0, 128.0, 0.0, 1.0))?;
                graphics::circle(
                    ctx,
                    DrawMode::Fill,
                    Point2::new(user.pos.0, user.pos.1),
                    5.0,
                    2.0
                )?;

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

    /* fn stop_event(&mut self, ctx: Context) {
       if self.clock.is_last_tick() {
       ggez::quit(ctx);
       }
       }
       */
}

pub fn main() {
    let c = conf::Conf::new();
    let ctx = &mut Context::load_from_conf("super_simple", "ggez", c).unwrap();
    let state = &mut MainState::new(ctx).unwrap();
    event::run(ctx, state).unwrap();
}
