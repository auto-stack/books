// Auto — functions, closures, and higher-order functions
function add(a: number, b: number): number {
    return a + b;
}

function apply(f: (param: number) => number, x: number): number {
    return f(x);
}

function greet(name: string, greeting: string | null): void {
    if (greeting !== null) {
        console.log(greeting + ", " + name + "!");
    } else {
        console.log("Hello, " + name + "!");
    }
}

function make_counter(): () => number {
    let count: number = 0;
    return function (): number {
        count = count + 1;
        return count;
    };
}

function main(): void {
    // Basic function
    console.log("3 + 4 = " + add(3, 4));

    // Higher-order function
    const double: (x: number) => number = (x: number) => x * 2;
    console.log("double(5) = " + apply(double, 5));

    // Closure counter
    const counter = make_counter();
    console.log("counter: " + counter());
    console.log("counter: " + counter());
    console.log("counter: " + counter());

    // Optional parameters
    greet("Alice");
    greet("Bob", "Good morning");
}

main();
