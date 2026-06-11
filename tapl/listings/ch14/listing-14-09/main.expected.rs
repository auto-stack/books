// Rust
fn main() {
    let data = "name,age\nAlice,30\nBob,25\nCharlie,35";
    let lines: Vec<&str> = data.split("\n").collect();

    println!("People over 28:");
    for i in 1..lines.len() {
        let line = lines[i];
        let fields: Vec<&str> = line.split(",").collect();
        let name = fields[0];
        let age: i32 = fields[1].parse().unwrap();
        if age > 28 {
            println!("  {} ({})", name, age);
        }
    }
}
