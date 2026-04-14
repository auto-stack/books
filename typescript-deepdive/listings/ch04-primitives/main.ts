// TypeScript — primitive types and annotations
function main(): void {
    // Explicit type annotations
    const count: number = 42;
    const pi: number = 3.14159;
    const name: string = "Auto";
    const is_ready: boolean = true;

    // Type inference
    const sum = count + 8;       // inferred as number
    const items = [1, 2, 3];     // inferred as number[]

    // Nullable types
    let middle_name: string | null = null;

    // Arrays
    const numbers = [10, 20, 30];
    const doubled = numbers.map((n: number) => n * 2);

    console.log("Name: " + name);
    console.log("Sum: " + sum);
    console.log("Doubled: " + doubled);

    // Union types
    let id: number | string = 42;
    id = "user-001";

    // Tuple types
    const pair: [number, string] = [1, "hello"];
    console.log("First: " + pair[0] + ", Second: " + pair[1]);
}
