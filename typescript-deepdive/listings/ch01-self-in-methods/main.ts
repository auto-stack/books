class User {
    name: string;

    constructor(name: string) {
        this.name = name;
    }

    greet(): void {
        console.log("Hello from " + this.name);
    }
}

function main(): void {
    const user = User("Alice");
    user.greet();
}

main();
