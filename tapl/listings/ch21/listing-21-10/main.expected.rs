// Rust
fn main() {
    let data = b"hello world";
    let hex_str: String = data.iter().map(|b| format!("{:02x}", b)).collect();
    println!("{}", hex_str);

    let original = String::from_utf8(
        (0..hex_str.len())
            .step_by(2)
            .map(|i| u8::from_str_radix(&hex_str[i..i+2], 16).unwrap())
            .collect()
    ).unwrap();
    println!("{}", original);

    let num = 255;
    println!("0x{:02x}", num);
}
