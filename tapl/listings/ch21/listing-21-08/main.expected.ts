// TypeScript
const config = {
    server: { host: "localhost", port: 8080 },
    database: { url: "postgres://localhost/mydb" }
};

console.log(config["server"]["host"]);
console.log(config["server"]["port"]);
console.log(config["database"]["url"]);
