// Rust
use std::fs;

fn main() {
    fs::write("lines.txt", "Rust\nFun\nAuto").unwrap();

    let data = fs::read_to_string("lines.txt").unwrap();
    println!("Content: {}", data);
    println!("Length: {}", data.len());

    for line in data.lines() {
        println!("  Line: {}", line);
    }

    fs::remove_file("lines.txt").unwrap();
}
