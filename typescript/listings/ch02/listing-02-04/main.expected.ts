class User {
    name: string;
    age: number;

    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }
}

function main(): void {
    const user = User("Alice", 30);
    console.log(`${user.name} is ${user.age} years old`);
}

main();
