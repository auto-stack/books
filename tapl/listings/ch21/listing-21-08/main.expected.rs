// Rust
use std::collections::HashMap;

fn main() {
    let config: HashMap<String, HashMap<String, String>> = {
        let mut c = HashMap::new();
        let mut server = HashMap::new();
        server.insert("host".to_string(), "localhost".to_string());
        server.insert("port".to_string(), "8080".to_string());
        c.insert("server".to_string(), server);
        let mut database = HashMap::new();
        database.insert("url".to_string(), "postgres://localhost/mydb".to_string());
        c.insert("database".to_string(), database);
        c
    };
    println!("{}", config["server"]["host"]);
    println!("{}", config["server"]["port"]);
    println!("{}", config["database"]["url"]);
}
