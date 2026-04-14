function add(a: number, b: number): number {
    return a + b;
}

function greet(name: string): void {
    console.log(`Hello, ${name}!`);
}

function main(): void {
    const result = add(5, 3);
    console.log(result);
    greet("Alice");
}

main();
