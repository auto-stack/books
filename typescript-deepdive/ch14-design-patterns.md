# Design Patterns

This chapter covers common design patterns in TypeScript and how they translate
to Auto. Most patterns carry over directly, but Auto's type system and module
model simplify several of them.

## Singleton

The **singleton** pattern ensures a class has only one instance. In TypeScript,
the classic approach uses a `private` constructor with a `static getInstance()`
method:

```typescript
// TypeScript — singleton class
class Database {
    private static instance: Database;
    private constructor() {}

    static getInstance(): Database {
        if (!Database.instance) {
            Database.instance = new Database();
        }
        return Database.instance;
    }
}
```

In practice, TypeScript developers prefer the simpler **module-level export**
approach — a module is only evaluated once, so its top-level exports are
naturally singleton:

```typescript
// TypeScript — module singleton (preferred)
export const db = new Database();
```

Auto takes this further. In Auto, a **module's top-level state is naturally
singleton** — shared across the entire program. No private constructors or
`getInstance()` boilerplate needed:

```auto
// Auto — module singleton (the only approach)
var db = Database()
```

No ceremony. The module system guarantees a single instance.

## Currying

**Currying** transforms `f(a, b) => c` into `f(a) => f(b) => c`, enabling
**partial application** and clean function composition:

```typescript
// TypeScript
const add = (x: number) => (y: number) => x + y;
const add5 = add(5);
add5(3);   // 8
add5(10);  // 15
```

Auto's syntax is nearly identical — space-separated type annotations instead
of colons:

```auto
// Auto
let add = (x int) => (y int) => x + y
let add5 = add(5)
add5(3)   // 8
add5(10)  // 15
```

Currying shines when building reusable utilities. A curried logger can
pre-bind the log level:

```typescript
const log = (level: string) => (msg: string) =>
    console.log(`[${level}] ${msg}`);
const warn = log("WARN");
warn("disk space low");
```

```auto
let log = (level str) => (msg str) =>
    print("[{level}] {msg}")
let warn = log("WARN")
warn("disk space low")
```

## Builder Pattern

The **builder** pattern constructs complex objects step by step. Both languages
support chainable methods returning `this` or `self`:

```typescript
// TypeScript
class QueryBuilder {
    private table = "";
    private conditions: string[] = [];

    from(table: string): this { this.table = table; return this; }
    where(c: string): this { this.conditions.push(c); return this; }
    build(): string {
        const w = this.conditions.length > 0
            ? " WHERE " + this.conditions.join(" AND ") : "";
        return "SELECT * FROM " + this.table + w;
    }
}
const q = new QueryBuilder().from("users").where("age > 18").build();
```

```auto
// Auto
type QueryBuilder {
    var table str
    var conditions []str

    fn from(table str) QueryBuilder { self.table = table; self }
    fn where(c str) QueryBuilder { self.conditions.push(c); self }
    fn build() str {
        let w = if self.conditions.len() > 0 {
            " WHERE " + self.conditions.join(" AND ")
        } else { "" }
        "SELECT * FROM " + self.table + w
    }
}
fn main() {
    let q = QueryBuilder().from("users").where("age > 18").build()
    print(q)
}
```

The pattern is identical in both languages. Auto's explicit `self` return type
is clearer than TypeScript's polymorphic `this`.

## Type-Safe Event Emitter

A **typed event emitter** provides subscribe/emit with full type safety. Each
emitter is parameterized by event data type `T`, so listeners receive correctly
typed arguments.

<Listing name="event-emitter" file="listings/ch14-event-emitter">

```auto
// Auto — type-safe event emitter
type Emitter<T> {
    var listeners []fn(T)

    fn on(listener fn(T)) {
        self.listeners.push(listener)
    }

    fn emit(event T) {
        for listener in self.listeners {
            listener(event)
        }
    }

    fn off(listener fn(T)) bool {
        let idx = self.listeners.index_of(listener)
        if idx >= 0 {
            self.listeners.remove_at(idx)
            true
        } else {
            false
        }
    }
}

// Currying example
let add = (x int) => (y int) => x + y

fn main() {
    // Event emitter
    var clicks = Emitter([]fn(int))
    clicks.on((n int) => print("Click #{n}"))
    clicks.on((n int) => print("  count = {n}"))
    clicks.emit(1)
    clicks.emit(2)

    // Currying
    let add5 = add(5)
    print("add(5)(3) = {add5(3)}")
    print("add(5)(10) = {add5(10)}")

    // String events
    var messages = Emitter([]fn(str))
    messages.on((msg str) => print("Message: {msg}"))
    messages.emit("Hello, Auto!")
}
```

```typescript
// TypeScript — type-safe event emitter
class Emitter<T> {
    private listeners: ((event: T) => void)[] = [];

    on(listener: (event: T) => void): void {
        this.listeners.push(listener);
    }

    emit(event: T): void {
        for (const listener of this.listeners) {
            listener(event);
        }
    }

    off(listener: (event: T) => void): boolean {
        const idx = this.listeners.indexOf(listener);
        if (idx >= 0) {
            this.listeners.splice(idx, 1);
            return true;
        }
        return false;
    }
}

// Currying example
const add = (x: number) => (y: number) => x + y;

// Event emitter
const clicks = new Emitter<number>();
clicks.on((n) => console.log("Click #" + n));
clicks.on((n) => console.log("  count = " + n));
clicks.emit(1);
clicks.emit(2);

// Currying
const add5 = add(5);
console.log("add(5)(3) = " + add5(3));
console.log("add(5)(10) = " + add5(10));

// String events
const messages = new Emitter<string>();
messages.on((msg) => console.log("Message: " + msg));
messages.emit("Hello, TypeScript!");
```

</Listing>

The `Emitter<T>` generic ensures a `Emitter<number>` only accepts and emits
numbers. Both languages implement this identically — Auto just drops semicolons
and uses space-separated annotations.

## Observer Pattern

The **observer** pattern is closely related to the event emitter — subscribers
listen for state changes on an observed object. The implementation is nearly
identical to the `Emitter<T>` above, with `subscribe()`/`set()` replacing
`on()`/`emit()`. Auto's `is` pattern matching can additionally route different
event types within a single handler. In most cases, the event emitter is
preferred because it decouples the event source from the triggering state.

## Factory Pattern

The **factory** pattern creates objects without exposing creation logic. Auto
uses `type` instead of `class`, and returns `Result<T>` instead of throwing:

```typescript
// TypeScript — factory (throws on error)
interface Shape { area(): number; }
class Circle implements Shape {
    constructor(private r: number) {}
    area(): number { return Math.PI * this.r * this.r; }
}
function createShape(t: string): Shape {
    if (t === "circle") return new Circle(5);
    throw new Error("Unknown: " + t);
}
```

```auto
// Auto — factory (returns Result)
spec Shape { fn area() f64 }
type Circle is Shape {
    radius f64
    fn area() f64 { 3.14159 * self.radius * self.radius }
}
fn createShape(t str) Result<Shape> {
    t is
        "circle" => ok(Circle(5.0))
        _        => err("Unknown: " + t)
}
```

Using `Result<T>` instead of exceptions makes the error path explicit and forces
callers to handle failures at compile time.

## Quick Reference

| Concept | TypeScript | Auto |
|---------|-----------|------|
| Singleton | `private constructor` + `static getInstance()` | Module top-level state |
| Currying | `(x: number) => (y: number) => ...` | `(x int) => (y int) => ...` |
| Builder | Chainable methods returning `this` | Chainable methods returning `self` |
| Event emitter | `class Emitter<T>` | `type Emitter<T>` |
| Observer | `subscribe()` returning unsubscribe fn | `subscribe()` with `is` matching |
| Factory | `function` returning `Shape` (throws) | `fn` returning `Result<Shape>` |
| Error handling | `throw new Error(...)` | `Result<T>` with `err(...)` |
