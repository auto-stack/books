# Interfaces & Enums

This chapter covers how TypeScript and Auto model contracts between types and
represent fixed sets of alternatives. These two features are foundational to
writing safe, expressive code — but Auto takes a fundamentally different
approach to enums.

## Interfaces to Specs

In TypeScript, an `interface` defines a **structural contract** — a shape that
other types must conform to. Interfaces have zero runtime impact; they exist
only as compile-time checks:

```typescript
// TypeScript
interface Greetable {
    name: string;
    greet(): void;
}

class User implements Greetable {
    constructor(public name: string) {}
    greet() {
        console.log("Hello, " + this.name);
    }
}
```

Auto uses `spec` for the same purpose — a purely structural contract with no
runtime cost:

```auto
// Auto
spec Greetable {
    fn greet()
}

type User as Greetable {
    name str
    fn greet() { print("Hello, " + self.name) }
}
```

One key difference: TypeScript interfaces are *open-ended* and support
**declaration merging** — you can extend an interface by re-declaring it in
another location. Auto specs are *closed* — once defined, their shape is fixed.
This eliminates an entire class of bugs where unexpected properties leak in
through merged declarations.

## Implementing Interfaces

TypeScript uses the `implements` keyword on classes:

```typescript
// TypeScript
class User implements Greetable, Serializable {
    // ...
}
```

Auto uses the `as` keyword on types:

<Listing name="spec-implementation" file="listings/ch05-spec-implementation">

```auto
// Auto
type User as Greetable {
    name str
    fn greet() { print("Hello, " + self.name) }
}
```

</Listing>

Auto's structural typing means the `as` keyword is technically optional — if a
type's shape matches a spec, it satisfies that spec automatically. However,
explicit `as` declarations are recommended for **documentation and intent**:
they tell readers that conformance is deliberate, not accidental.

Multiple spec implementation uses a comma-separated list:

```auto
// Auto — multiple specs
type User as Greetable, Serializable {
    name str
    fn greet() { ... }
    fn serialize() str { ... }
}
```

## TypeScript Enums vs Auto Enums

This is the **most important conceptual difference** in this chapter. Despite
sharing the name "enum," TypeScript and Auto mean fundamentally different things.

TypeScript enums are *named constants*. They generate real JavaScript objects at
runtime:

```typescript
// TypeScript — number enum (bidirectional mapping)
enum Direction {
    Up,      // 0
    Down,    // 1
    Left,    // 2
    Right    // 3
}

// TypeScript — string enum
enum Status {
    Active = "ACTIVE",
    Inactive = "INACTIVE"
}
```

TypeScript also has `const enum` (inlined at compile time) and *heterogeneous*
enums (mixing numbers and strings). All of these are just organized collections
of constants.

**Auto enums are algebraic data types** — tagged unions that can carry data
payloads:

```auto
// Auto — enum with data payloads
enum Shape {
    Circle(f64),
    Rect(f64, f64),
    Triangle(f64, f64, f64)
}
```

Each variant is not a bare constant — it wraps real data. A `Circle` *contains*
a radius, a `Rect` *contains* width and height. This makes Auto enums
dramatically more expressive than TypeScript enums.

## Pattern Matching with `is`

TypeScript uses `switch` combined with `typeof`, `in`, or property checks for
type narrowing. This is verbose and error-prone — the compiler cannot verify
that all cases are handled:

```typescript
// TypeScript — discriminated union with switch
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rect"; width: number; height: number };

function area(s: Shape): number {
    switch (s.kind) {
        case "circle":
            return Math.PI * s.radius * s.radius;
        case "rect":
            return s.width * s.height;
        // Forgot "triangle"? Compiler won't warn you.
    }
}
```

Auto provides the `is` keyword for **exhaustive pattern matching**. The
compiler verifies that every variant is handled:

```auto
// Auto — exhaustive pattern matching
fn area(s Shape) f64 {
    s is
        Circle(r) => 3.14159 * r * r
        Rect(w, h) => w * h
        Triangle(a, b, c) => {
            let s = (a + b + c) / 2
            sqrt(s * (s - a) * (s - b) * (s - c))
        }
}
```

If you add a new variant to `Shape` and forget to handle it in `area`, the
compiler produces an error. This is **exhaustiveness checking** — one of the
strongest safety guarantees Auto provides.

## Enums as Data Carriers

Auto enums replace TypeScript's *discriminated union* pattern. Consider a
`Result` type that represents either success or failure:

```typescript
// TypeScript — discriminated union (verbose)
type Result<T> =
    | { tag: "Ok"; value: T }
    | { tag: "Err"; error: string };

function processResult(r: Result<number>): void {
    switch (r.tag) {
        case "Ok":
            console.log("Success: " + r.value);
            break;
        case "Err":
            console.log("Error: " + r.error);
            break;
    }
}
```

The same concept in Auto is dramatically cleaner:

```auto
// Auto — enum as data carrier
enum Result<T> {
    Ok(T),
    Err(str)
}

fn process_result(r Result<int>) {
    r is
        Ok(value) => print("Success: {value}")
        Err(msg) => print("Error: {msg}")
}
```

Auto also provides `?T` as syntactic sugar for nullable values — equivalent to
`enum Option<T> { Some(T), None }`. This eliminates the need for TypeScript's
common `T | null | undefined` pattern.

## Composition with `has`

TypeScript uses **mixins** for code reuse across class hierarchies — typically
implemented via function factories that merge prototypes at runtime. This is
complex and relies on runtime behavior.

Auto provides the `has` keyword for clean, compile-time composition:

```auto
// Auto — composition with has
type Wing {
    span f64
    fn flap() { print("Flapping!") }
}

type Duck has Wing {
    name str
}

fn main() {
    let d = Duck(name: "Donald", span: 1.2)
    d.flap()  // Duck inherits Wing's methods
}
```

`type Duck has Wing` gives `Duck` all of `Wing`'s fields and methods — no
runtime magic, no prototype manipulation. Composition is resolved entirely at
compile time. Full mixin patterns are covered in Chapter 12.

## Quick Reference

| Concept | TypeScript | Auto |
|---------|-----------|------|
| Interface definition | `interface Foo { }` | `spec Foo { }` |
| Implement interface | `class X implements Foo` | `type X as Foo { }` |
| Multiple interfaces | `class X implements A, B` | `type X as A, B { }` |
| Named constants | `enum Dir { Up, Down }` | `const { Up = 0; Down = 1 }` |
| Tagged union | `{ tag: "Ok"; value: T } \| { ... }` | `enum Result<T> { Ok(T), Err(str) }` |
| Pattern matching | `switch` + type guards | `is` keyword |
| Exhaustiveness | Manual / never type | Compiler-enforced |
| Nullable type | `T \| null` | `?T` |
| Mixin / composition | Class mixins (runtime) | `has` keyword (compile-time) |
