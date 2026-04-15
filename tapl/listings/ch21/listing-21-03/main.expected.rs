// Rust
#[allow(unused_imports)]
use auto_lang::a2r_std::*;

use std::path::PathBuf;
use std::fs;

fn main() {
    let mut path = PathBuf::from("data").join("output.txt");
    println!("{}", path.display());

    fs::write(&path, "Hello from Auto!").unwrap();
    let content = fs::read_to_string(&path).unwrap();
    println!("{}", content);

    println!("{}", path.exists());
    println!("{}", PathBuf::from("nonexistent.txt").exists());

    fs::create_dir_all("data/backup").unwrap();
    let entries: Vec<_> = fs::read_dir("data").unwrap()
        .map(|e| e.unwrap().file_name().to_string_lossy().to_string())
        .collect();
    for entry in &entries {
        println!("{}", entry);
    }
}
