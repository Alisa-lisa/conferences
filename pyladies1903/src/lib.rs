// Source adopted from
// https://github.com/tildeio/helix-website/blob/master/crates/word_count/src/lib.rs
#![feature(specialization)]

#[macro_use]
extern crate pyo3;
extern crate rayon;

use pyo3::prelude::*;
use rayon::prelude::*;
use std::fs;
use std::path::PathBuf;

/// Represents a file that can be searched
#[pyclass]
struct WordCounter {
    path: PathBuf,
}

#[pymethods]
impl WordCounter {
    #[new]
    fn __new__(obj: &PyRawObject, path: String) -> PyResult<()> {
        obj.init(|_| WordCounter {
            path: PathBuf::from(path),
        })
    }

    fn search(&self, py: Python, search: String) -> PyResult<usize> {
        let contents = fs::read_to_string(&self.path)?;

        let count = py.allow_threads(move || {
            contents
                .par_lines()
                .map(|line| count_line(line, &search))
                .sum()
        });
        Ok(count)
    }

    /// Searches for a word in a classic sequential fashion
    fn search_sequential(&self, needle: String) -> PyResult<usize> {
        let contents = fs::read_to_string(&self.path)?;

        let result = contents.lines().map(|line| count_line(line, &needle)).sum();

        Ok(result)
    }
}

fn matches(word: &str, needle: &str) -> bool {
    word.trim_matches(|c: char| !c.is_alphabetic()).starts_with(needle)
}

/// Count the occurences of needle in line, case insensitive
#[pyfunction]
fn count_line(line: &str, needle: &str) -> usize {
    let mut total = 0;
    let needle_lower = needle.to_lowercase();
    for word in line.split(' ') {
        if matches(&word.to_lowercase(), &needle_lower) {
            total += 1;
        }
    }
    total
}

#[pymodinit]
fn pyladies_wordcount(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_function!(count_line))?;
    m.add_class::<WordCounter>()?;

    Ok(())
}
