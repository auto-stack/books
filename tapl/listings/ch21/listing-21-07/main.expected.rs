// Rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct User {
    name: String,
    age: i32,
}

fn main() {
    let alice = User { name: String::from("Alice"), age: 30 };
    let json = serde_json::to_string(&alice).unwrap();
    println!("{}", json);

    let parsed: serde_json::Value = serde_json::from_str(&json).unwrap();
    println!("{}", parsed["name"]);
    println!("{}", parsed["age"]);

    let bob = User { name: String::from("Bob"), age: 25 };
    let users = vec![alice, bob];
    let array_json = serde_json::to_string(&users).unwrap();
    println!("{}", array_json);
}
