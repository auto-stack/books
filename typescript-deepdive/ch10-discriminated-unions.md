# Discriminated Unions & Immutability

Discriminated unions are one of the most powerful patterns for modeling data that can take
one of several distinct forms. Combined with immutability, they give you safe, predictable
code that the compiler can verify exhaustively. TypeScript supports this pattern through
manual object-shaped unions, while Auto provides it as a first-class language feature via
`enum`.

## What Are Discriminated Unions?

A **discriminated union** uses a shared property — called the **discriminant** — to tell
the compiler which variant of a union type you are working with. Once the compiler knows
the discriminant, it narrows the type automatically, giving you access to only the fields
that belong to that variant.

In TypeScript, you build discriminated unions manually by giving every object variant a
common property:

```typescript
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rect"; width: number; height: number };
```

The `kind` property is the discriminant. Every variant carries it, and its literal value
uniquely identifies the shape.

In Auto, discriminated unions are built into the language. The `enum` keyword with data
payloads **is** a discriminated union — the variant name itself acts as the discriminant:

```auto
enum Shape {
    Circle(f64)
    Rect(f64, f64)
}
```

No manual `kind` field, no object boilerplate. The compiler knows every variant and
enforces exhaustive handling.

## TypeScript's Manual Approach

Here is the full pattern in TypeScript:

```typescript
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rect"; width: number; height: number };

function area(shape: Shape): number {
    switch (shape.kind) {
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "rect":
            return shape.width * shape.height;
    }
}
```

The verbosity is the cost. Every variant requires the `{ kind: "..."; ... }` wrapper.
Exhaustiveness checking relies on assigning to `never`:

```typescript
function area(shape: Shape): number {
    switch (shape.kind) {
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "rect":
            return shape.width * shape.height;
        default:
            const _exhaustive: never = shape;
            return _exhaustive;
    }
}
```

If you add a new variant and forget to handle it, TypeScript flags the `never` assignment.
It works, but it is a convention rather than a language guarantee.

## Auto's Native Enum Approach

Auto eliminates the boilerplate. Enums with payloads are inherently discriminated unions:

```auto
enum Shape {
    Circle(f64)
    Rect(f64, f64)
}

fn area(s Shape) f64 {
    s is
        Circle(r) => 3.14159 * r * r
        Rect(w, h) => w * h
}
```

The compiler **knows** every variant. If you add a new one, the `is` expression produces a
compile-time error unless you handle it. No `never` trick needed — exhaustiveness is
guaranteed by the language.

This is the most natural data modeling pattern in Auto. Use enums to represent anything
that can be one of several distinct cases: shapes, results, messages, states, AST nodes.

## The Result Pattern

One of the most practical uses of discriminated unions is **explicit error handling**. In
TypeScript, you build it manually:

```typescript
type Result<T> =
    | { ok: true; value: T }
    | { ok: false; error: string };
```

In Auto, it is a one-liner:

```auto
enum Result<T> {
    Ok(T)
    Err(str)
}
```

Auto's `Result` replaces `try`/`catch` with values you pass around. Errors are not
exceptions — they are data. The compiler forces you to acknowledge both `Ok` and `Err`
at every call site.

<Listing name="result-type" file="listings/ch10-result-type">

The listing shows a complete example: parsing integers, safe division, and pattern
matching on `Result`. It also demonstrates immutability with `let` and `var`.

</Listing>

## Immutability with `let`

TypeScript and Auto take opposite default stances on variable mutability:

| Concept | TypeScript | Auto |
|---------|-----------|------|
| Immutable binding | `const` | `let` |
| Mutable binding | `let` | `var` |

This is a common source of confusion. TypeScript's `let` allows reassignment; Auto's
`let` **does not**. In Auto, you must opt into mutability with `var`.

```typescript
// TypeScript
const name = "production";   // cannot reassign
let attempts = 0;            // can reassign
attempts = attempts + 1;     // fine
```

```auto
// Auto
let name = "production"      // cannot reassign
var attempts int = 0          // can reassign
attempts = attempts + 1       // fine
```

Auto's choice makes `let` the safe default. You see at a glance which variables might
change — they are the ones declared with `var`.

## Readonly in Depth

TypeScript offers three levels of `readonly` protection:

```typescript
// 1. Readonly property modifier
interface Config {
    readonly name: string;
    readonly port: number;
}

// 2. Readonly utility type (shallow)
type FrozenConfig = Readonly<Config>;

// 3. Readonly arrays
const items: ReadonlyArray<string> = ["a", "b"];
```

The `readonly` modifier prevents reassignment of individual properties. `Readonly<T>`
applies it to every property in a type. Both are **shallow** — nested objects remain
mutable unless you apply `Readonly` recursively.

Auto takes a simpler approach. `let` gives you an immutable binding. For deep
immutability, use immutable data structures. There is no `readonly` keyword because
immutability is the default:

```auto
let config = {name: "production", port: 8080}
// config.name = "staging"  // compile error — config is let
```

When you need mutation, wrap it in `var` and the compiler tracks the scope precisely.

## Quick Reference

| Concept | TypeScript | Auto |
|---------|-----------|------|
| Define discriminated union | `type T = { kind: "a"; ... } \| { kind: "b"; ... }` | `enum T { A(...), B(...) }` |
| Match on variant | `switch (x.kind)` | `x is A(v) => ...` |
| Exhaustiveness check | `const _: never = x` | Automatic at compile time |
| Result type | `type Result<T> = { ok: true; value: T } \| { ok: false; error: string }` | `enum Result<T> { Ok(T), Err(str) }` |
| Immutable variable | `const x = 5` | `let x = 5` |
| Mutable variable | `let x = 5` | `var x = 5` |
| Readonly property | `readonly name: string` | `let` binding (default) |
| Readonly all properties | `Readonly<T>` | Default with `let` |
| Readonly array | `ReadonlyArray<T>` | Immutable by default |
