// Rust
use base64::{Engine as _, engine::general_purpose::STANDARD};

fn main() {
    let original = "hello world";
    let encoded = STANDARD.encode(original.as_bytes());
    println!("{}", encoded);

    let decoded = STANDARD.decode(&encoded).unwrap();
    println!("{}", String::from_utf8_lossy(&decoded));

    let binary: Vec<u8> = vec![0x00, 0x01, 0x02, 0x03];
    let b64 = STANDARD.encode(&binary);
    println!("{}", b64);
}
