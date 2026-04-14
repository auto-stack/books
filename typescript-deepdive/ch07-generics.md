# Generics & Inference

Generics are one of the most powerful features in a typed language. They let you write **reusable, type-safe abstractions** that work across many types without duplicating code. Combined with *type inference*, generics give you both safety and conciseness.

## Why Generics?

Without generics, you face an uncomfortable choice: duplicate functions for every type, or use `any` and lose type safety entirely.

```typescript
// TypeScript — without generics
function identityNumber(arg: number): number { return arg; }
function identityString(arg: string): string { return arg; }
```

With generics, one function handles every type:

```typescript
// TypeScript — with generics
function identity<T>(arg: T): T { return arg; }
```

```auto
// Auto — with generics
fn identity<T>(value T) T {
    value
}
```

The type parameter `<T>` acts as a *placeholder* for whatever type the caller provides. The compiler guarantees that the input and output types match — no `any`, no runtime surprises.

## Generic Functions

A **generic function** declares one or more type parameters in angle brackets after its name. Callers usually do not need to specify the type argument explicitly — the compiler infers it from the arguments.

```typescript
function identity<T>(arg: T): T {
    return arg;
}

const a = identity(42);        // T inferred as number
const b = identity("hello");   // T inferred as string
```

```auto
fn identity<T>(value T) T {
    value
}

let a = identity(42)       // T inferred as int
let b = identity("hello")  // T inferred as str
```

```typescript
// Explicit type argument (rarely needed)
const c = identity<boolean>(true);
```

```auto
// Explicit type argument (rarely needed)
let c = identity<bool>(true)
```

When the inference is ambiguous (e.g., no arguments to guide it), you can supply the type parameter explicitly. Otherwise, let the compiler do the work.

## Generic Types

Types themselves can be parameterized. A **generic type** stores or operates on values of an unknown type `T` that the user specifies at construction time.

```typescript
class Box<T> {
    constructor(public value: T) {}
}

const intBox = new Box<number>(42);
const strBox = new Box("hello");  // T inferred as string
```

```auto
type Box<T> {
    value T
}

let intBox = Box<int>(42)
let strBox = Box("hello")  // T inferred as str
```

You can declare multiple type parameters for more complex structures:

```typescript
interface Pair<T, U> {
    first: T;
    second: U;
}
```

```auto
type Pair<T, U> {
    first T
    second U
}
```

Generic types can also define **generic methods** that introduce their own type parameters:

```auto
type Box<T> {
    value T

    fn map<U>(f fn(T) U) Box<U> {
        Box(f(self.value))
    }
}
```

Here `map` introduces a *second* type parameter `U` that is independent of `T`. The result type is `Box<U>`, not `Box<T>`.

## Generic Specs (Interfaces)

A **generic spec** defines a contract that is parameterized by type. Any type that implements the spec must satisfy the contract for the given type argument.

```typescript
interface Container<T> {
    get(): T;
    set(value: T): void;
}

class List<T> implements Container<T> {
    private items: T[] = [];
    get(): T | undefined { return this.items[0]; }
    set(value: T) { this.items.push(value); }
}
```

```auto
spec Container<T> {
    fn get() T
    fn set(value T)
}

type List<T> as Container<T> {
    items []T

    fn get() ?T {
        self.items[0]
    }

    fn set(value T) {
        self.items.push(value)
    }
}
```

Specs are Auto's equivalent of TypeScript interfaces. When a type declares `as Container<T>`, the compiler verifies that all required methods are present with matching signatures.

## Type Inference

Both TypeScript and Auto perform **type inference** — the compiler deduces types so you do not have to write them everywhere. Inference works in several contexts.

*Variable initialization* — the type is inferred from the initializer:

```typescript
const x = 42;          // number
const name = "Ada";    // string
const flags = [true, false];  // boolean[]
```

```auto
let x = 42          // int
let name = "Ada"    // str
let flags = [true, false]  // []bool
```

*Function return types* — can often be omitted when the body makes the type obvious:

```auto
fn double(n int) int {
    n * 2
}
```

*Generic type arguments* — inferred from call-site arguments:

```typescript
const result = identity("hello");  // T = string
```

```auto
let result = identity("hello")  // T = str
```

*Array literals* — the element type is inferred from the contents:

```typescript
const nums = [1, 2, 3];     // number[]
const mixed = [1, "two"];   // (number | string)[]
```

```auto
let nums = [1, 2, 3]       // []int
let mixed = [1, "two"]     // [](int | str)
```

TypeScript's `noImplicitAny` flag ensures that inference never silently falls back to `any`. Auto has no `any` type at all — inference either succeeds or the compiler reports an error.

## Generic Constraints

Sometimes a generic parameter needs to be more restricted than "any type." **Constraints** limit which types are valid for a type parameter.

```typescript
function getLength<T extends { length: number }>(arg: T): number {
    return arg.length;
}

getLength("hello");    // OK — string has .length
getLength([1, 2, 3]);  // OK — array has .length
// getLength(42);      // Error — number has no .length
```

```auto
fn get_length<T>(arg T) int where T: HasLength {
    arg.length()
}
```

In TypeScript, `extends` on a type parameter adds a constraint. In Auto, the `where` clause serves the same purpose — the compiler checks that `T` satisfies `HasLength` (a spec with a `length() int` method).

Constraints are covered in depth in later chapters. For now, remember: *constraints make generics more useful by letting you call methods on the type parameter.*

## TypeScript-Only Generic Features

TypeScript has a rich system of **type-level programming** that goes far beyond simple parameterized types. These features have no equivalent in Auto:

- **Conditional types** — `T extends U ? X : Y`
- **Mapped types** — `{ [K in keyof T]: T[K] }`
- **Template literal types** — `` `hello ${string}` ``
- **Utility types** — `Partial<T>`, `Required<T>`, `Pick<T, K>`, `Omit<T, K>`

```typescript
type Readonly<T> = { readonly [K in keyof T]: T[K] };
type NameOnly = Pick<{ name: string; age: number }, "name">;
//   ^ { name: string }
```

These constructs let you *transform types at the type level*, creating new types from existing ones. Auto deliberately omits them — generics in Auto stay simple: parameterized types, parameterized functions, and spec constraints. No type-level computation, no metaprogramming.

This design choice keeps Auto's type system easy to learn and fast to compile, while TypeScript's advanced features handle complex library typing at the cost of additional complexity.

## Quick Reference

| Concept | TypeScript | Auto |
|---|---|---|
| Generic function | `function id<T>(x: T): T` | `fn id<T>(x T) T` |
| Generic class/type | `class Box<T> { v: T }` | `type Box<T> { v T }` |
| Generic interface | `interface I<T> { get(): T }` | `spec I<T> { fn get() T }` |
| Multiple params | `<T, U>` | `<T, U>` |
| Type inference | `identity(42)` → `T = number` | `identity(42)` → `T = int` |
| Constraints | `<T extends Foo>` | `<T> where T: Foo` |
| Conditional types | `T extends U ? X : Y` | *(not supported)* |
| Mapped types | `{ [K in keyof T]: T[K] }` | *(not supported)* |
| Utility types | `Partial<T>`, `Pick<T, K>` | *(not supported)* |
