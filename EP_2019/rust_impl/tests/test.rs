use crate::core;


#[cfg(test)]
mod tests {
    #[test]
    fn test_clock_tick() {
        let mut clock = core::Clock{step: 1,
        unit: "s".to_string(),
        start: "2019-07-06T00:00:00".to_string(),
        end: "2019-07-06T00:02:00".to_string(),
        now: 0,
        number_ticks: 120};
        assert_eq!(clock.now, 0);

        clock.tick();
        assert_eq!(clock.now, 1);
    }
}
