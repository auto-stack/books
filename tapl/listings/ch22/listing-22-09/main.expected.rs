// Rust
fn main() {
    let mut output_lines: Vec<String> = Vec::new();
    output_lines.push("Building project...".to_string());
    output_lines.push("Compiling src/main.at".to_string());
    output_lines.push("Done: 2 files compiled".to_string());

    println!("Captured {} lines:", output_lines.len());
    for line in &output_lines {
        println!("  {}", line);
    }
}
