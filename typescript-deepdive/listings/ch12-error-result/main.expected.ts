type Result<T> = { _tag: "Ok"; value: T } | { _tag: "Err"; value: string };
const Result = { Ok: (value) => ({ _tag: "Ok", value }), Err: (value) => ({ _tag: "Err", value: value }) };

function safe_divide(a: number, b: number): Result<number> {
    if (b === 0.0) {
        return Result.Err("division by zero");
    } else {
        return Result.Ok(a / b);
    }
}

function parse_age(input: string): Result<number> {
    const trimmed = input.trim();
    if (trimmed.length === 0) {
        return Result.Err("empty input");
    } else if (trimmed[0] < '0' || trimmed[0] > '9') {
        return Result.Err("not a number");
    } else {
        return Result.Ok(parseInt(trimmed));
    }
}

function compute(input: string): Result<number> {
    const age = parse_age(input);
    if (age._tag === "Err") return age;
    const result = safe_divide(100.0, age.value);
    if (result._tag === "Err") return result;
    return Result.Ok(result.value);
}

function main(): void {
    const r1 = compute("25");
    switch (r1._tag) {
        case "Ok": console.log("Result: " + r1.value); break;
        case "Err": console.log("Error: " + r1.value); break;
    }

    const r2 = compute("abc");
    switch (r2._tag) {
        case "Ok": console.log("Result: " + r2.value); break;
        case "Err": console.log("Error: " + r2.value); break;
    }

    const r3 = compute("0");
    switch (r3._tag) {
        case "Ok": console.log("Result: " + r3.value); break;
        case "Err": console.log("Error: " + r3.value); break;
    }
}

main();
