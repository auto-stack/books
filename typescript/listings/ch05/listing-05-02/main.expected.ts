class User implements Greetable {
    name: number;

    constructor(name: number) {
        this.name = name;
    }

    greet(): void {
        console.log("Hello from user", this.name);
    }
}

function main(): void {
    const user = User(42);
    user.greet();
}

main();
