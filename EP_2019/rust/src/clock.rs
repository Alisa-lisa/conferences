/**
 * Internal simulation clock
 * */



pub struct Clock {
    pub lifetime: u32,
    pub now: u32,
}

impl Clock {
    pub fn tick(&mut self) {
        self.now += 1;
    }

    pub fn is_last_tick(&mut self) -> bool {
        if self.lifetime == self.now {
            return true
        }
        return false
    }
}
