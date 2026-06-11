// Rust
use url::Url;

fn main() {
    let url = Url::parse("https://example.com/rust?name=hello&age=20").unwrap();
    let query = url.query().unwrap_or("");
    println!("Query string: {}", query);

    let mut pair_count = 0;
    for pair in url.query_pairs() {
        pair_count += 1;
    }
    println!("Parameter count: {}", pair_count);
}
