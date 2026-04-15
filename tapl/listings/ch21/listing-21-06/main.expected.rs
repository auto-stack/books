// Rust
#[allow(unused_imports)]
use auto_lang::a2r_std::*;

use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct User {
    name: String,
    age: i32,
    email: String,
}

fn main() {
    let mut alice = User { name: String::from("Alice"), age: 30, email: String::from("alice@example.com") };
    let json = serde_json::to_string(&alice).unwrap();
    println!("{}", json);

    let parsed: User = serde_json::from_str(&json).unwrap();
    println!("{}", parsed.name);
    println!("{}", parsed.age);

    let pretty = serde_json::to_string_pretty(&alice).unwrap();
    println!("{}", pretty);

    let mut bob = User { name: String::from("Bob"), age: 25, email: String::from("bob@example.com") };
    let users = vec![alice, bob];
    let users_json = serde_json::to_string(&users).unwrap();
    println!("{}", users_json);
}
