# Type Guards & Exhaustiveness

When you work with **union types**, the compiler needs to know which variant you are dealing with at each point in the code. **Type narrowing** is the process of refining a broad type into a specific one. **Exhaustiveness checking** ensures you have handled every possible case. Together, they form the backbone of safe, predictable control flow in typed languages.

## Type Narrowing

TypeScript narrows types inside conditional blocks using `typeof`, `instanceof`, and `in` checks. Each check tells the compiler: *"inside this branch, treat the value as a more specific type."*

```typescript
// TypeScript — narrowing with typeof and instanceof
function process(value: number | string) {
    if (typeof value === "string") {
        console.log(value.toUpperCase());  // value: string
    } else {
        console.log(value.toFixed(2));     // value: number
    }
}

class Dog { bark() { console.log("woof"); } }
class Cat { meow() { console.log("meow"); } }

function speak(pet: Dog | Cat) {
    if (pet instanceof Dog) {
        pet.bark();  // pet: Dog
    } else {
        pet.meow();  // pet: Cat
    }
}
```

Auto narrows types using the `is` keyword — a **unified pattern matching** construct that replaces all three TypeScript narrowing mechanisms:

```auto
// Auto — narrowing with is
fn process(value int | str) {
    value is
        str => print(value.to_upper())
        int => print("{value}")
}

type Dog { fn bark(self) }
type Cat { fn meow(self) }

fn speak(pet Dog | Cat) {
    pet is
        Dog => pet.bark()
        Cat => pet.meow()
}
```

One keyword, one consistent syntax, for every narrowing scenario.

## `typeof` and `instanceof` Guards

TypeScript provides two built-in type guards. The `typeof` guard narrows to primitive types:

```typescript
function double(x: number | string): number | string {
    if (typeof x === "number") return x * 2;
    return x + x;
}
```

The `instanceof` guard narrows to class types:

```typescript
class FileReader { read() { return "file data"; } }
class HttpReader { fetch() { return "http data"; } }

function get_data(reader: FileReader | HttpReader): string {
    if (reader instanceof FileReader) {
        return reader.read();
    }
    return reader.fetch();
}
```

In Auto, both are expressed with `is`:

```auto
fn double(x int | str) int | str {
    x is
        int => x * 2
        str => x + x
}

type FileReader { fn read(self) str }
type HttpReader { fn fetch(self) str }

fn get_data(reader FileReader | HttpReader) str {
    reader is
        FileReader => reader.read()
        HttpReader => reader.fetch()
}
```

The `is` expression checks the runtime type and narrows the variable for each branch — no separate `typeof` or `instanceof` needed.

## Literal Types

In TypeScript, individual values can serve as types. A **literal type** restricts a variable to a single specific value:

```typescript
let direction: "North" | "South" | "East" | "West";
direction = "North";     // OK
// direction = "Up";     // Error

type Status = "loading" | "success" | "error";
```

Literal types are the foundation of **discriminated unions**, which are covered in depth in Chapter 10. When combined with a shared property, they enable exhaustive `switch` statements:

```typescript
type Action =
    | { type: "fetch"; url: string }
    | { type: "cancel"; id: number };

function handle(action: Action) {
    switch (action.type) {
        case "fetch": console.log("Fetching " + action.url); break;
        case "cancel": console.log("Cancel " + action.id); break;
    }
}
```

Auto supports the same literal type concept:

```auto
let direction "North" | "South" | "East" | "West"
direction = "North"     // OK
// direction = "Up"     // Error

type Status = "loading" | "success" | "error"
```

## User-Defined Type Guards

TypeScript lets you write **custom type guard functions** that assert a specific type using the `arg is Type` return annotation:

```typescript
function isString(value: unknown): value is string {
    return typeof value === "string";
}

function process(value: string | number) {
    if (isString(value)) {
        console.log(value.toUpperCase());  // value: string
    } else {
        console.log(value.toFixed(2));     // value: number
    }
}
```

The `value is string` part tells the compiler that when the function returns `true`, `value` is a `string`. This is powerful but verbose — you must write and maintain a separate function for each check.

Auto has **no need for user-defined type guards**. The `is` pattern match handles this natively:

```auto
fn process(value str | int) {
    value is
        str => print(value.to_upper())
        int => print("{value}")
}
```

No separate guard function, no `value is Type` return annotation. The `is` keyword *is* the type guard.

## Exhaustiveness Checking with `never`

When you have a union type, you want to make sure every variant is handled. TypeScript uses the `never` type to detect **missing cases**:

```typescript
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rect"; width: number; height: number };

function area(s: Shape): number {
    switch (s.kind) {
        case "circle": return Math.PI * s.radius * s.radius;
        case "rect": return s.width * s.height;
        default:
            const _exhaustive: never = s;
            return _exhaustive;  // Error if a case is added to Shape
    }
}
```

If you later add `{ kind: "triangle"; ... }` to `Shape`, the `never` assignment fails at compile time, alerting you that `area` is incomplete.

A common pattern is the `assertNever` helper:

```typescript
function assertNever(x: never): never {
    throw new Error("Unhandled case: " + x);
}
```

Auto's `is` keyword **inherently checks exhaustiveness**. The compiler verifies that every variant is handled:

```auto
enum Shape {
    Circle(f64),
    Rect(f64, f64)
}

fn area(s Shape) f64 {
    s is
        Circle(r) => 3.14159 * r * r
        Rect(w, h) => w * h
        // Adding a new variant here causes a compile error
}
```

No `never` hack, no `assertNever` helper — exhaustiveness is built into the language.

## The `never` Type

TypeScript's `never` is the **bottom type** — a type that no value can have. It appears in two key situations:

*Functions that never return* — they either throw or loop forever:

```typescript
function fail(message: string): never {
    throw new Error(message);
}

function infiniteLoop(): never {
    while (true) {}
}
```

*Unreachable code* — the compiler infers `never` when all possibilities are eliminated:

```typescript
type Status = "ok" | "err";
function check(s: Status) {
    if (s === "ok") return;
    else return;
    // s is never here — both cases handled
}
```

The difference between `void` and `never` is subtle but important: `void` means the function returns nothing (like `console.log`), while `never` means the function **never returns at all**.

Auto uses `!` as a return type for functions that propagate errors (similar to the `never` concept for divergence). But Auto does **not** expose `never` as a separate type — `is` pattern matching handles exhaustiveness directly, so there is no need for `assertNever` or manual `never` assignments.

<Listing name="pattern-matching" file="listings/ch09-pattern-matching">

```auto
// Auto — pattern matching and exhaustiveness
enum Shape {
    Circle(f64),
    Rect(f64, f64),
    Triangle(f64, f64, f64)
}

enum Option<T> {
    Some(T),
    None
}

fn area(s Shape) f64 {
    s is
        Circle(r) => 3.14159 * r * r
        Rect(w, h) => w * h
        Triangle(a, b, c) => {
            let s = (a + b + c) / 2.0
            sqrt(s * (s - a) * (s - b) * (s - c))
        }
}

fn describe(s Shape) str {
    s is
        Circle(r) => "Circle(r={r})"
        Rect(w, h) => "Rect({w}, {h})"
        Triangle(a, b, c) => "Triangle({a}, {b}, {c})"
}

fn process(value int | str | bool) {
    value is
        int => print("Integer: {value}")
        str => print("String length: {value.len()}")
        bool => print(if value { "true" } else { "false" })
}

fn main() {
    let shapes = [
        Shape.Circle(5.0),
        Shape.Rect(3.0, 4.0),
        Shape.Triangle(3.0, 4.0, 5.0)
    ]
    for shape in shapes {
        print(describe(shape))
        print("  area = {area(shape)}")
    }

    process(42)
    process("hello")
    process(true)
}
```

```typescript
// TypeScript — type guards and narrowing
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rect"; width: number; height: number }
    | { kind: "triangle"; a: number; b: number; c: number };

function area(s: Shape): number {
    switch (s.kind) {
        case "circle":
            return Math.PI * s.radius * s.radius;
        case "rect":
            return s.width * s.height;
        case "triangle":
            const p = (s.a + s.b + s.c) / 2;
            return Math.sqrt(p * (p - s.a) * (p - s.b) * (p - s.c));
    }
}

function describe(s: Shape): string {
    switch (s.kind) {
        case "circle": return `Circle(r=${s.radius})`;
        case "rect": return `Rect(${s.width}, ${s.height})`;
        case "triangle": return `Triangle(${s.a}, ${s.b}, ${s.c})`;
    }
}

function process(value: number | string | boolean): void {
    if (typeof value === "number") {
        console.log("Integer: " + value);
    } else if (typeof value === "string") {
        console.log("String length: " + value.length);
    } else {
        console.log(value ? "true" : "false");
    }
}

const shapes: Shape[] = [
    { kind: "circle", radius: 5 },
    { kind: "rect", width: 3, height: 4 },
    { kind: "triangle", a: 3, b: 4, c: 5 }
];
for (const shape of shapes) {
    console.log(describe(shape));
    console.log("  area = " + area(shape));
}

process(42);
process("hello");
process(true);
```

</Listing>

## Quick Reference

| Concept | TypeScript | Auto |
|---|---|---|
| Type narrowing | `typeof x === "string"` | `x is str => ...` |
| Class check | `x instanceof Foo` | `x is Foo => ...` |
| Property check | `"prop" in obj` | *(use `is` on enum/tag)* |
| Literal types | `type D = "N" \| "S"` | `type D = "N" \| "S"` |
| User-defined guard | `function isFoo(x): x is Foo` | *(not needed)* |
| Exhaustiveness | `const _: never = x` | *(built into `is`)* |
| Bottom type | `never` | `!` (error propagation) |
| Void / no return | `void` | *(implicit)* |
