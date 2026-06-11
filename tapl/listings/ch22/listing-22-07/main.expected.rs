// Rust
use url::Url;

fn main() {
    let u = Url::parse("https://example.com/path?query=1").unwrap();
    println!("Scheme: {}", u.scheme());
    println!("Host:   {}", u.host_str().unwrap_or(""));
    println!("Path:   {}", u.path());
}
