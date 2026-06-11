// Rust
fn main() {
    let a = vec![vec![1, 2], vec![3, 4]];
    let b = vec![vec![5, 6], vec![7, 8]];
    let mut c = vec![vec![0, 0], vec![0, 0]];

    for i in 0..2 {
        for j in 0..2 {
            c[i][j] = a[i][j] + b[i][j];
        }
    }

    println!("Result matrix:");
    for i in 0..2 {
        println!("  {} {}", c[i][0], c[i][1]);
    }
}
