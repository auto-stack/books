# Mixins & Error Handling

Code reuse across class hierarchies and handling failure gracefully are two challenges
every program faces. TypeScript solves the first with **mixins** — functions that
extend class prototypes at runtime — and the second with **exceptions** — `try`/`catch`
blocks. Auto takes a different path: `has` composition for sharing behavior, and
`Result<T>` with the `?` operator for explicit error handling.

## The Mixin Problem

TypeScript does not support multiple inheritance. Instead, it uses a **mixin pattern**:
a function that takes a class constructor and returns a new class extending it. Each
mixin adds a slice of functionality, and you chain them together.

```typescript
// TypeScript — mixin pattern
type Constructor<T> = new (...args: any[]) => T;

function Timestamped<T extends Constructor<{}>>(Base: T) {
    return class extends Base {
        created = new Date();
        getTimestamp() {
            return `created at ${this.created.toISOString()}`;
        }
    };
}

function Activatable<T extends Constructor<{}>>(Base: T) {
    return class extends Base {
        isActive = false;
        activate() { this.isActive = true; }
        deactivate() { this.isActive = false; }
    };
}

class User {
    constructor(public name: string) {}
}

const EnhancedUser = Activatable(Timestamped(User));
const u = new EnhancedUser("Alice");
u.activate();
console.log(u.getTimestamp()); // "created at 2024-..."
console.log(u.isActive);       // true
```

This works, but the cost is significant. Mixins rely on **runtime prototype
manipulation**, and the `Constructor<T>` type gymnastics are hard to read. The
type information for composed members is often incomplete, and IDE support can be
spotty.

## Auto's `has` Composition

Auto replaces mixins with `has` — **compile-time composition**. You declare reusable
behavior blocks and compose them into types with a single line:

```auto
// Auto — has composition
type Timestamped {
    created_at int
    fn created() str { "created at {self.created_at}" }
}

type Activatable {
    var is_active bool
    fn activate() { self.is_active = true }
    fn deactivate() { self.is_active = false }
}

type User has Timestamped, Activatable {
    name str
}

fn main() {
    let u = User(created_at: 1710000000, is_active: false, name: "Alice")
    u.activate()
    print(u.created())   // "created at 1710000000"
    print(u.is_active)   // true
    print(u.name)        // "Alice"
}
```

`type User has Timestamped, Activatable` gives `User` **all** fields and methods
from both composed types. No runtime magic, no prototype chains, no constructor
wrappers. The compiler resolves everything at compile time, and every member has
full type information.

You can compose as many types as you need. If two composed types define methods
with the same name, the compiler reports an error — no silent overrides.

## TypeScript Exception Handling

JavaScript and TypeScript use `try`/`catch`/`throw` for error handling. The pattern
is familiar but has a fundamental weakness: **exceptions are invisible in the type
system**.

```typescript
// TypeScript — try/catch
function parseJSON(input: string): any {
    try {
        return JSON.parse(input);
    } catch (e) {
        if (e instanceof SyntaxError) {
            console.error("Invalid JSON:", e.message);
            return null;
        }
        throw e; // re-throw unexpected errors
    }
}

try {
    const data = parseJSON('{"name": "Alice"}');
    console.log(data.name);
} catch (e) {
    console.error("Failed:", e);
}
```

Always throw `Error` objects, not raw strings. Built-in error types include
`RangeError`, `ReferenceError`, `SyntaxError`, and `TypeError`. You can also
create custom error classes by extending `Error`.

The problem: **any function can throw, and the type signature does not tell you**.
There is no way to know from `function parseJSON(input: string): any` that it might
throw a `SyntaxError`. You must read the documentation or the source code.

## Auto's Result-Based Error Handling

Auto replaces exceptions with `enum Result<T>` for **expected failures** — things
like parsing errors, missing files, validation failures, and network timeouts.
Functions return `Result<T>`, and the caller **must** handle both `Ok` and `Err`:

```auto
// Auto — Result type
enum Result<T> {
    Ok(T),
    Err(str)
}

fn safe_divide(a f64, b f64) Result<f64> {
    if b == 0.0 {
        Result.Err("division by zero")
    } else {
        Result.Ok(a / b)
    }
}
```

The return type `Result<f64>` **tells you** this function can fail. The compiler
enforces that you handle both cases at every call site. No surprises at runtime.

```auto
let r = safe_divide(10.0, 0.0)
r is
    Ok(v) => print("Result: {v}")
    Err(e) => print("Error: {e}")
```

## Error Propagation with `?`

When a function calls multiple fallible operations, TypeScript nests `try`/`catch`
blocks or uses early returns with manual checks. Auto's `?` operator unwraps `Ok`
or early-returns `Err` — letting you chain operations linearly:

```typescript
// TypeScript — manual error propagation
function compute(input: string): { ok: true; value: number } | { ok: false; error: string } {
    const age = parseAge(input);
    if (!age.ok) return age;
    const result = safeDivide(100, age.value);
    if (!result.ok) return result;
    return result;
}
```

```auto
// Auto — ? operator for error propagation
fn compute(input str) Result<f64> {
    let age = parse_age(input)?
    let result = safe_divide(100.0, f64(age))?
    Result.Ok(result)
}
```

The `?` operator does one thing: if the value is `Ok(v)`, it unwraps `v`; if it is
`Err(e)`, it immediately returns `Err(e)` from the enclosing function. This makes
multi-step pipelines read as straight-line code instead of nested conditionals.

## When to Use Each Approach

| Scenario | TypeScript | Auto |
|----------|-----------|------|
| Expected failure (parse, validate) | `try`/`catch` or manual Result | `Result<T>` — explicit in type |
| Error propagation | Nested `try`/`catch` | `?` operator |
| Truly exceptional (bug, assert) | `throw` | `panic()` |
| Code reuse across classes | Mixin functions | `has` composition |

Auto's approach makes **error handling paths visible in the type system**. When you
read a function signature, you know immediately whether it can fail and what kind
of error it produces. In TypeScript, that information lives only in documentation
and source code.

<Listing name="error-result" file="listings/ch12-error-result">

The listing shows a complete example of `Result`-based error handling in Auto,
including safe division, input parsing, the `?` operator for propagation, and
pattern matching on results. The TypeScript equivalent uses manual discriminated
unions and explicit error checks.

</Listing>

## Quick Reference

| Concept | TypeScript | Auto |
|---------|-----------|------|
| Code reuse across classes | Mixin functions with `Constructor<T>` | `has` composition |
| Compose multiple behaviors | Chain mixin functions | `type X has A, B, C` |
| Expected error handling | `try`/`catch`/`throw` | `enum Result<T>` |
| Error in type signature | Not represented | `Result<T>` return type |
| Error propagation | Nested `try`/`catch` or manual checks | `?` operator |
| Pattern match on result | `if (r.ok) ... else ...` | `r is Ok(v) => ... Err(e) => ...` |
| Unrecoverable error | `throw new Error(msg)` | `panic(msg)` |
