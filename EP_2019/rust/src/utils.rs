// check x and y coordinate. Uses int comparison
pub fn is_equal(pos1: (f32, f32), pos2: (f32, f32)) -> bool {
    // Return boolean if coordinates are "close enough"
    //
    // # Arguments
    //
    // * `pos1` - x, y tuple of floats 32
    // * `pos2` - x, y tuple of floats 32
    pos1.0.ceil() == pos2.0.ceil() && pos1.1.ceil() == pos2.1.ceil()
}
