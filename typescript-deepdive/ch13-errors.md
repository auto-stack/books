# Errors & Diagnostics

A type system is only as useful as the errors it produces. TypeScript has invested heavily in **clear, actionable diagnostic messages** that tell you not just *what* went wrong, but *why*. Understanding how to read these messages, and how Auto's design prevents entire categories of errors, is a practical skill you will use every day.

## Reading Error Messages

TypeScript error messages come in two forms. The **succinct** form is what you see in terminal output from `tsc`:

```
error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
```

The **detailed** form is what your IDE shows on hover. It expands the succinct message into a full chain:

```
Argument of type 'string' is not assignable to parameter of type 'number'.
  The call would succeed against 'number', but fails for 'string'.
```

Each line in the chain answers a successive **"WHY?"** question. The first line states the problem. The second line explains the underlying type relationship. Longer chains may show generic instantiation steps or property-level mismatches.

The key insight: **read the chain from top to bottom**. The top line names the error; each subsequent line provides one more layer of context. When the chain references generic types or union members, the final line is usually the most actionable — it tells you exactly which types are incompatible.

Auto error messages follow the same philosophy. When a type mismatch occurs, the compiler explains the expected type, the actual type, and the context in which the mismatch was detected. The goal is always to get you to the fix as quickly as possible.

## TypeScript Error Codes

Every TypeScript error has a numeric code. Here are the ones you will encounter most often:

| Code | Meaning |
|------|---------|
| `TS2304` | Cannot find name |
| `TS2307` | Cannot find module |
| `TS2322` | Type is not assignable |
| `TS2339` | Property does not exist on type |
| `TS2345` | Argument type mismatch |
| `TS2532` | Object is possibly `undefined` |

Error codes make errors **searchable**. When you see `TS2532`, you can search for it directly rather than describing the problem in natural language. This is especially valuable for less common codes.

To suppress a specific error, TypeScript provides two comment directives:

```typescript
// @ts-expect-error — documents that the next line IS expected to error
// @ts-ignore       — suppresses the next line's error silently
```

Prefer `@ts-expect-error` over `@ts-ignore`. If the error goes away (because you fixed it), `@ts-expect-error` will itself produce a warning, prompting you to clean up the now-unnecessary directive. `@ts-ignore` hides silently and can mask real bugs.

Auto uses error codes for the same reason — they make compiler errors searchable and consistent across versions.

## Common TypeScript Errors

**TS2304 — Cannot find name.** You forgot to import a type or variable, or the declaration file is missing.

```typescript
// Error: Cannot find name 'User'.
const user: User = { name: "Alice" };
```

Fix: add `import { User } from "./models";`

**TS2307 — Cannot find module.** The module path is wrong, or the `@types` package is not installed.

```typescript
// Error: Cannot find module 'lodash'.
import _ from "lodash";
```

Fix: run `npm install @types/lodash` or correct the path.

**TS2322 — Type mismatch.** The most common TypeScript error. You are assigning a value of one type where another is expected.

```typescript
let age: number = "twenty";  // TS2322: Type 'string' is not assignable to 'number'
```

Fix: ensure the value matches the declared type, or widen the type annotation.

**TS2532 — Object is possibly undefined.** The `strictNullChecks` flag catches potential null or undefined access.

```typescript
function getLength(s: string | undefined): number {
    return s.length;  // TS2532: Object is possibly 'undefined'
}
```

Fix: add a null check before accessing the property.

**TS2345 — Argument type mismatch.** A function argument does not match the parameter type.

```typescript
function greet(name: string): void { console.log("Hello, " + name); }
greet(42);  // TS2345: Argument of type 'number' is not assignable to 'string'
```

Fix: convert the argument to the expected type.

## Auto's Diagnostic Philosophy

Auto eliminates entire categories of errors **by design**:

- **No `any`** — there are no "implicit any" errors because the type is always known or explicitly declared.
- **No `null`/`undefined` duality** — there are no "possibly undefined" errors. Optional values use `?T` (`Option<T>`), which forces explicit handling.
- **Explicit `self`** — there are no "this is possibly undefined" or "this context lost" errors. Methods declare `self` explicitly, and the compiler ensures it is always available.
- **No semicolons** — there are no "missing semicolon" or "unexpected semicolon" parsing errors.
- **`let` is immutable by default** — reassignment requires `var`, which means accidental mutation is caught at compile time.

When Auto does report errors, they follow the same chain pattern as TypeScript: the error code, a description of the problem, and context explaining why the types are incompatible. The difference is that many errors TypeScript developers encounter daily simply **cannot happen** in Auto.

## Type Errors in Practice

Here are common error scenarios and how Auto prevents them.

**Missing return value.** In TypeScript, a function declared with a return type may silently return `undefined` if you forget a `return` statement. Auto uses **implicit return** — the last expression in a function body is the return value. There is no way to "forget" a return.

**Unused variables.** Both TypeScript and Auto warn about unused variables. In TypeScript, this is controlled by the `noUnusedLocals` compiler option. Auto always warns, because unused variables are almost always a mistake.

**Type mismatch in generics.** Both languages report type mismatches in generic instantiation. The difference is that Auto has fewer escape hatches — there is no `any` cast and no type assertion operator that can bypass the type system. If the types do not match, you must fix the types, not suppress the error.

**Missing enum case in pattern match.** In TypeScript, a `switch` statement does not enforce exhaustiveness by default. You need the `never` type trick or a lint rule. Auto's `is` pattern match **always checks exhaustiveness**. If you add a new variant to an enum, every `is` expression that matches on it will produce a compile error until all cases are handled.

## Debugging Type Errors

When you encounter a type error, follow these strategies:

1. **Read the error chain from top to bottom.** The first line names the error; subsequent lines explain why.
2. **Hover over types in your IDE.** Place your cursor on a variable to see its inferred type. Often the inferred type is wider than expected.
3. **Guide inference with annotations.** In TypeScript, use `as Type` or explicit annotations. In Auto, add explicit type annotations to help the compiler resolve ambiguity.
4. **Isolate the error.** Extract the problematic expression into a small, self-contained example. This removes noise and makes the type relationships clear.
5. **Document intentional mismatches.** In TypeScript, use `// @ts-expect-error` with a comment explaining why the mismatch is expected. In Auto, if a type mismatch is intentional, reconsider the design — the type system is telling you something.

The single most effective strategy is **reading the error message fully before reaching for a fix**. Most TypeScript error chains contain the complete diagnosis. The fix is usually obvious once you understand what the chain is telling you.

<Listing name="common-errors" file="listings/ch13-common-errors">

```auto
// Auto — common error scenarios

// Error: type mismatch
fn add(a int, b int) int { a + b }
// let result = add("hello", "world")  // Error: expected int, got str

// Error: missing enum case
enum Color { Red, Green, Blue }

fn describe(c Color) str {
    c is
        Red => "red"
        Green => "green"
        // Missing Blue — compiler error: non-exhaustive pattern match
}

// Error: nil safety
fn process(name ?str) {
    // print(name.len())  // Error: name is ?str, must check for nil first
    name is
        Some(n) => print("Length: {n.len()}")
        None => print("No name")
}

// Error: immutability
fn main() {
    let x = 5
    // x = 10  // Error: cannot reassign immutable variable

    var y = 5
    y = 10  // OK — var is mutable
    print("y = {y}")
}
```

```typescript
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
```

</Listing>

## Quick Reference

| Concept | TypeScript | Auto |
|---|---|---|
| Error code format | `TS2345` | Numeric code (same convention) |
| Error suppression | `// @ts-expect-error` | *(not available — fix the error)* |
| Possibly undefined | `TS2532` (strictNullChecks) | *(cannot happen — use `?T`)* |
| Implicit any | `TS7006` | *(cannot happen — no `any`)* |
| Missing return | `TS7030` | *(cannot happen — implicit return)* |
| Non-exhaustive switch | *(no error by default)* | Compile error (built into `is`) |
| Immutability violation | `TS2588` (const) | Compile error (`let` is immutable) |
| Type assertion escape | `x as Type` | *(not available — no escape hatch)* |
