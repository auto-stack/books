// Rust
use std::time::Instant;
use std::thread;

fn main() {
    let start = Instant::now();

    let mut sum = 0;
    for i in 0..1000 {
        sum += i;
    }

    let elapsed = start.elapsed().as_millis();
    println!("Sum: {}", sum);
    println!("Elapsed: {} ms", elapsed);

    thread::sleep(std::time::Duration::from_millis(100));
    println!("Slept 100ms");
}
