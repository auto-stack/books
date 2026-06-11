// Rust
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let msg = "hello";
    let result: Result<String, &str> = Ok(msg.to_string());
    let val = result?;
    println!("Got: {}", val);

    let fail: Result<String, &str> = Err("something went wrong");
    let recover = fail?;
    println!("{}", recover);
    Ok(())
}
