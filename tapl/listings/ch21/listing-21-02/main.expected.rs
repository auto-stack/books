// Rust
#[allow(unused_imports)]
use auto_lang::a2r_std::*;

fn clamp(value: i32, min_val: i32, max_val: i32) -> i32 {
    if value < min_val { min_val } else if value > max_val { max_val } else { value }
}

fn main() {
    println!("{}", std::cmp::min(3, 7));
    println!("{}", std::cmp::max(3, 7));
    println!("{}", (-42_i32).abs());
    println!("{}", (3.7_f64).round());
    println!("{}", (3.9_f64).floor());
    println!("{}", (3.1_f64).ceil());
    println!("{}", clamp(15, 0, 10));
    println!("{}", 2.0_f64.powf(10.0));
    println!("{}", 144.0_f64.sqrt());
}
