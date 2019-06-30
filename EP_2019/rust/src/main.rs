use ggez::*;
use ggez::graphics::{DrawMode, Point2};
use rand::prelude::*;
use rand::seq::SliceRandom;
use std::collections::HashMap;

mod user;
mod request;
mod driver;
mod clock;


// internal functions
fn assign_random(mut request: request::Request, mut drivers: Vec<driver::Driver>) {
    // random free car gets the request
}


fn assign_closest() {
    //
}

struct MainState {
    rng: SmallRng,
    clock: clock::Clock,
    users: HashMap<u32, user::User>,
    cars: HashMap<u32, driver::Driver>,
    requests: HashMap<String, request::Request>,
}

impl MainState {
    fn new(_ctx: &mut Context) -> GameResult<MainState> {
        let mut rng = SmallRng::from_rng(thread_rng()).unwrap();
        let mut clock = clock::Clock{lifetime: 1200, now: 0};
        let mut users = user::spawn(1, &mut rng);
        let mut cars = driver::spawn(1, &mut rng);
        let mut requests = HashMap::new();
        let mut s = MainState{rng, clock, users, cars, requests};
        Ok(s)
    }
}

impl event::EventHandler for MainState {
    fn update(&mut self, ctx: &mut Context) -> GameResult<()> {
        for (i, ref mut user) in self.users.iter_mut() {
            let req = user.update(&mut self.rng, self.clock.now);
            if req.is_some() {
                let mut request = req.unwrap().clone();
                self.requests.insert(request.id.clone(), request);
            }
            else {
                if user.current_request.is_some() {
                    let u = user.current_request.clone().unwrap();
                    let status = self.requests.get(&u).clone();
                    let s = status.unwrap().clone().status;
                    if s == request::Status::Cancelled || s == request::Status::Finished {
                        user.determination = false;
                        user.current_request = None;
                    }
                }
            }
        }
        // helper vec of free drivers
        let mut free_cars = self.drivers
        for (i, ref mut req) in self.requests.iter_mut() {
            req.update()
        }

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
