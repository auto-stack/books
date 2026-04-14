function greet(name: number, greeting: number | null): void {
    if (greeting) {
        console.log(greeting, name);
    } else {
        console.log(name);
    }
}

function main(): void {
    greet(42);
    greet(42, 1);
}

main();
