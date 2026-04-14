// TypeScript — discriminated unions manually
type Result<T> =
    | { ok: true; value: T }
    | { ok: false; error: string };

function parseInt(input: string): Result<number> {
    if (input.length === 0) {
        return { ok: false, error: "empty string" };
    }
    return { ok: true, value: 42 };
}

function safeDivide(a: number, b: number): Result<number> {
    if (b === 0) {
        return { ok: false, error: "division by zero" };
    }
    return { ok: true, value: a / b };
}

function process(result: Result<number>): void {
    if (result.ok) {
        console.log("Success: " + result.value);
    } else {
        console.log("Failed: " + result.error);
    }
}

// Parse results
const good = parseInt("42");
const bad = parseInt("");
process(good);
process(bad);

// Division results
const r1 = safeDivide(10, 3);
const r2 = safeDivide(10, 0);
process(r1);
process(r2);

// Immutability
const config = "production";   // immutable
let attempts = 0;              // mutable
attempts = attempts + 1;
console.log("Attempts: " + attempts + ", Config: " + config);
