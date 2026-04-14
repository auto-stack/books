// Auto — primitive types and annotations
function main(): void {
    // Explicit type annotations
    const count: number = 42;
    const pi: number = 3.14159;
    const name: string = "Auto";
    const is_ready: boolean = true;

    // Type inference
    const sum: number = count + 8;       // inferred as int
    const items: number[] = [1, 2, 3];     // inferred as []int

    // Nullable types
    const middle_name: string | null = null;

    // Arrays
    const numbers: number[] = [10, 20, 30];
    const doubled: number[] = numbers.map((n: number) => n * 2);

    console.log("Name: " + name);
    console.log("Sum: " + sum);
    console.log("Doubled: " + doubled);

    // Union types
    const id: number | string = 42;
    id = "user-001";

    // Tuple-like types
    const pair: [number, string] = (1, "hello");
    console.log("First: " + pair[0] + ", Second: " + pair[1]);
}

main();
