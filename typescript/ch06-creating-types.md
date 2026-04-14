# Creating Types from Types

Auto supports generics for both `type` and `spec` declarations, providing a
way to write code that works across multiple types. TypeScript extends generics
with several advanced type-level features that Auto does not replicate.

## Generic Types

Auto supports generic types with the `<T>` syntax. A generic type transpiles
to a TypeScript generic class.

```auto
type Box<T> {
    value T
}

fn main() {
    let intBox = Box(42)
    let strBox = Box("hello")
    print(intBox.value)
    print(strBox.value)
}
```

```typescript
class Box<T> {
    value: T;

    constructor(value: T) {
        this.value = value;
    }
}

function main(): void {
    const intBox = Box(42);
    const strBox = Box("hello");
    console.log(intBox.value);
    console.log(strBox.value);
}

main();
```

The `<T>` parameter is a placeholder for any type. When you create a `Box`,
the compiler infers the concrete type from the argument. You can also
explicitly specify it:

```auto
let intBox = Box<int>(42)
```

## Generic Specs

Specs can also be generic, transpiling to TypeScript generic interfaces:

```auto
spec Container<T> {
    fn get() T
    fn set(value T)
}

type Bag<T> as Container<T> {
    items Array<T>

    fn get() T {
        return self.items[0]
    }

    fn set(value T) {
        self.items[0] = value
    }
}
```

```typescript
interface Container<T> {
    get(): T;
    set(value: T): void;
}

class Bag<T> implements Container<T> {
    items: Array<T>;

    constructor(items: Array<T>) {
        this.items = items;
    }

    get(): T {
        return this.items[0];
    }

    set(value: T): void {
        this.items[0] = value;
    }
}
```

Generic specs allow you to define contracts that work with any type. Every
type parameter used in the spec body must appear in the spec declaration
(`<T>`).

## Multiple Type Parameters

Auto supports multiple type parameters separated by commas:

```auto
type Pair<T, U> {
    first T
    second U
}

fn main() {
    let p = Pair("age", 30)
    print(p.first, p.second)
}
```

```typescript
class Pair<T, U> {
    first: T;
    second: U;

    constructor(first: T, second: U) {
        this.first = first;
        this.second = second;
    }
}

function main(): void {
    const p = Pair("age", 30);
    console.log(p.first, p.second);
}

main();
```

There is no upper limit on the number of type parameters, but in practice
two or three is common. When the meaning is not obvious from context, use
descriptive names like `TKey` and `TValue` instead of single letters.

## TypeScript-Only: Conditional Types

Conditional types let you choose a type based on a condition:

```typescript
// TypeScript only
type IsString<T> = T extends string ? "yes" : "no";

type A = IsString<string>;   // "yes"
type B = IsString<number>;   // "no"
```

The syntax mirrors a ternary expression but operates at the type level. When
`T` extends `string`, the result type is `"yes"`; otherwise it is `"no"`.

### Distributive Conditional Types

When a conditional type is applied to a union type, it distributes across each
member of the union:

```typescript
// TypeScript only
type ToArray<T> = T extends any ? T[] : never;

type Result = ToArray<string | number>;
// Result is string[] | number[]
```

### `infer` Keyword

The `infer` keyword lets you extract a type from within another type:

```typescript
// TypeScript only
type ReturnType<T> = T extends (...args: any) => infer R ? R : any;

type Fn = (x: number) => string;
type R = ReturnType<Fn>;  // string
```

`infer R` declares a new type variable `R` that is inferred from the
matched position. This is particularly useful for extracting function return
types, element types from arrays, and more.

## TypeScript-Only: Mapped Types

Mapped types create new types by transforming every property in an existing
type:

```typescript
// TypeScript only
type Readonly<T> = {
    readonly [Property in keyof T]: T[Property];
};

type Optional<T> = {
    [Property in keyof T]?: T[Property];
};
```

The `[Property in keyof T]` syntax iterates over each key of `T`, producing
a new property in the result type.

### Modifiers

You can add or remove modifiers with `+` and `-`:

```typescript
// TypeScript only
type Modify<T> = {
    -readonly [Property in keyof T]: T[Property];  // remove readonly
    +optional [Property in keyof T]: T[Property];   // add optional
};
```

### Key Remapping

TypeScript 4.1+ supports remapping keys in mapped types using `as`:

```typescript
// TypeScript only
type Getters<T> = {
    [Property in keyof T as `get${Capitalize<string & Property>}`]: () => T[Property];
};

type Person = { name: string; age: number };
type PersonGetters = Getters<Person>;
// { getName: () => string; getAge: () => number }
```

The `as` clause transforms each key through a template literal type.

## TypeScript-Only: Template Literal Types

Template literal types allow string interpolation at the type level:

```typescript
// TypeScript only
type EventName = "click" | "focus" | "blur";
type Handler = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"
```

### Intrinsic String Types

TypeScript provides built-in string manipulation types:

```typescript
// TypeScript only
type Uppercase<T> = ...;
type Lowercase<T> = ...;
type Capitalize<T> = ...;
type Uncapitalize<T> = ...;

type Greeting = Capitalize<"hello">;  // "Hello"
type Shout = Uppercase<"quiet">;       // "QUIET"
```

These are especially powerful when combined with mapped types and conditional
types to transform string literal unions.

## TypeScript-Only: Utility Types

TypeScript ships with several built-in utility types built on top of the
advanced features above:

### `ReturnType<T>`

Extracts the return type of a function type.

```typescript
// TypeScript only
type R = ReturnType<() => string>;  // string
```

### `Parameters<T>`

Extracts the parameter types of a function type as a tuple.

```typescript
// TypeScript only
type P = Parameters<(x: number, y: string) => void>;
// [number, string]
```

### `Partial<T>`

Makes all properties of `T` optional.

```typescript
// TypeScript only
type User = { name: string; age: number };
type PartialUser = Partial<User>;
// { name?: string; age?: number }
```

### `Required<T>`

Makes all properties of `T` required.

```typescript
// TypeScript only
type Config = { host?: string; port?: number };
type FullConfig = Required<Config>;
// { host: string; port: number }
```

### `Readonly<T>`

Makes all properties of `T` readonly.

```typescript
// TypeScript only
type Frozen = Readonly<{ x: number; y: number }>;
// { readonly x: number; readonly y: number }
```

### `Pick<T, K>`

Selects a subset of properties from `T`.

```typescript
// TypeScript only
type User = { name: string; age: number; email: string };
type NameOnly = Pick<User, "name" | "age">;
// { name: string; age: number }
```

### `Omit<T, K>`

Removes a subset of properties from `T`.

```typescript
// TypeScript only
type User = { name: string; age: number; email: string };
type NoEmail = Omit<User, "email">;
// { name: string; age: number }
```

## Quick Reference

| TypeScript | Auto | Description |
|-----------|------|-------------|
| `class Box<T> { }` | `type Box<T> { }` | Generic type |
| `interface Spec<T> { }` | `spec Container<T> { }` | Generic spec |
| `T extends U ? X : Y` | -- | Conditional type (TS-only) |
| `infer R` | -- | Infer type (TS-only) |
| `[K in keyof T]: ...` | -- | Mapped type (TS-only) |
| `` `on${Capitalize<K>}` `` | -- | Template literal type (TS-only) |
| `ReturnType<T>` | -- | Utility type (TS-only) |
| `Partial<T>` | -- | Utility type (TS-only) |
| `Required<T>` | -- | Utility type (TS-only) |
| `Readonly<T>` | -- | Utility type (TS-only) |
| `Pick<T, K>` | -- | Utility type (TS-only) |
| `Omit<T, K>` | -- | Utility type (TS-only) |
| `Parameters<T>` | -- | Utility type (TS-only) |
