// Rust
use sha2::{Sha256, Digest};

fn main() {
    let mut hasher = Sha256::new();
    hasher.update(b"hello world");
    let result = hasher.finalize();

    let hex: String = result.iter().map(|b| format!("{:02x}", b)).collect();
    println!("SHA-256: {}", hex);
}
