// Rust
#[derive(Clone, Debug)]
struct Person {
    name: String,
    age: i32,
}

fn main() {
    let mut people = vec![
        Person { name: "Zoe".to_string(), age: 25 },
        Person { name: "Al".to_string(), age: 60 },
        Person { name: "John".to_string(), age: 1 },
    ];

    println!("Sorted by age:");
    people.sort_by_key(|p| p.age);
    for p in &people {
        println!("  {} ({})", p.name, p.age);
    }
}
