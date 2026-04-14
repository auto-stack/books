# Modern Language Features

This chapter covers modern programming language features that TypeScript
adopted from ES6+. Auto provides its own take on each of these concepts.

## Classes → Types with Methods

TypeScript uses ES6 classes with `constructor`, `extends`, and access
modifiers:

```typescript
// TypeScript
class Point {
    constructor(public x: number, public y: number) {}
    add(other: Point): Point {
        return new Point(this.x + other.x, this.y + other.y);
    }
}

class Point3D extends Point {
    constructor(x: number, y: number, public z: number) {
        super(x, y);
    }
}
```

Auto uses `type` declarations with inline methods. Inheritance uses the `is`
keyword:

<Listing name="types-with-methods" file="listings/ch02-types-with-methods">

```auto
type Point {
    x int
    y int

    fn add(other Point) Point {
        Point(self.x + other.x, self.y + other.y)
    }
}

type Point3D is Point {
    z int

    fn add(other Point3D) Point3D {
        Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
    }
}
```

</Listing>

Auto does not have `public`/`private`/`protected` access modifiers. All fields
are accessible by default (Auto favors simplicity over encapsulation via
keywords).

## Arrow Functions → Closures

TypeScript arrow functions serve two purposes: concise syntax and lexical
`this` capture:

```typescript
// TypeScript
const inc = (x: number): number => x + 1;
const nums = [1, 2, 3].map(n => n * 2);
```

Auto closures don't need to solve the `this` problem (Auto uses explicit
`self`). The concise syntax maps directly:

```auto
// Auto
let inc = (x int) => x + 1
let doubled = items.map((n int) => n * 2)
```

Function types use the `fn` keyword for annotations:

```auto
// Auto
let transform: fn(int) int = (x int) => x + 1
```

```typescript
// TypeScript
let transform: (x: number) => number = (x) => x + 1;
```

## `let` / `const` → `let` / `var`

TypeScript has `let` (mutable, block-scoped) and `const` (immutable):

```typescript
// TypeScript
let x = 5;       // mutable
const y = 10;    // immutable
```

Auto flips the defaults — `let` is immutable, `var` is mutable:

```auto
// Auto
let x = 5        // immutable — cannot reassign
var y = 10       // mutable — can reassign
```

This follows Rust's philosophy: immutability is the safe default.

## Destructuring

TypeScript supports destructuring for objects and arrays:

```typescript
// TypeScript
const { x, y } = point;
const [first, ...rest] = items;
```

Auto supports destructuring through `is` pattern matching:

```auto
// Auto
let Point { x, y } = point
```

## Spread / Rest

TypeScript uses `...` for spreading and rest parameters:

```typescript
// TypeScript
const combined = [...list1, ...list2];
const sum = (a: number, b: number, ...rest: number[]) => rest.reduce((x, y) => x + y, 0);
```

Auto does not currently have spread/rest syntax. For arrays, use `+`
concatenation or method calls. Variadic parameters use trailing `...`:

```auto
// Auto
let combined = list1 + list2

fn sum(a int, b int, ...) {
    // ... collects remaining args
}
```

## Template Strings → f-strings

TypeScript uses backtick template literals with `${}`:

```typescript
// TypeScript
const greeting = `Hello, ${name}! You are ${age} years old.`;
```

Auto uses `print()` with string interpolation using `{}`:

```auto
// Auto
print("Hello, {name}! You are {age} years old.")
```

## Iterators and `for...of`

TypeScript iterates with `for...of`:

```typescript
// TypeScript
for (const item of items) {
    console.log(item);
}
```

Auto uses `for item in collection`:

```auto
// Auto
for item in items {
    print(item)
}

// With index
for i, item in items {
    print("{i}: {item}")
}
```

For ranges, Auto uses `range()`:

```auto
// Auto
for i in range(1, 10) {
    print(i)
}
```

## Async/Await → `~T` / `on`

TypeScript uses `async`/`await`:

```typescript
// TypeScript
async function fetchData(): Promise<string> {
    const response = await fetch(url);
    return response.text();
}
```

Auto uses `~T` for async types and `.?` for awaiting:

```auto
// Auto
fn fetch_data() !str {
    let response = http_get(url)?
    response.text()?
}
```

The `!` return type means the function propagates errors (equivalent to
returning a `Promise` or `Result`). The `?` operator unwraps the value or
early-returns on error.

## Quick Reference

| TypeScript (ES6+) | Auto | Notes |
|-------------------|------|-------|
| `class` / `extends` | `type` / `is` | Auto uses structural types |
| `(x) => x + 1` | `(x int) => x + 1` | Same closure syntax |
| `fn(x: number): number` | `fn(int) int` | Function type annotation |
| `let x = 5` | `let x = 5` (immutable) | Auto defaults to immutable |
| `const x = 5` | `let x = 5` | Same semantics |
| `var x = 5` (TS — mutable) | `var x = 5` (Auto — mutable) | Same keyword, different default |
| `...spread` | Not yet supported | Use concatenation |
| `` `${expr}` `` | `{expr}` in print() | String interpolation |
| `for...of` | `for item in collection` | Auto uses `in` keyword |
| `async/await` | `!` / `?` | Error propagation model |
