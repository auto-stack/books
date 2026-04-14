# Narrowing

TypeScript uses *narrowing* to refine a value's type within conditional
branches. Auto uses `is` expressions for pattern matching, which provides
a more structured approach to the same problem.

## Pattern Matching with `is`

Auto's `is` expression inspects a value and matches it against patterns.
When a pattern matches, the corresponding branch executes. This is Auto's
primary mechanism for narrowing — it replaces TypeScript's `typeof` checks,
`instanceof` checks, and discriminated union switches with a single
consistent syntax.

<Listing number="03-01" file="listings/ch03/listing-03-01/main.at" caption="Pattern matching with is">

```auto
enum Value {
    Num int
    Text int
}

fn describe(value Value) {
    is value {
        Value.Num(n) => print("It's a number:", n)
        Value.Text(t) => print("It's text:", t)
    }
}

fn main() {
    describe(Value.Num(42))
    describe(Value.Text(99))
}
```

```typescript
type Value =
    { _tag: "Num", value: number }
    | { _tag: "Text", value: number };

const Value = {
    Num: (value: number) => ({ _tag: "Num", value }),
    Text: (value: number) => ({ _tag: "Text", value })
};


function describe(value: Value): void {
    switch (value) {
        case Value.Num(n):
            console.log("It's a number:", n);
            break;
        case Value.Text(t):
            console.log("It's text:", t);
            break;
    }
}

function main(): void {
    describe(Value.Num(42));
    describe(Value.Text(99));
}

main();
```

</Listing>

The `is` expression transpiles to a TypeScript `switch` statement. Each
pattern binds variables (like `n` and `t`) that are available within the
branch body. In TypeScript, the equivalent would use a `switch` on the
`_tag` field of a discriminated union.

## Truthiness Narrowing

Auto treats `0`, empty strings, `null`, and `false` as falsy — the same
as TypeScript. You can use any value directly in an `if` condition:

<Listing number="03-02" file="listings/ch03/listing-03-02/main.at" caption="Truthiness narrowing">

```auto
fn process_count(count int) {
    if count {
        print("Count is non-zero:", count)
    } else {
        print("Count is zero")
    }
}

fn main() {
    process_count(5)
    process_count(0)
}
```

```typescript
function process_count(count: number): void {
    if (count) {
        console.log("Count is non-zero:", count);
    } else {
        console.log("Count is zero");
    }
}

function main(): void {
    process_count(5);
    process_count(0);
}

main();
```

</Listing>

This works identically in both Auto and TypeScript. The `if count`
condition narrows the type implicitly — inside the `if` branch, the
compiler knows `count` is truthy.

## Discriminated Unions

TypeScript's discriminated unions use a common property (like `kind`) to
narrow types. Auto uses enums with tagged variants, which transpile to
discriminated unions automatically:

<Listing number="03-03" file="listings/ch03/listing-03-03/main.at" caption="Discriminated unions with enum">

```auto
enum Shape {
    Circle float
    Square float
}

fn area(shape Shape) {
    is shape {
        Shape.Circle(r) => print("Circle area:", 3.14 * r * r)
        Shape.Rectangle(w) => print("Rectangle area:", w * w)
    }
}

fn main() {
    let c = Shape.Circle(5.0)
    let s = Shape.Square(4.0)
    area(c)
    area(s)
}
```

```typescript
type Shape =
    { _tag: "Circle", value: number }
    | { _tag: "Square", value: number };

const Shape = {
    Circle: (value: number) => ({ _tag: "Circle", value }),
    Square: (value: number) => ({ _tag: "Square", value })
};


function area(shape: Shape): void {
    switch (shape) {
        case Shape.Circle(r):
            console.log("Circle area:", 3.14 * r * r);
            break;
        case Shape.Rectangle(w):
            console.log("Rectangle area:", w * w);
            break;
    }
}

function main(): void {
    const c = Shape.Circle(5);
    const s = Shape.Square(4);
    area(c);
    area(s);
}

main();
```

</Listing>

Each enum variant becomes a `{ _tag: "...", value: T }` object. The `is`
expression transpiles to a `switch` on the `_tag` field, which is exactly
how TypeScript handles discriminated unions.

## Exhaustiveness

Auto's `is` expression requires you to handle every variant. If you add a
new variant to an enum but forget to handle it in an `is` expression, the
compiler will warn you. TypeScript achieves the same effect with
`never` type checking in `switch` default cases.

## TypeScript-Only Narrowing Features

The following TypeScript narrowing features do not have direct equivalents
in Auto, because Auto uses `is` pattern matching as its unified narrowing
mechanism.

### `typeof` Guards

```typescript
// TypeScript only
function format(value: string | number) {
    if (typeof value === "string") {
        return value.toUpperCase();
    }
    return value.toFixed(2);
}
```

In Auto, use `is` pattern matching with enum variants instead.

### `instanceof` Narrowing

```typescript
// TypeScript only
function formatDate(date: Date | string) {
    if (date instanceof Date) {
        return date.toISOString();
    }
    return date;
}
```

Auto does not have classes with runtime type information in the same way.
Use enum-based tagging instead.

### Type Predicates

```typescript
// TypeScript only
function isFish(pet: Fish | Bird): pet is Fish {
    return (pet as Fish).swim !== undefined;
}
```

Auto's `is` expression handles this implicitly — each branch already has
the narrowed type.

## Quick Reference

| TypeScript | Auto | Description |
|-----------|------|-------------|
| `typeof x === "string"` | `x is str => ...` | Type check |
| `x instanceof Date` | Enum tagging | Runtime type check |
| `switch (x.kind)` | `x is { ... }` | Discriminated union |
| `if (value)` | `if value` | Truthiness |
| `x is Type` (predicate) | `is` branch binding | Type predicate |
