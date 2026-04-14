# More on Functions

Functions in Auto use the `fn` keyword with space-separated type annotations.
This chapter covers closures, generics, optional parameters, and other
function-related features.

## Closures (Arrow Functions)

Auto supports closures using the arrow syntax `(params) => expression`. A
closure captures variables from its surrounding scope and can be assigned
to a variable or passed as an argument.

<Listing number="04-01" file="listings/ch04/listing-04-01/main.at" caption="Closures">

```auto
fn main() {
    let add = (a int, b int) => a + b
    let double = (n int) => n * 2

    print(add(3, 4))
    print(double(5))
}
```

```typescript
function main(): void {
    const add: (number, number) => any = (a: number, b: number) => a + b;
    const double: (number) => number = (n: number) => n * 2;
    

    console.log(add(3, 4));
    console.log(double(5));
}

main();
```

</Listing>

Closures with type annotations transpile directly to TypeScript arrow
functions with the same types. The parameter types are preserved in the
output.

## Generic Functions

Generics allow you to write functions that work with any type. Auto uses
the `<T>` syntax, same as TypeScript:

<Listing number="04-02" file="listings/ch04/listing-04-02/main.at" caption="Generic functions">

```auto
fn identity<T>(arg T) T {
    arg
}

fn main() {
    let a = identity(5)
    let b = identity("hello")
    print(a)
    print(b)
}
```

```typescript
function identity(arg: T): T {
    arg;
}

function main(): void {
    const a = identity(5);
    const b = identity("hello");
    console.log(a);
    console.log(b);
}

main();
```

</Listing>

The type parameter `<T>` is passed through to the TypeScript output.
TypeScript infers the concrete type from the arguments — no explicit type
argument is needed at the call site.

## Generics with Arrays

Generics work particularly well with array types. You can write functions
that accept arrays of any element type:

<Listing number="04-03" file="listings/ch04/listing-04-03/main.at" caption="Generic function with array">

```auto
fn first<T>(arr []T) T {
    arr[0]
}

fn main() {
    let nums = [1, 2, 3]
    let n = first(nums)
    print(n)
}
```

```typescript
function first(arr: T[]): T {
    arr[0];
}

function main(): void {
    const nums: number[] = [1, 2, 3];
    const n = first(nums);
    console.log(n);
}

main();
```

</Listing>

Note how `[]T` in Auto becomes `T[]` in TypeScript — the bracket placement
is reversed.

## Optional Parameters

Optional parameters use the `?` prefix on the parameter name. An optional
parameter can be omitted at the call site, and its type becomes `T | null`
in the function body.

<Listing number="04-05" file="listings/ch04/listing-04-05/main.at" caption="Optional parameters">

```auto
fn greet(name int, greeting? int) {
    if greeting {
        print(greeting, name)
    } else {
        print(name)
    }
}

fn main() {
    greet(42)
    greet(42, 1)
}
```

```typescript
function greet(name: number, greeting: number | null): void {
    if (greeting) {
        console.log(greeting, name);
    } else {
        console.log(name);
    }
}

function main(): void {
    greet(42);
    greet(42, 1);
}

main();
```

</Listing>

Optional parameters in Auto transpile directly to TypeScript's optional
parameters (`param?: T`). Use an `if` check to determine whether the
parameter was provided.

## Special Return Types

TypeScript has several special types that relate to functions:

| TypeScript | Auto | Description |
|-----------|------|-------------|
| `void` | (implicit) | Function returns nothing |
| `unknown` | — | Safer alternative to `any` |
| `never` | — | Function never returns |
| `Function` | — | Untyped function (avoid) |

Auto does not have `unknown`, `never`, or `Function` as explicit types.
Functions that don't return a value implicitly have `void` return type in
the TypeScript output.

## TypeScript-Only Features

### Function Overloads

```typescript
// TypeScript only
function makeDate(timestamp: number): Date;
function makeDate(m: number, d: number, y: number): Date;
function makeDate(mOrTimestamp: number, d?: number, y?: number): Date {
    // implementation
}
```

Auto does not support function overloads. Use a single function with union
parameter types or an enum-based dispatch instead.

### Rest Parameters

```typescript
// TypeScript only
function sum(...nums: number[]): number {
    return nums.reduce((a, b) => a + b, 0);
}
```

### The `this` Parameter

```typescript
// TypeScript only
db.filterUsers(function (this: User) {
    console.log(this.name);
});
```

Auto uses `self` instead of `this`, and does not support explicit `this`
parameter declarations.

## Quick Reference

| TypeScript | Auto | Description |
|-----------|------|-------------|
| `(a: number) => number` | `(a int) => int` | Arrow function |
| `function f<T>(x: T): T` | `fn f<T>(x T) T` | Generic function |
| `function f(x?: number)` | `fn f(x? int)` | Optional parameter |
| `function f(...args: number[])` | — | Rest parameters |
| `f<number>(x)` | `f(x)` | Type argument inference |
