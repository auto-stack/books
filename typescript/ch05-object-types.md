# Object Types

Auto provides two primary mechanisms for defining object types: `type` for
data structures (transpiles to TypeScript `class`) and `spec` for behavioral
contracts (transpiles to TypeScript `interface`).

## The `spec` Keyword (Interfaces)

Use `spec` to define a behavioral contract — a set of method signatures that
a type must implement. This is Auto's equivalent of TypeScript's `interface`.

<Listing number="05-01" file="listings/ch05/listing-05-01/main.at" caption="Spec declaration">

```auto
spec Greetable {
    fn greet()
}

fn main() {
    print("spec Greetable defined")
}
```

```typescript
function main(): void {
    console.log("spec Greetable defined");
}

main();
```

</Listing>

A `spec` transpiles to a TypeScript `interface` with method signatures.
Types that implement the spec must provide concrete implementations of all
methods.

## Implementing a Spec

Use `type Name as SpecName` to declare that a type implements a spec. This
is Auto's equivalent of TypeScript's `class X implements Y`.

<Listing number="05-02" file="listings/ch05/listing-05-02/main.at" caption="Implementing a spec">

```auto
spec Greetable {
    fn greet()
}

type User as Greetable {
    name int
    fn greet() {
        print("Hello from user", self.name)
    }
}

fn main() {
    let user = User(42)
    user.greet()
}
```

```typescript
class User implements Greetable {
    name: number;

    constructor(name: number) {
        this.name = name;
    }

    greet(): void {
        console.log("Hello from user", this.name);
    }
}

function main(): void {
    const user = User(42);
    user.greet();
}

main();
```

</Listing>

The `as Greetable` clause on the type declaration tells the TypeScript
compiler that `User` implements the `Greetable` interface. Methods defined
inside the `type` block become class methods that use `self` (transpiled to
`this`) for field access.

## Composition with `has`

Auto supports composition via the `has` keyword. When a type `has` another
type, it embeds all of its methods. This is a form of mixin or trait
composition.

<Listing number="05-04" file="listings/ch05/listing-05-04/main.at" caption="Composition with has">

```auto
type Wing {
    fn flap() {
        print("Flap!")
    }
}

type Duck has Wing {
    name int
}

fn main() {
    let duck = Duck(1)
    duck.flap()
    print("Duck name:", duck.name)
}
```

```typescript
class Wing {

    flap(): void {
    console.log("Flap!");
}
}

class Duck {
    name: number;

    constructor(name: number) {
        this.name = name;
    }

    flap(): void {
    console.log("Flap!");
}
}

function main(): void {
    const duck = Duck(1);
    duck.flap();
    console.log("Duck name:", duck.name);
}

main();
```

</Listing>

The `type Duck has Wing` declaration embeds all methods from `Wing` into
`Duck`. In the TypeScript output, the methods are inlined directly into the
`Duck` class. This is a powerful alternative to inheritance — you get code
reuse without the tight coupling of an `extends` chain.

## Optional Fields

Auto supports optional fields using the `?` suffix on the field name:

<Listing number="05-05" file="listings/ch05/listing-05-05/main.at" caption="Optional fields">

```auto
type Config {
    host int
    port? int
}

fn main() {
    let c = Config(8080)
    print("Host:", c.host)
    if c.port {
        print("Port:", c.port)
    }
}
```

```typescript
class Config {
    host: number;
    port: number | null;

    constructor(host: number, port: number | null) {
        this.host = host;
        this.port = port;
    }
}

function main(): void {
    const c = Config(8080);
    console.log("Host:", c.host);
    if (c.port) {
        console.log("Port:", c.port);
    }
}

main();
```

</Listing>

Optional fields transpile to TypeScript optional properties (`port?: number`)
with an optional constructor parameter.

## Quick Reference

| TypeScript | Auto | Description |
|-----------|------|-------------|
| `interface X { }` | `spec X { }` | Behavioral contract |
| `class X implements Y` | `type X as Y { }` | Implement interface |
| `class X extends Y` | — | Inheritance (TS-only) |
| `class X { ... }` | `type X { ... }` | Data structure |
| `obj.x` | `self.x` or `obj.x` | Property access |
| `prop?: T` | `prop? T` | Optional property |

## TypeScript-Only Features

### Inheritance (`extends`)

```typescript
// TypeScript only
class Dog extends Animal {
    breed: string;
}
```

Auto does not currently support type inheritance via `extends` in the a2ts
transpiler. Use composition with `has` instead.

### Intersection Types (`&`)

```typescript
// TypeScript only
type ColorfulCircle = Colorful & Circle;
```

Auto uses `has` for composition, which achieves similar goals at the
implementation level.

### Readonly Properties

```typescript
// TypeScript only
class Person {
    readonly name: string;
}
```

Auto uses `let` (immutable) for variables but does not have a `readonly`
modifier for fields.
