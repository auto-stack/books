# Functions

Functions are the fundamental building blocks of any program. Both TypeScript and Auto provide first-class functions, closures, and higher-order function support — but with different syntax and a few key semantic differences.

## Function Declarations

A *function declaration* defines a named function with typed parameters and a return type. The syntax is similar, but Auto is more concise.

```typescript
function add(a: number, b: number): number {
    return a + b;
}
```

```auto
fn add(a int, b int) int {
    a + b
}
```

Auto uses the `fn` keyword instead of `function`. Two key differences: **Auto does not require `return`** for the last expression in a function body — the final expression is returned implicitly. The `return` keyword is still available when you need an *early exit* from a function.

Return type annotations appear after the parameter list in both languages: `): number` in TypeScript versus `) int` in Auto.

## Closures (Arrow Functions)

*Closures* (arrow functions) provide a lightweight syntax for anonymous functions. They are essential for callbacks, higher-order functions, and functional programming patterns.

```typescript
const add = (a: number, b: number): number => a + b;
const greet = (name: string): void => {
    console.log("Hello, " + name);
};
```

```auto
let add = (a int, b int) => a + b
let greet = (name str) => print("Hello, " + name)
```

The arrow syntax is nearly identical between the two languages. Auto uses space-separated type annotations (`a int`) rather than TypeScript's colon-separated annotations (`a: number`).

One important distinction: TypeScript closures are often used to work around `this` binding issues. **Auto does not have this problem** — it uses an explicit `self` parameter for methods, so closures are used purely for their expressiveness.

## Function Types

Both languages treat functions as *first-class values* — you can store them in variables, pass them as arguments, and return them from other functions.

```typescript
let transform: (x: number) => number = (x) => x * 2;
let predicate: (x: number) => boolean = (x) => x > 0;
```

```auto
let transform fn(int) int = (x int) => x * 2
let predicate fn(int) bool = (x int) => x > 0
```

TypeScript uses `(x: number) => number` for callable type annotations. Auto uses the more compact `fn(int) int` syntax. Multi-parameter function types follow the same pattern:

```typescript
let combine: (a: number, b: string) => boolean;
```

```auto
let combine fn(int, str) bool
```

Higher-order functions — functions that accept or return other functions — work naturally with these types:

```auto
fn apply(f fn(int) int, x int) int {
    f(x)
}
```

```typescript
function apply(f: (x: number) => number, x: number): number {
    return f(x);
}
```

## Optional and Default Parameters

Functions can accept parameters that the caller may omit. TypeScript uses a `?` suffix for optional parameters; Auto uses a `?` prefix on the type.

```typescript
function greet(name: string, greeting?: string): void {
    if (greeting !== undefined) {
        console.log(greeting + ", " + name + "!");
    } else {
        console.log("Hello, " + name + "!");
    }
}
```

```auto
fn greet(name str, greeting ?str) {
    if greeting != nil {
        print("{greeting}, {name}!")
    } else {
        print("Hello, {name}!")
    }
}
```

Optional parameters **must come after** all required parameters in both languages. In TypeScript, an optional parameter has type `T | undefined`. In Auto, it has type `?T` and defaults to `nil`.

You can also provide *default values*:

```typescript
function greet(name: string, greeting: string = "Hello"): void {
    console.log(greeting + ", " + name + "!");
}
```

```auto
fn greet(name str, greeting str = "Hello") {
    print("{greeting}, {name}!")
}
```

Default parameters remove the need for manual `undefined` / `nil` checks — the compiler inserts them automatically.

## Function Overloading

TypeScript supports **function overloading**, which allows multiple signatures for the same function name:

```typescript
function parse(value: string): number;
function parse(value: number): string;
function parse(value: string | number): string | number {
    if (typeof value === "string") {
        return parseInt(value, 10);
    }
    return value.toString();
}
```

> **TypeScript Only.** Auto does *not* support function overloading. Instead, use **union types** or **enums** to handle different input shapes in a single function body:

```auto
fn parse(value int | str) int | str {
    value is
        int => value
        str => int.from_str(value)
}
```

This approach is simpler and avoids the boilerplate of writing multiple signatures followed by a single implementation.

## Methods and `self`

In TypeScript, methods use `this` to refer to the current object. The value of `this` depends on *how the function is called*, which is a common source of bugs:

```typescript
class Counter {
    count = 0;
    increment() {
        this.count++;
    }
}
const c = new Counter();
c.increment();       // this === c  — correct
const fn = c.increment;
fn();                // this === undefined  — bug in strict mode
```

Auto uses an **explicit `self` parameter** instead of implicit `this`. There is no dynamic binding — `self` always refers to the current instance, regardless of how the method is referenced:

```auto
type Counter {
    count int
    fn inc() {
        self.count = self.count + 1
    }
}
```

Method calls use the same `obj.method()` syntax in both languages. But in Auto, extracting a method into a variable preserves its receiver — no binding surprises.

## Closures and Captured Variables

Both TypeScript and Auto support *closures*: functions that capture variables from their enclosing scope. Captured variables are shared by reference, meaning mutations are visible across calls.

```auto
fn make_counter() fn() int {
    var count int = 0
    fn() int {
        count = count + 1
        count
    }
}
```

```typescript
function makeCounter(): () => number {
    let count = 0;
    return function (): number {
        count = count + 1;
        return count;
    };
}
```

Each call to `make_counter()` (or `makeCounter()`) creates a **new lexical scope** with its own `count` variable. The returned closure retains access to that variable across invocations — this is the *closure counter* or *factory* pattern.

This pattern is widely used for encapsulation, iterators, and stateful callbacks in both languages.

## Quick Reference

| Concept | TypeScript | Auto |
|---|---|---|
| Function declaration | `function add(a: number, b: number): number` | `fn add(a int, b int) int` |
| Implicit return | Not supported | Last expression returned implicitly |
| Arrow function | `const f = (x: number) => x * 2` | `let f = (x int) => x * 2` |
| Function type | `(x: number) => number` | `fn(int) int` |
| Optional parameter | `function f(x?: string)` | `fn f(x ?str)` |
| Default parameter | `function f(x: string = "hi")` | `fn f(x str = "hi")` |
| Function overloading | Multiple signatures supported | Not supported; use unions |
| Method receiver | `this` (dynamic binding) | `self` (explicit parameter) |
| Closure capture | By reference | By reference |
