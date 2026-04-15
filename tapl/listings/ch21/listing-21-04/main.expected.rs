// Rust
#[allow(unused_imports)]
use auto_lang::a2r_std::*;

fn main() {
    let mut nums = vec![3, 1, 4, 1, 5, 9, 2, 6];
    let mut sorted = { let mut v = nums.clone(); v.sort(); v };
    for n in &sorted {
        println!("{}", n);
    }

    let mut rev: Vec<i32> = vec![1, 2, 3, 4, 5].into_iter().rev().collect();
    println!("{:?}", rev);

    let mut uniq: Vec<i32> = {
        let mut seen = std::collections::HashSet::new();
        let src = vec![3, 1, 4, 1, 5, 9, 2, 6, 5, 3];
        src.into_iter().filter(|x| seen.insert(*x)).collect()
    };
    println!("{:?}", uniq);

    let mut flat: Vec<i32> = vec![vec![1, 2], vec![3, 4], vec![5, 6]]
        .into_iter().flatten().collect();
    println!("{:?}", flat);

    let names = vec!["Alice", "Bob", "Carol"];
    let scores = vec![95, 87, 92];
    let mut pairs: Vec<_> = names.into_iter().zip(scores.into_iter()).collect();
    for pair in &pairs {
        println!("{:?}", pair);
    }

    let mut chunked: Vec<Vec<i32>> = vec![1, 2, 3, 4, 5, 6, 7]
        .chunks(3).map(|c| c.to_vec()).collect();
    for c in &chunked {
        println!("{:?}", c);
    }
}
