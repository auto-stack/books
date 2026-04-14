// Auto — common error scenarios

// Error: type mismatch
function add(a: number, b: number): number { return a + b; }
// let result = add("hello", "world")  // Error: expected int, got str

// Error: missing enum case
enum Color { Red, Green, Blue }

function describe(c: Color): string {
    switch (c) {
        case Color.Red: return "red";
        case Color.Green: return "green";
        // Missing Blue — compiler error: non-exhaustive pattern match
    }
}

// Error: nil safety
function process(name: string | null): void {
    // console.log(name.length)  // Error: name is ?str, must check for nil first
    if (name !== null) {
        console.log("Length: " + name.length);
    } else {
        console.log("No name");
    }
}

// Error: immutability
function main(): void {
    const x = 5;
    // x = 10  // Error: cannot reassign immutable variable

    let y = 5;
    y = 10  // OK — var is mutable
    console.log("y = " + y);
}

main();
