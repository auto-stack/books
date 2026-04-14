# Language Basics

This chapter covers fundamental language concepts, contrasting JavaScript's
design choices with how Auto handles the same problems. Understanding these
differences is key to writing idiomatic Auto code.

## Equality: No Implicit Coercion

JavaScript has two equality operators: `==` (with type coercion) and `===`
(strict). The coercive `==` produces surprising results:

```typescript
// TypeScript / JavaScript
"" == "0";     // false
0 == "";       // true (!)
null == undefined; // true
```

Auto has **no implicit coercion**. Equality always compares values of the
same type:

```auto
// Auto
1 == 1         // true
1 == 2         // false
"a" == "a"     // true
// No implicit coercion between types
```

## References vs Values

In JavaScript, objects are reference types — assigning an object does not
copy it, and mutations through one variable are visible through all aliases:

```typescript
// TypeScript / JavaScript
const foo = { x: 1 };
const bar = foo;
foo.x = 2;
console.log(bar.x);  // 2 — same reference
```

Auto distinguishes value and reference semantics more explicitly. Primitive
types (`int`, `float`, `str`, `bool`) are value types — they are copied on
assignment. Complex types (`type` instances, lists) have reference semantics
by default, but you can use explicit copying where needed.

## Null and Undefined

JavaScript has two "empty" values: `undefined` (uninitialized) and `null`
(intentionally empty). This causes confusion:

```typescript
// TypeScript
let x;              // undefined
let y = null;        // null
typeof undefined;    // "undefined"
typeof null;         // "object" (!)
```

Auto uses a single `nil` value for "no value":

```auto
// Auto
var x int           // default value depends on type
let y = nil         // explicitly no value
```

For optional values, Auto uses the `?T` nullable type (like Rust's `Option<T>`),
which is checked with pattern matching:

```auto
fn process(name ?str) {
    name is
        Some(n) => print("Got:", n)
        None => print("No name provided")
}
```

## `this` Binding

In JavaScript, `this` is determined by *how* a function is called, not where
it is defined. This is one of the most confusing aspects of JavaScript:

```typescript
// TypeScript / JavaScript
const obj = {
    name: "Alice",
    greet() { console.log(this.name); }
};
obj.greet();    // "Alice" — this = obj
const fn = obj.greet;
fn();           // undefined — this = global/undefined
```

Auto uses **explicit `self`** in method bodies. There is no dynamic `this`
binding — `self` always refers to the current instance:

<Listing name="self-in-methods" file="listings/ch01-self-in-methods">

```auto
type User {
    name str
    fn greet() {
        print("Hello from " + self.name)
    }
}

fn main() {
    let user = User("Alice")
    user.greet()
}
```

</Listing>

## Closures

Closures are functions that capture variables from their enclosing scope.
Both JavaScript and Auto support closures, but Auto's type system provides
stronger guarantees:

<Listing name="closure-counter" file="listings/ch01-closure-counter">

```auto
fn apply(f fn(int) int, x int) int {
    f(x)
}

fn double(x int) int {
    x * 2
}

fn main() {
    let result = apply(double, 5)
    print(result)
}
```

</Listing>

## Numbers

JavaScript has only one numeric type (`number`), a 64-bit float. This causes
IEEE 754 precision issues:

```typescript
// TypeScript / JavaScript
0.1 + 0.2;  // 0.30000000000000004
```

Auto has **distinct integer and floating-point types**:

```auto
// Auto
let x int = 42          // integer
let y f64 = 3.14        // floating point
let z = 0.1 + 0.2       // f64, also has IEEE 754 behavior
```

## Truthiness: Explicit Conditions

JavaScript implicitly coerces values to booleans in conditions. Falsy values
are `false`, `0`, `NaN`, `""`, `null`, `undefined` — everything else is truthy:

```typescript
// TypeScript / JavaScript
if ("hello") { }   // truthy
if (0) { }         // falsy
if ({}) { }        // truthy (even empty object!)
```

Auto requires **explicit boolean conditions**:

```auto
// Auto
let name = "Alice"
if name != nil {       // explicit nil check
    print("Has name")
}

if count > 0 {          // explicit boolean expression
    print("Positive")
}
```

## Quick Reference

| JavaScript Quirk | Auto's Approach |
|------------------|-----------------|
| `==` type coercion | No implicit coercion |
| Two null values (`null`, `undefined`) | Single `nil` + `?T` nullable type |
| Dynamic `this` binding | Explicit `self` in methods |
| Single `number` type | Separate `int`, `float`, `double` |
| Implicit truthiness | Explicit boolean conditions |
| `var` is function-scoped | `let` (immutable) / `var` (mutable) block-scoped |
| No deep immutability | `let` defaults to immutable |
