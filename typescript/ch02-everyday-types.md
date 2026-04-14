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
/**
 * AutoLang TypeScript Runtime
 */
const print = console.log.bind(console);

function range(start: number, end: number, eq: boolean = false): number[] {
    const res: number[] = [];
    if (eq) {
        for (let i = start; i <= end; i++) res.push(i);
    } else {
        for (let i = start; i < end; i++) res.push(i);
    }
    return res;
}

function main(): void {
    const name = "Alice";
    const age = 25;
    const is_active = true;
    print(name);
    print(age);
    print(is_active);
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
/**
 * AutoLang TypeScript Runtime
 */
const print = console.log.bind(console);

function range(start: number, end: number, eq: boolean = false): number[] {
    const res: number[] = [];
    if (eq) {
        for (let i = start; i <= end; i++) res.push(i);
    } else {
        for (let i = start; i < end; i++) res.push(i);
    }
    return res;
}

function main(): void {
    const nums = [1, 2, 3];
    const names = ["Alice", "Bob", "Charlie"];
    for (const n of nums) {
        print(n);
    }
    for (const name of names) {
        print(name);
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
/**
 * AutoLang TypeScript Runtime
 */
const print = console.log.bind(console);

function range(start: number, end: number, eq: boolean = false): number[] {
    const res: number[] = [];
    if (eq) {
        for (let i = start; i <= end; i++) res.push(i);
    } else {
        for (let i = start; i < end; i++) res.push(i);
    }
    return res;
}

function add(a: number, b: number): number {
    return a + b;
}

function greet(name: string): void {
    print(`Hello, ${name}!`);
}

function main(): void {
    const result = add(5, 3);
    print(result);
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
/**
 * AutoLang TypeScript Runtime
 */
const print = console.log.bind(console);

function range(start: number, end: number, eq: boolean = false): number[] {
    const res: number[] = [];
    if (eq) {
        for (let i = start; i <= end; i++) res.push(i);
    } else {
        for (let i = start; i < end; i++) res.push(i);
    }
    return res;
}

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
    print(`${user.name} is ${user.age} years old`);
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

## Nullable Types

TypeScript uses `T | null` to represent a value that might be missing. Auto
provides the `?T` syntax (inspired by Rust's `Option<T>`), which is more
concise and forces you to handle the `None` case explicitly.

<Listing number="02-05" file="listings/ch02/listing-02-05/main.at" caption="Nullable types">

```auto
fn process_name(name ?str) {
    name is
        Some(n) -> print(f"Hello, ${n}!")
        None -> print("No name provided")
}

fn main() {
    process_name("Alice")
    process_name(None)
}
```

```typescript
/**
 * AutoLang TypeScript Runtime
 */
const print = console.log.bind(console);

function range(start: number, end: number, eq: boolean = false): number[] {
    const res: number[] = [];
    if (eq) {
        for (let i = start; i <= end; i++) res.push(i);
    } else {
        for (let i = start; i < end; i++) res.push(i);
    }
    return res;
}

function process_name(name: string | null): void {
    switch (name) {
        case null:
            print("No name provided");
            break;
        default:
            print(`Hello, ${name}!`);
            break;
    }
}

function main(): void {
    process_name("Alice");
    process_name(null);
}

main();
```

</Listing>

The `?str` type in Auto is equivalent to TypeScript's `string | null`. The `is`
keyword provides pattern matching: `Some(n)` binds the unwrapped value to `n`,
and `None` handles the null case. This transpiles to a `switch` statement in
TypeScript.

You can unwrap a nullable value with `is` in any scope, not just function
bodies:

```auto
let name ?str = get_name()
name is
    Some(n) -> print(f"Got: ${n}")
    None -> print("No name")
```

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
/**
 * AutoLang TypeScript Runtime
 */
const print = console.log.bind(console);

function range(start: number, end: number, eq: boolean = false): number[] {
    const res: number[] = [];
    if (eq) {
        for (let i = start; i <= end; i++) res.push(i);
    } else {
        for (let i = start; i < end; i++) res.push(i);
    }
    return res;
}

function greet(name: string, greeting?: string): void {
    if (greeting) {
        print(`${greeting}, ${name}!`);
    } else {
        print(`Hello, ${name}!`);
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
| `T \| null` | `?T` | Nullable |
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
