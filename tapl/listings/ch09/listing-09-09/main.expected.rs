// Rust
use std::env;

fn main() {
    env::set_var("AUTO_GREETING", "Hello from Auto");

    let val = env::var("AUTO_GREETING").unwrap_or("default".to_string());
    println!("Greeting: {}", val);

    let missing = env::var("NONEXISTENT_VAR").unwrap_or("not set".to_string());
    println!("Missing: {}", missing);
}
