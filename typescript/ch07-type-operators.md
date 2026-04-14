# Type Operators

TypeScript provides several operators that let you query and compose types at
the type level. Auto shares basic property access but does not implement the
advanced type-level operators.

## Property Access

Both Auto and TypeScript use dot notation for property access:

```auto
type Point {
    x int
    y int
}

fn main() {
    let p = Point(3, 4)
    print(p.x)
    print(p.y)
}
```

```typescript
class Point {
    x: number;
    y: number;

    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
    }
}

function main(): void {
    const p = Point(3, 4);
    console.log(p.x);
    console.log(p.y);
}

main();
```

This is the only type operator that Auto supports. Everything else in this
chapter is TypeScript-only.

## TypeScript-Only: `keyof`

The `keyof` operator creates a union type of all known public property names
of a given type:

```typescript
// TypeScript only
type Person = { name: string; age: number; city: string };
type Keys = keyof Person;
// "name" | "age" | "city"
```

This is useful for writing generic functions that accept a property name as
an argument:

```typescript
// TypeScript only
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const person = { name: "Alice", age: 30 };
const name = getProperty(person, "name");  // string
const age = getProperty(person, "age");    // number
```

Combining `keyof` with generic constraints ensures type safety when
accessing dynamic properties.

### `keyof` with Indexed Types

`keyof` works with arrays and maps too:

```typescript
// TypeScript only
type ArrayKeys = keyof string[];    // "length" | "toString" | ...
type MapKeys = keyof Map<string, number>;  // Map method names
```

Note that `keyof` on an array does not produce numeric indices — it produces
the names of `Array` methods and properties.

## TypeScript-Only: `typeof` Type Operator

The `typeof` operator captures the type of a value at the type level. This
is distinct from JavaScript's runtime `typeof`:

```typescript
// TypeScript only
const colors = {
    red: "#ff0000",
    green: "#00ff00",
    blue: "#0000ff",
};

type Colors = typeof colors;
// { red: string; green: string; blue: string }

type ColorValue = typeof colors["red"];
// string
```

### With `const` Assertion

`typeof` is often paired with `as const` to get precise literal types:

```typescript
// TypeScript only
const directions = ["north", "south", "east", "west"] as const;
type Direction = typeof directions[number];
// "north" | "south" | "east" | "west"
```

Without `as const`, `typeof directions` would be `string[]`, losing the
literal information.

### Capturing Function Types

`typeof` also works on functions and classes:

```typescript
// TypeScript only
function createPair(x: number, y: string): [number, string] {
    return [x, y];
}

type FnType = typeof createPair;
// (x: number, y: string) => [number, string]
```

## TypeScript-Only: Indexed Access Types

Indexed access types let you look up a specific property of a type using
bracket notation:

```typescript
// TypeScript only
type Person = { name: string; age: number; address: { city: string } };

type Name = Person["name"];            // string
type City = Person["address"]["city"]; // string
```

### With Union Keys

When the index is a union of keys, the result is a union of the corresponding
property types:

```typescript
// TypeScript only
type Person = { name: string; age: number };
type NameOrAge = Person["name" | "age"];
// string | number
```

### With `keyof`

Combining indexed access with `keyof` produces a union of all property types:

```typescript
// TypeScript only
type Person = { name: string; age: number; active: boolean };
type Values = Person[keyof Person];
// string | number | boolean
```

### With `number` for Arrays

Using `number` as an index on an array type yields the element type:

```typescript
// TypeScript only
type StringArray = string[];
type Element = StringArray[number];
// string
```

## Quick Reference

| TypeScript | Auto | Description |
|-----------|------|-------------|
| `obj.field` | `obj.field` or `self.field` | Property access |
| `keyof T` | -- | Union of property keys (TS-only) |
| `typeof value` | -- | Type of a value (TS-only) |
| `Type["key"]` | -- | Indexed access type (TS-only) |
| `T[keyof T]` | -- | Union of property types (TS-only) |
| `Array[number]` | -- | Array element type (TS-only) |
| `as const` | -- | Literal type assertion (TS-only) |
