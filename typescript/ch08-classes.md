# Classes

Auto's `type` with methods is equivalent to TypeScript classes. Auto uses
`self` instead of `this`, supports spec implementation via `as`, and
provides composition via `has`. This chapter covers Auto's approach and the
additional TypeScript-only class features.

## Type with Methods

In Auto, methods are defined directly inside the `type` block. Fields are
declared as name-type pairs, and methods use `self` to refer to the current
instance:

```auto
type Counter {
    count int

    fn new() Counter {
        return Counter(0)
    }

    fn increment() {
        self.count = self.count + 1
    }

    fn get() int {
        return self.count
    }
}

fn main() {
    let c = Counter.new()
    c.increment()
    c.increment()
    print(c.get())
}
```

```typescript
class Counter {
    count: number;

    constructor(count: number) {
        this.count = count;
    }

    increment(): void {
        this.count = this.count + 1;
    }

    get(): number {
        return this.count;
    }
}

function main(): void {
    const c = Counter.new();
    c.increment();
    c.increment();
    console.log(c.get());
}

main();
```

`self` transpiles to `this` in TypeScript. The `new` method serves as a
factory constructor, returning a new instance of `Counter`.

## Implementing Specs

A type can implement one or more specs using the `as` keyword:

```auto
spec Printable {
    fn toString() string
}

type User as Printable {
    name string

    fn toString() string {
        return "User(" + self.name + ")"
    }
}

fn main() {
    let u = User("Alice")
    print(u.toString())
}
```

```typescript
interface Printable {
    toString(): string;
}

class User implements Printable {
    name: string;

    constructor(name: string) {
        this.name = name;
    }

    toString(): string {
        return "User(" + this.name + ")";
    }
}

function main(): void {
    const u = User("Alice");
    console.log(u.toString());
}

main();
```

A type can implement multiple specs by separating them with commas:
`type X as SpecA, SpecB { }`.

## Composition with `has`

Auto uses `has` to compose types by embedding methods from one type into
another. This is a structural alternative to inheritance:

```auto
type Logger {
    fn log(msg string) {
        print("[LOG]", msg)
    }
}

type Service has Logger {
    name string

    fn start() {
        self.log("Service started:" + self.name)
    }
}

fn main() {
    let svc = Service("api")
    svc.start()
    svc.log("custom message")
}
```

```typescript
class Logger {
    log(msg: string): void {
        console.log("[LOG]", msg);
    }
}

class Service {
    name: string;

    constructor(name: string) {
        this.name = name;
    }

    log(msg: string): void {
        console.log("[LOG]", msg);
    }

    start(): void {
        this.log("Service started:" + this.name);
    }
}

function main(): void {
    const svc = Service("api");
    svc.start();
    svc.log("custom message");
}

main();
```

The `has Logger` declaration inlines all of `Logger`'s methods into
`Service`. Unlike inheritance, composition does not create a subclass
relationship — `Service` is not a `Logger`, it simply has `Logger`'s
methods.

## Enum-Based State

Auto encourages using enums with pattern matching to model state machines
instead of class hierarchies:

```auto
enum State {
    Idle,
    Running,
    Done
}

type Task {
    state State
    name string

    fn new(name string) Task {
        return Task(Idle, name)
    }

    fn advance() {
        self.state = is self.state {
            Idle => Running,
            Running => Done,
            Done => Done,
        }
    }

    fn status() string {
        return is self.state {
            Idle => "idle",
            Running => "running",
            Done => "done",
        }
    }
}

fn main() {
    let t = Task.new("build")
    print(t.status())
    t.advance()
    print(t.status())
    t.advance()
    print(t.status())
}
```

```typescript
enum State {
    Idle,
    Running,
    Done
}

class Task {
    state: State;
    name: string;

    constructor(state: State, name: string) {
        this.state = state;
        this.name = name;
    }

    advance(): void {
        this.state = (() => {
            switch (this.state) {
                case State.Idle: return State.Running;
                case State.Running: return State.Done;
                case State.Done: return State.Done;
            }
        })();
    }

    status(): string {
        return (() => {
            switch (this.state) {
                case State.Idle: return "idle";
                case State.Running: return "running";
                case State.Done: return "done";
            }
        })();
    }
}

function main(): void {
    const t = Task.new("build");
    console.log(t.status());
    t.advance();
    console.log(t.status());
    t.advance();
    console.log(t.status());
}

main();
```

This pattern is more explicit and exhaustive than class hierarchies with
overridden methods. The `is` expression ensures every case is handled.

## TypeScript-Only: Accessors (get/set)

TypeScript supports getter and setter accessors:

```typescript
// TypeScript only
class Temperature {
    private _celsius: number = 0;

    get fahrenheit(): number {
        return this._celsius * 9 / 5 + 32;
    }

    set fahrenheit(value: number) {
        this._celsius = (value - 32) * 5 / 9;
    }
}

const temp = new Temperature();
temp.fahrenheit = 212;
console.log(temp.celsius);  // 100
```

Getters and setters provide controlled access to underlying fields. They are
called like properties, not methods.

## TypeScript-Only: Abstract Classes

TypeScript's `abstract` keyword defines a base class that cannot be
instantiated directly:

```typescript
// TypeScript only
abstract class Shape {
    abstract getArea(): number;

    describe(): string {
        return `Area: ${this.getArea()}`;
    }
}

class Circle extends Shape {
    constructor(public radius: number) {
        super();
    }

    getArea(): number {
        return Math.PI * this.radius * this.radius;
    }
}

const circle = new Circle(5);
console.log(circle.describe());
```

Abstract classes define methods that subclasses must implement, while
providing shared implementation for other methods.

## TypeScript-Only: Visibility Modifiers

TypeScript supports three visibility modifiers for class members:

```typescript
// TypeScript only
class BankAccount {
    public owner: string;
    private balance: number;
    protected id: number;

    constructor(owner: string, balance: number, id: number) {
        this.owner = owner;
        this.balance = balance;
        this.id = id;
    }
}

class SavingsAccount extends BankAccount {
    getDetails(): string {
        return `${this.owner} (id: ${this.id})`;
        // this.balance  // Error: private
    }
}
```

- `public` — accessible everywhere (default)
- `private` — accessible only within the class
- `protected` — accessible within the class and its subclasses

Auto does not have visibility modifiers. All fields and methods are
publicly accessible.

## TypeScript-Only: Static Members

TypeScript supports static members and static initialization blocks:

```typescript
// TypeScript only
class Config {
    static instance: Config;
    static readonly VERSION = "1.0.0";

    private constructor() {}

    static {
        Config.instance = new Config();
    }

    static getInstance(): Config {
        return Config.instance;
    }
}

const cfg = Config.getInstance();
console.log(Config.VERSION);
```

Static members belong to the class itself rather than to instances. The
`static { }` block runs once when the class is defined. Auto does not have
a `static` keyword; use module-level functions and variables instead.

## Quick Reference

| TypeScript | Auto | Description |
|-----------|------|-------------|
| `class X { }` | `type X { }` | Define a type |
| `this` | `self` | Reference current instance |
| `class X implements Y` | `type X as Y { }` | Implement spec |
| `class X extends Y` | -- | Inheritance (TS-only) |
| `get prop()` / `set prop()` | -- | Accessors (TS-only) |
| `abstract class X` | -- | Abstract class (TS-only) |
| `public` / `private` / `protected` | -- | Visibility (TS-only) |
| `static` members | -- | Static members (TS-only) |
| `type X has Y { }` | `type X has Y { }` | Composition |
