// Rust
fn main() {
    let x = 2.0;
    let y = 3.0;

    let power = x.powf(y);
    let sqrt_val = x.sqrt();
    println!("{} ^ {} = {}", x, y, power);
    println!("sqrt({}) = {}", x, sqrt_val);

    let neg = -5.0;
    let abs_result = neg.abs();
    println!("|{}| = {}", neg, abs_result);

    let pi = std::f64::consts::PI;
    let sin_val = pi.sin();
    let cos_val = pi.cos();
    println!("sin(pi) = {}", sin_val);
    println!("cos(pi) = {}", cos_val);
}
