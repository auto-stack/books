// TypeScript — intersection types and index signatures
interface Named {
    name: string;
    greet(): void;
}

interface Aged {
    age: number;
}

interface Logged {
    log(msg: string): void;
}

type User = Named & Aged & Logged & { email: string };

type Admin = Named & Logged & { level: number };

function introduce(u: User): void {
    u.greet();
    console.log("Age: " + u.age);
}

const user: User = {
    name: "Alice",
    age: 30,
    email: "alice@example.com",
    greet() { console.log("Hi, I'm " + this.name); },
    log(msg: string) { console.log("[LOG] " + msg); }
};
user.greet();
user.log("User created");
console.log("Email: " + user.email);

const admin: Admin = {
    name: "Bob",
    level: 1,
    greet() { console.log("Hi, I'm " + this.name); },
    log(msg: string) { console.log("[LOG] " + msg); }
};
admin.greet();
admin.log("Admin logged in");
console.log("Admin level: " + admin.level);
