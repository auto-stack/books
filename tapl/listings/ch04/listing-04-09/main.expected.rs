// Rust
fn main() {
    let mut nums = vec![15, 3, 8, 1, 12, 7];

    println!("Before sort:");
    for n in &nums {
        print!("{} ", n);
    }
    println!();

    nums.sort();

    println!("After sort:");
    for n in &nums {
        print!("{} ", n);
    }
    println!();
}
