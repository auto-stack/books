// Auto — has composition vs index signatures
class Named {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
  greet(): void {
    console.log("Hi, I'm " + this.name);
  }
}

class Aged {
  age: number;
  constructor(age: number) {
    this.age = age;
  }
}

class Logged {
  log(msg: string): void {
    console.log("[LOG] " + msg);
  }
}

class User {
  name: string;
  age: number;
  email: string;
  constructor(name: string, age: number, email: string) {
    this.name = name;
    this.age = age;
    this.email = email;
  }
  greet(): void {
    console.log("Hi, I'm " + this.name);
  }
  log(msg: string): void {
    console.log("[LOG] " + msg);
  }
}

class Admin {
  name: string;
  level: number;
  constructor(name: string, level: number) {
    this.name = name;
    this.level = level;
  }
  greet(): void {
    console.log("Hi, I'm " + this.name);
  }
  log(msg: string): void {
    console.log("[LOG] " + msg);
  }
}

function introduce(u: User): void {
  u.greet();
  console.log("Age: " + u.age);
}

function main(): void {
  const user = new User("Alice", 30, "alice@example.com");
  user.greet();
  user.log("User created");
  console.log("Email: " + user.email);

  const admin = new Admin("Bob", 1);
  admin.greet();
  admin.log("Admin logged in");
  console.log("Admin level: " + admin.level);

  // Structural typing — Admin satisfies the parts User needs
  // But introduce() requires `age`, which Admin doesn't have
}

main();
