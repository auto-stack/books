# Type Compatibility

Type compatibility determines when one type can be used in place of another. Both TypeScript and Auto use **structural typing** — the *shape* of a type matters, not its name. This chapter covers the rules that govern when assignments, function calls, and generics are valid in each language.

## Structural Typing

In a *structurally typed* system, a value is compatible with a type if it has at least the required properties. The type's name is irrelevant — only its structure counts.

```typescript
// TypeScript — structural typing
interface Point2D { x: number; y: number; }
interface Point3D { x: number; y: number; z: number; }

const p3: Point3D = { x: 1, y: 2, z: 3 };
const p2: Point2D = p3;  // OK — Point3D has all Point2D properties
```

```auto
// Auto — structural typing
type Point2D { x f64, y f64 }
type Point3D { x f64, y f64, z f64 }

let p3 = Point3D(1.0, 2.0, 3.0)
let p2 = p3  // OK — Point3D has all Point2D fields
```

`Point3D` is assignable to `Point2D` because it contains *at least* `x` and `y`. The extra `z` field is simply ignored. This works the same in both TypeScript and Auto.

This contrasts with **nominal typing** (used by Java, Rust structs, Swift), where compatibility requires matching type names — `Point3D` would *not* be assignable to `Point2D` regardless of shared fields.

## Excess Property Checking

While structural typing allows extra fields in general, TypeScript applies **excess property checking** specifically to *object literals* assigned directly to a typed location. This catches accidental typos and misplaced properties.

```typescript
// TypeScript — excess property checking
interface Point2D { x: number; y: number; }

const p1: Point2D = { x: 1, y: 2, z: 3 };
// Error: Object literal may only specify known properties,
// and 'z' does not exist in type 'Point2D'.

const obj = { x: 1, y: 2, z: 3 };
const p2: Point2D = obj;  // OK — obj is a variable, not a literal
```

Auto follows the same principle. When you construct a type directly, unexpected fields are rejected. When you assign an existing variable, the structural rule applies — extra fields are fine.

```auto
type Point2D { x f64, y f64 }

let p1 = Point2D(1.0, 2.0, 3.0)
// Error — Point2D only accepts x and y

let obj = Point3D(1.0, 2.0, 3.0)
let p2 = obj  // OK — obj already exists, extra field is fine
```

This is a pragmatic compromise: strict enough to catch mistakes at construction time, flexible enough for structural assignments.

## Function Compatibility

Function types have their own compatibility rules, and this is where TypeScript and Auto begin to differ.

**Parameter types** — TypeScript uses *bivariance* for function parameters by default, meaning a function `(x: Base) => void` is assignable to `(x: Derived) => void` *and vice versa*. This is technically unsound but convenient for common patterns like event handlers.

```typescript
// TypeScript — bivariant function parameters
class Event { /* ... */ }
class MouseEvent extends Event { /* ... */ }

type EventHandler = (e: Event) => void;
const handler: EventHandler = (e: MouseEvent) => { /* ... */ };
// OK in TS — MouseEvent handler used where Event handler expected
```

Auto is **stricter** — function parameter types follow standard contravariance. A function accepting `Base` can be used where `Derived` is expected, but not the reverse. This is sound and avoids subtle bugs.

**Return types** — Both languages are *covariant* in return types. A function returning `Derived` is assignable to a function type returning `Base` — the more specific return type satisfies the broader contract.

```typescript
// TypeScript — covariant return types
class Animal { name: string; }
class Dog extends Animal { breed: string; }

function getDog(): Dog { return new Dog(); }
const getAnimal: () => Animal = getDog;  // OK
```

```auto
type Animal { name str }
type Dog { name str, breed str }

fn get_dog() Dog { Dog("Rex", "Labrador") }
let get_animal = get_dog  // OK — Dog return is fine for Animal expectation
```

## Enum Compatibility

TypeScript enums are unusual: each enum value is a number, and enums are compatible with `number` but *not* with other enums.

```typescript
// TypeScript — enum compatibility
enum Direction { Up, Down, Left, Right }
enum Status { Active, Inactive }

let d: Direction = Direction.Up;
let n: number = d;       // OK — enums are numbers
// let s: Status = d;     // Error — different enum types
```

Auto enums are **algebraic data types** — each variant is a distinct tagged type, not a number. There is no implicit numeric compatibility.

```auto
enum Direction {
    Up
    Down
    Left
    Right
}

let d = Direction.Up
// let n = d  // Error — Direction is not a number
```

Auto enum variants can carry data, making them far more expressive than TypeScript's number-based enums:

```auto
enum Shape {
    Circle(radius f64)
    Rectangle(width f64, height f64)
}

fn area(s Shape) f64 {
    match s {
        Circle(r) => 3.14159 * r * r
        Rectangle(w, h) => w * h
    }
}
```

## Class Compatibility

TypeScript compares classes based on their *instance members* only. Constructors and static members are ignored for compatibility purposes.

```typescript
// TypeScript — class compatibility
class Animal {
    name: string;
    constructor(name: string) { this.name = name; }
}

class Person {
    name: string;
    age: number;
    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }
}

let animal: Animal = new Person("Alice", 30);  // OK
```

However, TypeScript makes an exception for `private` and `protected` members. When a class has private or protected fields, compatibility becomes *nominal* — two classes are only compatible if they share the same private/protected declaration.

```typescript
class Secret {
    private id: number;
    constructor(id: number) { this.id = id; }
}

class OtherSecret {
    private id: number;
    constructor(id: number) { this.id = id; }
}

// let s: Secret = new OtherSecret(1);  // Error — different private declarations
```

Auto has **no access modifiers** — all fields are visible. Type compatibility is always structural, regardless of how the type was constructed. This eliminates the confusion of TypeScript's hybrid approach.

```auto
type Animal { name str }
type Person { name str, age int }

let animal = Person("Alice", 30)  // OK — structural compatibility
```

## Generic Type Compatibility

Generic types are compatible when their type arguments are compatible. `Box<int>` and `Box<str>` are *incompatible* — the parameter type differs, so the container types differ.

```typescript
// TypeScript — generic compatibility
class Box<T> { value: T; }

const intBox: Box<number> = { value: 42 };
const strBox: Box<string> = { value: "hello" };

// let a: Box<number> = strBox;  // Error — Box<string> not assignable to Box<number>
```

```auto
type Box<T> { value T }

let int_box = Box<int>(42)
let str_box = Box("hello")

// let a = str_box  // Error — Box<str> not compatible with Box<int>
```

Covariance applies when the type parameter is only used in output positions. If `T` appears only as a return type, `Box<Derived>` can be assigned to `Box<Base>`. Both languages respect this rule, though TypeScript's structural system may infer it more freely.

## Structural Assignment in Practice

<Listing name="structural-assign" file="listings/ch08-structural-assign">

```typescript
// TypeScript — structural type compatibility
interface Point2D { x: number; y: number; }
interface Point3D { x: number; y: number; z: number; }

function printX(p: Point2D): void {
    console.log("x = " + p.x);
}

interface Named { name: string; }
interface Employee { name: string; role: string; }

function greet(n: Named): void {
    console.log("Hello, " + n.name);
}

const p2: Point2D = { x: 1, y: 2 };
const p3: Point3D = { x: 1, y: 2, z: 3 };

printX(p2);  // exact match
printX(p3);  // OK — extra field is fine (structural)

const emp: Employee = { name: "Alice", role: "Engineer" };
greet(emp);  // OK — Employee has `name` property
```

```auto
// Auto — structural type compatibility
type Point2D {
    x f64
    y f64
}

type Point3D {
    x f64
    y f64
    z f64
}

fn print_x(p Point2D) {
    print("x = {p.x}")
}

type Named {
    name str
}

type Employee {
    name str
    role str
}

fn greet(n Named) {
    print("Hello, {n.name}")
}

fn main() {
    let p2 = Point2D(1.0, 2.0)
    let p3 = Point3D(1.0, 2.0, 3.0)

    print_x(p2)   // exact match
    print_x(p3)   // OK — extra field is fine (structural)

    let emp = Employee("Alice", "Engineer")
    greet(emp)    // OK — Employee has `name` field
}
```

</Listing>

## Quick Reference

| Concept | TypeScript | Auto |
|---|---|---|
| Typing discipline | Structural | Structural |
| Extra fields | OK (except object literals) | OK (except direct construction) |
| Function params | Bivariant (unsound) | Contravariant (sound) |
| Return types | Covariant | Covariant |
| Enum compatibility | Numeric, cross-enum incompatible | ADT, no numeric conversion |
| Private/protected | Creates nominal compatibility | Not supported (always structural) |
| Generic compat | By type argument compatibility | By type argument compatibility |
| `Box<int>` vs `Box<str>` | Incompatible | Incompatible |
