# Index Signatures & Type Operators

TypeScript provides **index signatures** and **type-level operators** (`keyof`,
`typeof`, mapped types) that let you work with dynamic property access and
transform types programmatically. Auto deliberately omits these features,
choosing `has` composition and explicit methods instead. This chapter explores
both approaches and explains when each is appropriate.

## Index Signatures in TypeScript

An **index signature** declares that an object can have arbitrary keys of a
given type, all mapping to the same value type. This is useful for dictionaries,
maps, and other dynamic data structures.

```typescript
// TypeScript — string index signature
interface StringMap {
    [key: string]: number;
}

const scores: StringMap = {};
scores["alice"] = 95;
scores["bob"] = 87;
// scores["charlie"] = "excellent"; // Error: value must be number
```

```typescript
// TypeScript — numeric index signature
interface StringArray {
    [index: number]: string;
}

const names: StringArray = ["Alice", "Bob"];
console.log(names[0]); // "Alice"
```

Index signatures only allow `string` or `number` as the key type. A numeric
index signature is mainly useful for describing array-like objects. For most
dictionary use cases, TypeScript developers also reach for the built-in
`Map<K, V>` class.

One subtlety: when both a string index signature and known properties exist, the
known properties must have values assignable to the index signature's value type:

```typescript
// TypeScript — mixing index signatures with known properties
interface Config {
    [key: string]: string | number;
    host: string;    // OK — string is assignable to string | number
    port: number;    // OK — number is assignable to string | number
    // debug: boolean; // Error — boolean is not assignable to string | number
}
```

## Auto's Approach: `has` Composition Instead of Index Signatures

Auto does **not** have index signatures. Arbitrary dynamic key access is
inherently unsafe — you lose compile-time knowledge of what keys exist and what
types they map to. Instead, Auto uses `has` composition to build types from
reusable components.

```auto
// Auto — composition with has
type Engine {
    horsepower int
    fn start() { print("Engine started") }
}

type Wheels {
    count int
    fn roll() { print("Rolling...") }
}

type Car has Engine, Wheels {
    brand str
}
```

`type Car has Engine, Wheels` gives `Car` all of `Engine`'s and `Wheels`'s
fields and methods. This is more explicit and type-safe than an index signature
because every field and method is known at compile time.

```auto
fn main() {
    let car = Car(horsepower: 300, count: 4, brand: "Tesla")
    car.start()   // method from Engine
    car.roll()    // method from Wheels
    print(car.brand)  // own field
}
```

Where TypeScript uses index signatures for dynamic data, Auto provides dedicated
collection types from the standard library — such as `Map<K, V>` — with explicit
methods for access:

```auto
// Auto — explicit map type
let scores = Map<str, int>()
scores.set("alice", 95)
scores.set("bob", 87)

let alice_score = scores.get("alice")  // ?int (optional)

match alice_score {
    Some(v) => print("Alice scored {v}")
    None => print("Alice not found")
}
```

<Listing name="has-composition" file="listings/ch11-has-composition">

```auto
// Auto — has composition vs index signatures
type Named {
    name str
    fn greet() { print("Hi, I'm {self.name}") }
}

type Aged {
    age int
}

type Logged {
    fn log(msg str) { print("[LOG] {msg}") }
}

type User has Named, Aged, Logged {
    email str
}

type Admin has Named, Logged {
    level int
}

fn introduce(u User) {
    u.greet()
    print("Age: {u.age}")
}

fn main() {
    let user = User("Alice", 30, "alice@example.com")
    user.greet()
    user.log("User created")
    print("Email: {user.email}")

    let admin = Admin("Bob", 1)
    admin.greet()
    admin.log("Admin logged in")
    print("Admin level: {admin.level}")

    // Structural typing — Admin satisfies the parts User needs
    // But introduce() requires `age`, which Admin doesn't have
}
```

</Listing>

## The `keyof` Operator (TypeScript Only)

TypeScript's `keyof` operator produces a union of all property **names** of a
type. It is the foundation for mapped types and many utility types:

```typescript
// TypeScript — keyof extracts property names
type Person = { name: string; age: number };
type PersonKeys = keyof Person;  // "name" | "age"

// Used for safe property access
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const p: Person = { name: "Ada", age: 30 };
getProperty(p, "name");  // string
// getProperty(p, "email"); // Error: "email" is not a key of Person
```

`keyof` is especially powerful when combined with mapped types to transform
every property of a type. Auto does **not** have `keyof` — Auto enums and `is`
pattern matching serve similar purposes for type-safe property handling.

## The `typeof` Operator

TypeScript's `typeof` captures the **type of a value** at the type level. This
is useful for synchronizing type declarations with runtime values:

```typescript
// TypeScript — typeof captures a value's type
const config = {
    host: "localhost",
    port: 8080,
    debug: true
};

type Config = typeof config;
// { host: string; port: number; debug: boolean }

function loadConfig(c: Config): void { /* ... */ }
loadConfig(config); // OK — config matches its own type
```

Auto handles this through **type inference**. When you declare a value, the
compiler infers its type automatically. Explicit `typeof` is unnecessary because
the inferred type is always available:

```auto
// Auto — type inference replaces typeof
let config = {
    host = "localhost"
    port = 8080
    debug = true
}
// config is inferred as { host: str; port: int; debug: bool }

fn load_config(c typeof config) { ... }
load_config(config)
```

## Mapped Types (TypeScript Only)

**Mapped types** transform every property of an existing type to produce a new
type. They use `keyof` and `in` to iterate over property names:

```typescript
// TypeScript — mapped types
type Readonly<T> = { readonly [K in keyof T]: T[K] };

type Partial<T> = { [K in keyof T]?: T[K] };

type Pick<T, K extends keyof T> = { [P in K]: T[P] };

type Record<K extends string, V> = { [P in K]: V };
```

These are the foundation of TypeScript's built-in utility types. A `Partial<T>`
makes every property optional; `Readonly<T>` makes every property immutable;
`Record<K, V>` creates a type from a key set.

```typescript
// TypeScript — using mapped types
interface Todo {
    title: string;
    description: string;
    done: boolean;
}

type PartialTodo = Partial<Todo>;
// { title?: string; description?: string; done?: boolean }

type TodoKeys = keyof Todo;  // "title" | "description" | "done"
type TodoPreview = Pick<Todo, "title" | "done">;
// { title: string; done: boolean }
```

Auto does **not** have mapped types. Type-level computation is intentionally
omitted to keep the type system simple and fast to compile. Auto achieves
similar goals through generics, specs, and `has` composition — without the
complexity of type-level loops and conditionals.

## Practical Comparison — Building a Dictionary

Here is how you might build a map-like structure in both languages:

```typescript
// TypeScript — index signature approach
interface Dictionary<T> {
    [key: string]: T;
}

const dict: Dictionary<number> = {};
dict["x"] = 42;
console.log(dict["x"]);  // 42
console.log(dict["missing"]);  // undefined — no compile-time warning
```

```typescript
// TypeScript — Map approach (safer)
const map = new Map<string, number>();
map.set("x", 42);
map.get("x");       // 42
map.get("missing"); // undefined
map.has("x");       // true
```

```auto
// Auto — standard library Map
let map = Map<str, int>()
map.set("x", 42)

let value = map.get("x")       // ?int (Some(42))
let missing = map.get("nope")  // ?int (None)
let exists = map.has("x")      // bool (true)
```

Auto's `Map` returns `?T` (optional) from `get`, forcing you to handle the
missing-key case explicitly. TypeScript's index signature silently returns
`undefined`, which is a common source of runtime errors.

## Quick Reference

| Concept | TypeScript | Auto |
|---------|-----------|------|
| String index signature | `{ [key: string]: T }` | *(not supported)* |
| Numeric index signature | `{ [index: number]: T }` | *(not supported)* |
| Dictionary | Index signature or `Map<K, V>` | `Map<K, V>` with `?T` returns |
| Property name union | `keyof T` | *(not supported)* |
| Value type capture | `typeof x` | Type inference |
| Mapped type | `{ [K in keyof T]: T[K] }` | *(not supported)* |
| Utility types | `Partial<T>`, `Pick<T, K>` | *(not supported)* |
| Composition | Intersection types `&` | `has` keyword |
