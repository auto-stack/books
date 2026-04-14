function greet(name: string, greeting: string | null): void {
    if (greeting) {
        console.log(`${greeting}, ${name}!`);
    } else {
        console.log(`Hello, ${name}!`);
    }
}

function main(): void {
    greet("Alice");
    greet("Bob", "Hi");
}

main();
