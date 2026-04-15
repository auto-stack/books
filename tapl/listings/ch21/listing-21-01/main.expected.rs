// Rust
#[allow(unused_imports)]
use auto_lang::a2r_std::*;

fn main() {
    let mut raw = String::from("  Hello, World!  ");
    let mut trimmed = raw.trim().to_string();
    println!("{}", trimmed);

    let mut greeting = format!("Hello, {}!", "Auto");
    println!("{}", greeting);

    let mut csv = String::from("one,two,three,four");
    let mut parts: Vec<&str> = csv.split(",").collect();
    for part in &parts {
        println!("{}", part);
    }

    let mut joined = vec!["Hello", "World"].join(" ");
    println!("{}", joined);

    let mut msg = String::from("Hello, World!");
    println!("{}", msg.contains("World"));
    println!("{}", msg.starts_with("Hello"));
    println!("{}", msg.ends_with("!"));
    println!("{}", msg.to_uppercase());
    println!("{}", msg.replace("World", "Auto"));
}
