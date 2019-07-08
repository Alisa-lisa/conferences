#[derive(Clone, Debug)]
pub struct Car {
    // Car object
    //
    // id: unique identifyer
    // pos: u32 tuple coordinate
    // free: bool if the car has an assigned request
    pub id: u32,
    pub pos: (u32, u32),
    pub free: bool,
}

