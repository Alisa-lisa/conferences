use uuid::Uuid;

#[derive(Debug, Clone)]
pub struct Request {
    // Main object controlling the logic flow. Bind a car and a user together
    //
    // id: unique identifyer of the Request uuid.to_string()
    // passenger : u32 id uo user spawned this requrest
    // car_id: u32 id of the assigned car, is None untill assigned
    // in_progress: bool if the request was assigned to a car
    // picked: bool is the passenger being transported
    // lifetime: u64 how long a passenger can wait untill the request is assigned to a car
    // execution_time: how long will it last to fulfill an assigned request (movement proxy)
    // pickup: tuple of u32 coordinates
    // destination: tuple of u32 coordinates
    pub id: Uuid,
    pub passenger: u32,
    pub car_id: Option<u32>,
    pub in_progress: bool,
    pub picked: bool, 
    pub finished: bool,
    pub lifetime: u64,
    pub execution_time: u64,
    pub pickup: (u32, u32),
    pub destination: (u32, u32),
}
