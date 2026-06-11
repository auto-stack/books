// Rust
fn main() {
    let csv_str = "name,age\nAlice,30\nBob,25";

    let lines: Vec<&str> = csv_str.split("\n").collect();

    for i in 1..lines.len() {
        let line = lines[i];
        let fields: Vec<&str> = line.split(",").collect();
        let name = fields[0];
        let age = fields[1];
        println!("Name: {}, Age: {}", name, age);
    }
}
