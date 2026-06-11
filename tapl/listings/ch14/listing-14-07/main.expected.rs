// Rust
use std::fs;

fn main() {
    let content = "line1\nline2\nline3";
    let path = "test_temp.txt";

    fs::write(path, content).unwrap();

    let text = fs::read_to_string(path).unwrap();
    let mut line_count = 0;
    for line in text.lines() {
        line_count += 1;
        println!("  [{}] {}", line_count, line);
    }
    println!("Total lines: {}", line_count);

    fs::remove_file(path).unwrap();
}
