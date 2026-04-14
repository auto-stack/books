// Auto — discriminated unions via enum Result
type Result<T> =
  | { _tag: "Ok"; value: T }
  | { _tag: "Err"; value: string };
const Result = {
  Ok: <T>(v: T) => ({ _tag: "Ok", value: v }),
  Err: (msg: string) => ({ _tag: "Err", value: msg }),
};

function parse_int(input: string): Result<number> {
  // Simulated parsing
  if (input.length === 0) {
    return Result.Err("empty string");
  } else {
    // In real code: actual parsing logic
    return Result.Ok(42);
  }
}

function safe_divide(a: number, b: number): Result<number> {
  if (b === 0.0) {
    return Result.Err("division by zero");
  } else {
    return Result.Ok(a / b);
  }
}

function process(result: Result<number>): void {
  switch (result._tag) {
    case "Ok": {
      const value = result.value;
      console.log("Success: " + value);
      break;
    }
    case "Err": {
      const msg = result.value;
      console.log("Failed: " + msg);
      break;
    }
  }
}

function main(): void {
  // Parse results
  const good = parse_int("42");
  const bad = parse_int("");
  process(good);
  process(bad);

  // Division results
  const r1 = safe_divide(10.0, 3.0);
  const r2 = safe_divide(10.0, 0.0);
  process(r1);
  process(r2);

  // Immutability
  const config = "production";   // immutable
  let attempts: number = 0;         // mutable counter
  attempts = attempts + 1;
  console.log("Attempts: " + attempts + ", Config: " + config);
}

main();
