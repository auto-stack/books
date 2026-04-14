// TypeScript — exception-based error handling
function safeDivide(a: number, b: number): { ok: true; value: number } | { ok: false; error: string } {
    if (b === 0) {
        return { ok: false, error: "division by zero" };
    }
    return { ok: true, value: a / b };
}

function parseAge(input: string): { ok: true; value: number } | { ok: false; error: string } {
    const trimmed = input.trim();
    if (trimmed.length === 0) {
        return { ok: false, error: "empty input" };
    }
    const num = parseInt(trimmed, 10);
    if (isNaN(num)) {
        return { ok: false, error: "not a number" };
    }
    return { ok: true, value: num };
}

function compute(input: string): { ok: true; value: number } | { ok: false; error: string } {
    const age = parseAge(input);
    if (!age.ok) return age;
    const result = safeDivide(100, age.value);
    if (!result.ok) return result;
    return result;
}

const r1 = compute("25");
if (r1.ok) console.log("Result: " + r1.value);
else console.log("Error: " + r1.error);

const r2 = compute("abc");
if (r2.ok) console.log("Result: " + r2.value);
else console.log("Error: " + r2.error);

const r3 = compute("0");
if (r3.ok) console.log("Result: " + r3.value);
else console.log("Error: " + r3.error);
