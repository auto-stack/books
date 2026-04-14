// TypeScript — common error scenarios

// Error: type mismatch
function add(a: number, b: number): number { return a + b; }
// let result = add("hello", "world");  // TS2345: Argument of type 'string'

// Error: missing case in switch
type Color = "Red" | "Green" | "Blue";
function describe(c: Color): string {
    switch (c) {
        case "Red": return "red";
        case "Green": return "green";
        // Missing "Blue" — no compiler error without exhaustive check
    }
}

// Error: possibly undefined (strictNullChecks)
function process(name: string | null): void {
    // console.log(name.length);  // TS2532: Object is possibly 'null'
    if (name !== null) {
        console.log("Length: " + name.length);
    }
}

// Error: const assignment
function main(): void {
    const x = 5;
    // x = 10;  // TS2588: Cannot assign to 'x' because it is a constant

    let y = 5;
    y = 10;  // OK
    console.log("y = " + y);
}
