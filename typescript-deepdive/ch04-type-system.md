# Type System Basics

This chapter covers the fundamental building blocks of TypeScript's and Auto's
type systems — primitive types, arrays, annotations, unions, and the critical
differences in how each language handles type safety.

## The `any` Escape Hatch

TypeScript provides an `any` type that **completely disables type checking** for
a value. It is an intentional escape hatch for incremental adoption, but it is
also the single most dangerous feature in the language:

```typescript
// TypeScript — the any escape hatch
let data: any = "hello";
data = 42;                // no error
data.toUpperCase();       // no error at compile time, crashes at runtime
data.someRandomMethod();  // also no error — silently broken
```

Once `any` enters your codebase, it **propagates**. Any value derived from an
`any` expression also becomes `any`, quickly eroding type safety across entire
modules.

TypeScript also offers `unknown`, a *type-safe* version of `any`. You cannot use
an `unknown` value without first narrowing its type:

```typescript
let input: unknown = "hello";
input.toUpperCase();  // ERROR — Object is of type 'unknown'
if (typeof input === "string") {
    input.toUpperCase();  // OK — narrowed to string
}
```

Auto has **no `any` type** — and no `unknown` either. Every value has a concrete,
checked type. This is not a limitation; it is a design choice that eliminates an
entire category of runtime errors at the source.

## Primitive Types

TypeScript's primitive types are inherited directly from JavaScript:

```typescript
// TypeScript — all numbers are float64
let count: number = 42;
let pi: number = 3.14159;
let name: string = "hello";
let flag: boolean = true;
let nothing: null = null;
let undef: undefined = undefined;
let sym: symbol = Symbol("id");
let big: bigint = 9007199254740991n;
```

The JavaScript `number` type is **always float64** — even integers. This leads to
well-known precision problems:

```typescript
// TypeScript
0.1 + 0.2;  // 0.30000000000000004 — not 0.3!
```

Auto provides cleaner, more explicit primitives:

<Listing name="primitives" file="listings/ch04-primitives">

```auto
// Auto — primitive types and annotations
fn main() {
    // Explicit type annotations
    let count int = 42
    let pi f64 = 3.14159
    let name str = "Auto"
    let is_ready bool = true

    // Type inference
    let sum = count + 8       // inferred as int
    let items = [1, 2, 3]     // inferred as []int

    // Nullable types
    let middle_name ?str = nil

    // Arrays
    let numbers = [10, 20, 30]
    let doubled = numbers.map((n int) => n * 2)

    print("Name: {name}")
    print("Sum: {sum}")
    print("Doubled: {doubled}")

    // Union types
    let id: int | str = 42
    id = "user-001"

    // Tuple-like types
    let pair = (1, "hello")
    print("First: {pair.0}, Second: {pair.1}")
}
```

</Listing>

Key differences in Auto's primitives:

1. **`int` and `f64` are separate types.** Integer arithmetic is exact — no
   floating-point surprises for whole numbers.
2. **`nil` unifies `null` and `undefined`.** JavaScript's two "empty" values are
   collapsed into one, simplifying null handling.
3. **No `symbol` or `bigint` built-in.** Auto covers these use cases through
   its standard library when needed.

## Arrays

Arrays are ordered, indexed collections of a single element type.

```typescript
// TypeScript — array syntax
let numbers: number[] = [1, 2, 3];
let names: string[] = ["Alice", "Bob"];
let matrix: boolean[][] = [[true, false], [false, true]];

numbers.push(4);
const last = numbers.pop();
const len = numbers.length;
const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);
```

```auto
// Auto — array syntax
let numbers []int = [1, 2, 3]
let names []str = ["Alice", "Bob"]
let matrix [][]bool = [[true, false], [false, true]]

numbers.push(4)
let last = numbers.pop()
let len = numbers.len()
let doubled = numbers.map((n int) => n * 2)
let evens = numbers.filter((n int) => n % 2 == 0)
```

Auto places the bracket **before** the type (`[]int`), following the convention
of Go and Pascal. TypeScript places it **after** (`number[]`). The meaning is
identical: a homogeneous list of values.

## Type Annotations on Variables

TypeScript uses a **colon** to annotate a variable's type:

```typescript
// TypeScript — explicit annotations
let age: number = 30;
let name: string = "Alice";
let active: boolean = true;

// TypeScript — type inference
let score = 100;        // inferred as number
let greeting = "hi";    // inferred as string
```

Auto uses **space-separated** annotations — no colon:

```auto
// Auto — explicit annotations
let age int = 30
let name str = "Alice"
let active bool = true

// Auto — type inference
let score = 100        // inferred as int
let greeting = "hi"    // inferred as str
```

In both languages, annotations are *optional* when the compiler can infer the
type from the initializer. Use explicit annotations when the intent matters
more than brevity — function parameters and public APIs are good candidates.

## Interfaces as Types

TypeScript uses `interface` to define object shapes:

```typescript
// TypeScript
interface Point {
    x: number;
    y: number;
}

let p: Point = { x: 1, y: 2 };
```

Auto unifies `type` and `interface` into a single `type` declaration. This
eliminates the common TypeScript confusion about when to use each:

```auto
// Auto
type Point {
    x f64
    y f64
}

let p Point = { x: 1, y: 2 }
```

We will explore `type` declarations in depth in [ch05](ch05-interfaces.md).

## Union and Intersection Types

**Union types** let a value be one of several types. Both TypeScript and Auto
use the `|` operator:

```typescript
// TypeScript
let id: string | number = 42;
id = "user-001";  // OK — both types are allowed
```

```auto
// Auto
let id: int | str = 42
id = "user-001"   // OK
```

**Intersection types** combine multiple types into one. TypeScript uses `&`:

```typescript
// TypeScript
interface HasId { id: number; }
interface HasName { name: string; }
type User = HasId & HasName;
```

Auto does **not** have intersection types. Instead, it uses `has` composition
to mix traits into types — a pattern we will cover in [ch05](ch05-interfaces.md)
and [ch12](ch12-composition.md).

**Nullable types** are a special case of unions. In TypeScript you write
`string | null`. Auto provides syntactic sugar:

```auto
// Auto — nullable sugar
let name ?str = nil       // equivalent to str | nil
```

The `?` prefix is concise and makes nullable types instantly recognizable in
code.

## Tuple Types

Tuples are fixed-length, positional arrays where each position has its own type.

```typescript
// TypeScript — tuple
let pair: [string, number] = ["hello", 42];
let first: string = pair[0];
let second: number = pair[1];
```

```auto
// Auto — tuple
let pair = ("hello", 42)
let first str = pair.0
let second int = pair.1
```

Tuples are useful for returning multiple values from a function, but they should
be used sparingly — a named `type` is almost always clearer.

## Quick Reference

| Concept | TypeScript | Auto |
|---------|-----------|------|
| Escape hatch | `any`, `unknown` | None — all types checked |
| Integer | `number` (float64) | `int` |
| Float | `number` (float64) | `f64` |
| String | `string` | `str` |
| Boolean | `boolean` | `bool` |
| Null / Undefined | `null`, `undefined` | `nil` |
| Nullable | `T \| null` | `?T` |
| Array | `number[]` | `[]int` |
| Annotation | `let x: number` | `let x int` |
| Object shape | `interface` / `type` | `type` |
| Union | `string \| number` | `str \| int` |
| Intersection | `A & B` | Use `has` composition |
| Tuple | `[string, number]` | `(str, int)` |
