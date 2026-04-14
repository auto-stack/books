# Everyday Types

In this chapter, we cover the everyday types you will use most often in Auto and
how they map to their TypeScript equivalents.

## The Primitives: `string`, `number`, and `boolean`

TypeScript has three core primitives: `string`, `number`, and `boolean`. Auto
provides shorter aliases for each:

| TypeScript | Auto   |
|-----------|--------|
| `string`  | `str`  |
| `number`  | `int`, `float` |
| `boolean` | `bool` |

Auto distinguishes between `int` and `float`, but both transpile to TypeScript's
`number` type since TypeScript does not separate integer and floating-point
types at runtime.

<Listing number="02-01" file="listings/ch02/listing-02-01/main.at" caption="The primitives">

```auto
fn main() {
    let name = "Alice"
    let age = 25
    let is_active = true
    print(name)
    print(age)
    print(is_active)
}
```

```typescript
function main(): void {
    const name: string = "Alice";
    const age: number = 25;
    const is_active: boolean = true;
    console.log(name);
    console.log(age);
    console.log(is_active);
}

main();
```

</Listing>

As you can see, Auto infers the types automatically. `"Alice"` is inferred as
`str`, `25` is inferred as `int`, and `true` is inferred as `bool`. You can
also annotate types explicitly:

```auto
let name str = "Alice"
let age int = 25
let is_active bool = true
```

Note that Auto uses a space (not a colon) between the variable name and its
type annotation.

## Arrays

To specify an array type in TypeScript, you write `number[]` or `string[]`. In
Auto, the syntax is reversed: you write `[]int` or `[]str`. This places the
element type after the bracket notation, which is consistent with Auto's
general pattern of putting types after names.

<Listing number="02-02" file="listings/ch02/listing-02-02/main.at" caption="Arrays">

```auto
fn main() {
    let nums = [1, 2, 3]
    let names = ["Alice", "Bob", "Charlie"]
    for n in nums {
        print(n)
    }
    for name in names {
        print(name)
    }
}
```

```typescript
function main(): void {
    const nums: number[] = [1, 2, 3];
    const names: string[] = ["Alice", "Bob", "Charlie"];
    for (const n of nums) {
        console.log(n);
    }
    for (const name of names) {
        console.log(name);
    }
}

main();
```

</Listing>

Auto's `for ... in` iterates over elements (not indices), which maps to
TypeScript's `for ... of` loop. If you need indices, use the `enumerate`
function:

```auto
for (i, name) in enumerate(names) {
    print(f"${i}: ${name}")
}
```

## Functions

Functions in Auto use the `fn` keyword. Parameter types are annotated with a
space (not a colon), and the return type follows the parameter list.

<Listing number="02-03" file="listings/ch02/listing-02-03/main.at" caption="Function type annotations">

```auto
fn add(a int, b int) int {
    return a + b
}

fn greet(name str) {
    print(f"Hello, ${name}!")
}

fn main() {
    let result = add(5, 3)
    print(result)
    greet("Alice")
}
```

```typescript
function add(a: number, b: number): number {
    return a + b;
}

function greet(name: string): void {
    console.log(`Hello, ${name}!`);
}

function main(): void {
    const result = add(5, 3);
    console.log(result);
    greet("Alice");
}

main();
```

</Listing>

Functions without an explicit return type are inferred. If a function does not
return a value, the transpiler emits `: void` in the TypeScript output.

For function type expressions, Auto uses a concise arrow syntax:

| TypeScript | Auto |
|-----------|------|
| `(a: number, b: number) => number` | `(a int, b int) => int` |
| `(name: string) => void` | `(name str) =>` |

When the return type is `void`, you can omit it entirely in Auto.

## Object Types

In TypeScript, you define object shapes with interfaces or inline types like
`{ name: string; age: number }`. Auto uses the `type` keyword to define named
object types with fields:

<Listing number="02-04" file="listings/ch02/listing-02-04/main.at" caption="Object types">

```auto
type User {
    name str
    age int
}

fn main() {
    let user = User("Alice", 30)
    print(f"${user.name} is ${user.age} years old")
}
```

```typescript
class User {
    name: string;
    age: number;

    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }
}

function main(): void {
    const user = User("Alice", 30);
    console.log(`${user.name} is ${user.age} years old`);
}

main();
```

</Listing>

Auto's `type Name { fields }` transpiles to a TypeScript `class` with a
constructor. The constructor parameters are positional, matching the order the
fields are declared. This gives you a concise way to create typed objects
without boilerplate.

For structural contracts (like TypeScript's `interface`), Auto provides the
`spec` keyword, which is covered in a later chapter.

## Nullable Types with Enums

TypeScript uses `T | null` to represent a value that might be missing. In Auto,
you model nullable types using enums with tagged variants. This is inspired by
Rust's `Option<T>` and gives you exhaustive pattern matching at compile time.

<Listing number="02-05" file="listings/ch02/listing-02-05/main.at" caption="Nullable types with enum">

```auto
enum MaybeId {
    Just int
    Nothing
}

fn process_id(id MaybeId) {
    is id {
        MaybeId.Just(n) => print("ID:", n)
        MaybeId.Nothing => print("No ID provided")
    }
}

fn main() {
    let a = MaybeId.Just(42)
    process_id(a)
    process_id(MaybeId.Nothing)
}
```

```typescript
type MaybeId =
    { _tag: "Just", value: number }
    | { _tag: "Nothing", value: void };

const MaybeId = {
    Just: (value: number) => ({ _tag: "Just", value }),
    Nothing: (value: void) => ({ _tag: "Nothing", value })
};


function process_id(id: MaybeId): void {
    switch (id) {
        case MaybeId.Just(n):
            console.log("ID:", n);
            break;
        case MaybeId.Nothing(_):
            console.log("No ID provided");
            break;
    }
}

function main(): void {
    const a = MaybeId.Just(42);
    process_id(a);
    process_id(MaybeId.Nothing);
}

main();
```

</Listing>

The enum `MaybeId` transpiles to a discriminated union type in TypeScript. Each
variant becomes a `{ _tag: "...", value: T }` object, and the enum namespace
provides constructor functions like `MaybeId.Just(42)`. The `is` expression
transpiles to a `switch` statement with pattern matching on the `_tag` field.

This approach gives you exhaustive matching — the compiler ensures you handle
every case. In TypeScript, you would typically use `T | null` instead, but
Auto's enum approach is safer and more explicit.

For string-based nullable types, you can define a similar enum:

```auto
enum MaybeName {
    Just str
    Nothing
}
```

Note: Auto reserves `Some` and `None` as keywords. Use `Just` and `Nothing`
(or any other non-keyword names) for your enum variants.

## Optional Parameters

TypeScript supports optional parameters with `?`: `function greet(name: string,
greeting?: string)`. Auto uses the same `?` prefix on the parameter name to
mark it as optional.

<Listing number="02-06" file="listings/ch02/listing-02-06/main.at" caption="Optional function parameters">

```auto
fn greet(name str, greeting? str) {
    if greeting {
        print(f"${greeting}, ${name}!")
    } else {
        print(f"Hello, ${name}!")
    }
}

fn main() {
    greet("Alice")
    greet("Bob", "Hi")
}
```

```typescript
function greet(name: string, greeting: string | null): void {
    if (greeting) {
        console.log(`${greeting}, ${name}!`);
    } else {
        console.log(`Hello, ${name}!`);
    }
}

function main(): void {
    greet("Alice");
    greet("Bob", "Hi");
}

main();
```

</Listing>

Optional parameters in Auto transpile directly to TypeScript's optional
parameters (`param?: T`). The `if greeting` check works because Auto treats
`null` and `undefined` as falsy, just like TypeScript.

## Type Aliases

TypeScript's `type` keyword creates aliases for existing types. Auto supports
the same concept with a simpler syntax:

```auto
type ID = int
type Name = str
type UserList = []User
```

This transpiles directly to:

```typescript
type ID = number;
type Name = string;
type UserList = User[];
```

Type aliases are useful for giving meaningful names to complex types and for
keeping your code self-documenting.

## Quick Reference

| TypeScript | Auto | Description |
|-----------|------|-------------|
| `string` | `str` | Text |
| `number` | `int`, `float` | Numeric |
| `boolean` | `bool` | True/false |
| `T[]` | `[]T` | Array |
| `T \| null` | enum with `Just`/`Nothing` | Nullable |
| `{ name: string }` | `type Obj { name str }` | Object |
| `(a: number) => void` | `(a int) =>` | Function type |

## TypeScript-Only Features

The following TypeScript features do not have direct equivalents in Auto.

### The `any` Type

TypeScript's `any` type disables type checking entirely. Auto does not have an
`any` type -- the language is designed to be type-safe. If you need to work
with dynamically-typed data, use explicit nullable types or union types
instead.

```typescript
// TypeScript only
let data: any = JSON.parse(input);
```

### Tuple Types

TypeScript supports fixed-length arrays with typed positions, called tuples:

```typescript
// TypeScript only
let pair: [number, string] = [1, "hello"];
```

Auto does not have tuple types. Use a named `type` with fields instead:

```auto
type Pair {
    first int
    second str
}

let pair = Pair(1, "hello")
```

### Literal Types

TypeScript allows you to use specific values as types:

```typescript
// TypeScript only
let direction: "left" | "right" = "left";
```

Auto does not support literal types. Use an `enum` or a `str` with validation
instead:

```auto
enum Direction {
    Left
    Right
}

let direction = Direction::Left
```
