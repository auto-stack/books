// Rust
#[allow(unused_imports)]
use auto_lang::a2r_std::*;

use std::time::{SystemTime, Duration};

fn main() {
    let now = SystemTime::now();
    println!("{:?}", now);

    let formatted = chrono::Local::now().format("%Y-%m-%d %H:%M:%S");
    println!("{}", formatted);

    let parsed = chrono::NaiveDateTime::parse_from_str(
        "2025-01-15 10:30:00", "%Y-%m-%d %H:%M:%S"
    ).unwrap();
    println!("{}", parsed);

    let duration = Duration::from_secs(2 * 3600 + 30 * 60);
    println!("{:?}", duration);

    let later = now + duration;
    println!("{:?}", later);

    let diff = later.duration_since(now).unwrap();
    println!("{}", diff.as_secs() / 60);
}
