# Why Types

This book is an in-depth exploration of the TypeScript type system and how
those concepts map to the Auto programming language. Before diving into
syntax, let's establish *why types matter*.

## The Value of Types

Types serve two fundamental purposes:

1. **Catch errors at compile time, not runtime.** It is far cheaper for the
   compiler to find a bug than for your users to find it in production.

2. **Serve as living documentation.** A function signature is a contract —
   the signature describes *what* the function does, and the body is the
   proof that it does it correctly.

Large engineering organizations (Google, Microsoft, Meta) have independently
arrived at this conclusion: typed codebases are easier to maintain, refactor,
and scale.

## Auto's Approach: Types by Default

Unlike TypeScript, where types are *optional* (JavaScript is valid TypeScript),
Auto makes types a first-class part of the language. Every variable, function
parameter, and return value has a type — either explicitly annotated or
inferred by the compiler.

```auto
// Explicit type annotation
let name str = "Auto"

// Type inferred from context
let count = 42          // inferred as int
let items = [1, 2, 3]   // inferred as List<int>
```

```typescript
// Explicit type annotation
let name: string = "Auto";

// Type inferred from context
let count = 42;          // inferred as number
let items = [1, 2, 3];   // inferred as number[]
```

Auto uses **space-separated** type annotations (no colon), which keeps the
syntax clean and unambiguous:

```auto
fn greet(name str) {
    print("Hello, " + name)
}
```

```typescript
function greet(name: string): void {
    console.log("Hello, " + name);
}
```

## Types are Structural

Both Auto and TypeScript use **structural typing** — a value's type is
determined by its *shape*, not its *name*. If two types have the same
structure, they are compatible, even if they were defined separately.

```auto
type Point2D {
    x int
    y int
}

type Point3D {
    x int
    y int
    z int
}

fn printX(p Point2D) {
    print(p.x)
}

fn main() {
    let p2 = Point2D(1, 2)
    let p3 = Point3D(1, 2, 3)
    printX(p2)   // exact match
    printX(p3)   // extra fields okay — structural typing
}
```

```typescript
interface Point2D { x: number; y: number; }
interface Point3D { x: number; y: number; z: number; }

function printX(p: Point2D): void {
    console.log(p.x);
}

const p2: Point2D = { x: 1, y: 2 };
const p3: Point3D = { x: 1, y: 2, z: 3 };
printX(p2);  // exact match
printX(p3);  // extra fields okay — structural typing
```

This is different from nominally typed languages (like Java or Rust's
structs) where you must explicitly declare inheritance or trait
implementation.

## Immutability by Default

Auto follows the philosophy that **immutability is the safe default**:

```auto
let x = 5        // immutable — cannot reassign
var y = 5        // mutable — can reassign with `=`
```

```typescript
const x = 5;     // immutable — cannot reassign
let y = 5;       // mutable — can reassign with =
```

This is a stricter default than TypeScript's `let` (which is mutable), but
it catches entire categories of bugs at compile time.

## Auto Transpiles to TypeScript

Auto is not interpreted — it compiles ahead-of-time to TypeScript (or Rust),
which then runs on any JavaScript engine (or native). This means:

- Auto gets **compile-time type checking** from its own type system
- The generated TypeScript code runs on **existing JavaScript runtimes**
- You can interoperate with any TypeScript/JavaScript library

## What This Book Covers

This book goes deeper than a quick-start guide. We cover:

- **Type system fundamentals** — annotations, inference, compatibility
- **Advanced patterns** — generics, discriminated unions, mixins
- **Type theory** — covariance, contravariance, structural vs nominal typing
- **Design patterns** — singleton, currying, event emitters
- **Error handling** — philosophy and practical patterns
- **Compiler architecture** — how Auto's compiler pipeline works

## Quick Reference

| Concept | TypeScript | Auto |
|---------|-----------|------|
| Immutable variable | `const x = 5` | `let x = 5` |
| Mutable variable | `let x = 5` | `var x = 5` |
| Type annotation | `x: number` | `x int` |
| Function | `function` / `=>` | `fn` / `=>` |
| Interface | `interface` | `spec` |
| Class | `class` | `type` |
| Inheritance | `extends` | `is` |
| Composition | — | `has` |
| Pattern matching | `switch` / `typeof` | `is` |
| Print | `console.log()` | `print()` |
