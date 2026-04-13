# Object-Oriented Patterns in Auto

Object-oriented programming (OOP) is a way of modeling programs. Objects as a
programmatic concept were introduced in the programming language Simula in the
1960s. Many competing definitions describe what OOP is, and by some of these
definitions Auto is object oriented but by others it is not. In this chapter,
we'll explore certain characteristics that are commonly considered object
oriented and how those characteristics translate to idiomatic Auto.

Auto provides three key mechanisms for OOP-style patterns:

- **`spec`** — specs define shared behavior (similar to Rust's `trait`)
- **`is`** — type composition and behavioral contracts (replacing inheritance)
- **`has`** — delegation of behavior through composition

We'll then show how to implement an object-oriented design pattern in Auto and
discuss the trade-offs of doing so versus implementing a solution using some of
Auto's strengths instead.

## Characteristics of Object-Oriented Languages

There is no consensus in the programming community about what features a
language must have to be considered object oriented. Auto is influenced by many
programming paradigms, including OOP; for example, we explored the features
that came from functional programming in Chapter 13. Arguably, OOP languages
share certain common characteristics — namely, objects, encapsulation, and
inheritance. Let's look at what each of those characteristics means and whether
Auto supports it.

### Objects Contain Data and Behavior

The book _Design Patterns: Elements of Reusable Object-Oriented Software_ by
Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides (Addison-Wesley,
1994), colloquially referred to as _The Gang of Four_ book, defines OOP in this
way:

> Object-oriented programs are made up of objects. An __object__ packages both
> data and the procedures that operate on that data. The procedures are
> typically called __methods__ or __operations__.

Using this definition, Auto is object oriented: types have data, and `ext`
blocks provide methods on types. Even though types with methods aren't _called_
objects in Auto, they provide the same functionality according to the Gang of
Four's definition of objects.

<Listing number="18-1" file-name="src/lib.at" caption="A type that packages data and behavior">

```auto
pub type AveragedCollection {
    list List<int>
    average f64
}

ext AveragedCollection {
    pub fn new() AveragedCollection {
        AveragedCollection(list: List.new(), average: 0.0)
    }

    pub fn add(mut, value int) {
        .list.push(value)
        .update_average()
    }

    pub fn remove(mut) ?int {
        let result = .list.pop()
        if let Some(value) = result {
            .update_average()
        }
        result
    }

    pub fn average() f64 {
        .average
    }

    fn update_average(mut) {
        let total = .list.fold(0, (acc, x) => acc + x)
        .average = total as f64 / .list.len() as f64
    }
}
```

```rust
pub struct AveragedCollection {
    list: Vec<i32>,
    average: f64,
}

impl AveragedCollection {
    pub fn new() -> AveragedCollection {
        AveragedCollection { list: Vec::new(), average: 0.0 }
    }

    pub fn add(&mut self, value: i32) {
        self.list.push(value);
        self.update_average();
    }

    pub fn remove(&mut self) -> Option<i32> {
        let result = self.list.pop();
        if result.is_some() {
            self.update_average();
        }
        result
    }

    pub fn average(&self) -> f64 {
        self.average
    }

    fn update_average(&mut self) {
        let total: i32 = self.list.iter().sum();
        self.average = total as f64 / self.list.len() as f64;
    }
}
```

</Listing>

The `type` keyword defines a data structure with fields, and `ext` blocks
attach behavior. This is the Auto equivalent of a class in traditional OOP
languages.

### Encapsulation That Hides Implementation Details

Another aspect commonly associated with OOP is the idea of _encapsulation_,
which means that the implementation details of an object aren't accessible to
code using that object. Therefore, the only way to interact with an object is
through its public API.

In Listing 18-1, the `list` and `average` fields are private by default in
Auto. Only the methods marked `pub` are accessible from outside the type. The
`update_average` method is private — it's an implementation detail.

We discussed how to control encapsulation in Chapter 7: we can use the `pub`
keyword to decide which modules, types, functions, and methods in our code
should be public, and by default everything else is private.

Because we've encapsulated the implementation details of
`AveragedCollection`, we can easily change aspects, such as the data structure,
in the future. For instance, we could use a `Set<int>` instead of a
`List<int>` for the `list` field. As long as the signatures of the `add`,
`remove`, and `average` public methods stayed the same, code using
`AveragedCollection` wouldn't need to change.

If encapsulation is a required aspect for a language to be considered object
oriented, then Auto meets that requirement. The option to use `pub` or not for
different parts of code enables encapsulation of implementation details.

### Inheritance: Replaced by Composition and Specs

_Inheritance_ is a mechanism whereby an object can inherit elements from another
object's definition, thus gaining the parent object's data and behavior without
you having to define them again.

If a language must have inheritance to be object oriented, then Auto is not
such a language. There is no way to define a type that inherits the parent
type's fields and method implementations.

However, Auto provides powerful alternatives:

1. **`spec` with default implementations** — for code reuse (like Rust's traits)
2. **`is` composition** — for type relationships (replacing inheritance)
3. **`has` delegation** — for forwarding behavior to contained types

You would choose inheritance for two main reasons. One is for reuse of code:
you can implement particular behavior for one type, and inheritance enables you
to reuse that implementation for a different type. In Auto, you can achieve
this with `spec` default implementations.

The other reason to use inheritance relates to the type system: to enable a
child type to be used in the same places as the parent type. This is also
called _polymorphism_. In Auto, you achieve this through `spec` bounds and
generic types.

### Polymorphism

_Polymorphism_ means that you can substitute multiple objects for each other at
runtime if they share certain characteristics.

Auto uses generics to abstract over different possible types and `spec` bounds
to impose constraints on what those types must provide. This is sometimes called
_bounded parametric polymorphism_, the same approach Rust takes.

## The `is`/`has`/`spec` Triangle

Auto's approach to OOP centers on three keywords that work together:

| Keyword | Purpose | OOP Equivalent |
|---------|---------|---------------|
| `spec` | Define shared behavior | Interface / Trait |
| `is` | Compose types, assert contracts | Inheritance (type relationship) |
| `has` | Delegate behavior via composition | Composition + delegation |

### `spec`: Defining Shared Behavior

A `spec` defines a set of methods that a type must implement. This is
identical to Rust's `trait` or an interface in Java/Go:

<Listing number="18-2" file-name="src/lib.at" caption="Defining a spec with a default implementation">

```auto
pub spec Summary {
    fn summarize() String {
        "(Read more...)"
    }
}
```

```rust
pub trait Summary {
    fn summarize(&self) -> String {
        String::from("(Read more...)")
    }
}
```

</Listing>

Types implement specs using the `spec ... for Type` syntax:

<Listing number="18-3" file-name="src/lib.at" caption="Implementing a spec for a type">

```auto
type Article {
    title String
    author String
    content String
}

spec Summary for Article {
    fn summarize() String {
        f"${.title} by ${.author}"
    }
}
```

```rust
pub struct Article {
    pub title: String,
    pub author: String,
    pub content: String,
}

impl Summary for Article {
    fn summarize(&self) -> String {
        format!("{} by {}", self.title, self.author)
    }
}
```

</Listing>

### `is`: Type Composition and Contracts

The `is` keyword serves two purposes:

1. **Composing types** — embedding one type's fields into another
2. **Asserting spec contracts** — declaring that a type satisfies a spec

<Listing number="18-4" file-name="src/main.at" caption="Using `is` for type composition">

```auto
type Animal {
    name String
    age int
}

type Dog {
    is Animal          // Dog has all fields of Animal
    breed String
}

fn main() {
    let dog = Dog(name: "Rex", age: 3, breed: "German Shepherd")
    print(f"${dog.name} is ${dog.age} years old")  // Accesses Animal fields
    print(f"Breed: ${dog.breed}")
}
```

```rust
struct Animal {
    name: String,
    age: i32,
}

struct Dog {
    animal: Animal,    // Manual composition
    breed: String,
}

fn main() {
    let dog = Dog {
        animal: Animal { name: String::from("Rex"), age: 3 },
        breed: String::from("German Shepherd"),
    };
    println!("{} is {} years old", dog.animal.name, dog.animal.age);
    println!("Breed: {}", dog.breed);
}
```

</Listing>

In Rust, composition requires accessing nested fields (`dog.animal.name`). In
Auto, `is` flattens the composition — `dog.name` works directly because `Dog
is Animal`.

You can also use `is` to assert that a type implements a spec:

```auto
type Dog {
    is Animal
    is Summary       // Assert Dog implements Summary
    breed String
}
```

### `has`: Delegation Through Composition

The `has` keyword delegates method implementations to a contained type:

<Listing number="18-5" file-name="src/main.at" caption="Using `has` for delegation">

```auto
type Engine {
    horsepower int
}

ext Engine {
    fn start() {
        print("Engine started!")
    }

    fn stop() {
        print("Engine stopped!")
    }
}

type Car {
    has Engine            // Car delegates Engine methods
    make String
    model String
}

fn main() {
    let car = Car(
        horsepower: 200,
        make: "Toyota",
        model: "Camry"
    )
    car.start()           // Delegated to Engine.start()
    car.stop()            // Delegated to Engine.stop()
}
```

```rust
struct Engine {
    horsepower: i32,
}

impl Engine {
    fn start(&self) {
        println!("Engine started!");
    }

    fn stop(&self) {
        println!("Engine stopped!");
    }
}

struct Car {
    engine: Engine,
    make: String,
    model: String,
}

impl Car {
    fn start(&self) {
        self.engine.start();    // Manual delegation
    }

    fn stop(&self) {
        self.engine.stop();     // Manual delegation
    }
}

fn main() {
    let car = Car {
        engine: Engine { horsepower: 200 },
        make: String::from("Toyota"),
        model: String::from("Camry"),
    };
    car.start();
    car.stop();
}
```

</Listing>

In Rust, you must write delegation methods manually (`self.engine.start()`).
Auto's `has` keyword automatically forwards method calls to the contained type.

### `is` vs `has`

| Feature | `is` | `has` |
|---------|------|-------|
| Purpose | Compose fields | Delegate behavior |
| Field access | Flattened (direct) | Through the field |
| Method delegation | No | Yes |
| Multiple | A type can `is` multiple types | A type can `has` multiple types |
| Analog | Inheritance (data) | Composition (behavior) |

Use `is` when you want to share data structure. Use `has` when you want to
share behavior without exposing the inner type's fields.

## Using Specs for Polymorphism

### Spec Objects: Dynamic Dispatch

Like Rust's `dyn Trait`, Auto supports dynamic dispatch through spec objects.
When you need a collection of heterogeneous types that all implement the same
spec, you use spec objects:

<Listing number="18-6" file-name="src/lib.at" caption="Using spec objects for a GUI library">

```auto
pub spec Draw {
    fn draw()
}

pub type Screen {
    components List<Box<dyn Draw>>
}

ext Screen {
    pub fn run() {
        for component in .components {
            component.draw()
        }
    }
}
```

```rust
pub trait Draw {
    fn draw(&self);
}

pub struct Screen {
    pub components: Vec<Box<dyn Draw>>,
}

impl Screen {
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw();
        }
    }
}
```

</Listing>

The `dyn Draw` syntax creates a _spec object_ — a reference to any type that
implements the `Draw` spec. This is exactly analogous to Rust's `dyn Trait`.

### Implementing Specs for Concrete Types

<Listing number="18-7" file-name="src/lib.at" caption="Implementing `Draw` for `Button`">

```auto
pub type Button {
    width int
    height int
    label String
}

spec Draw for Button {
    fn draw() {
        // Code to actually draw a button
    }
}
```

```rust
pub struct Button {
    pub width: u32,
    pub height: u32,
    pub label: String,
}

impl Draw for Button {
    fn draw(&self) {
        // Code to actually draw a button
    }
}
```

</Listing>

Now a `Screen` can hold both `Button` and any other type that implements
`Draw`:

<Listing number="18-8" file-name="src/main.at" caption="Using heterogeneous types with spec objects">

```auto
use gui::{Button, Screen, Draw}

type SelectBox {
    width int
    height int
    options List<String>
}

spec Draw for SelectBox {
    fn draw() {
        // Code to actually draw a select box
    }
}

fn main() {
    let screen = Screen(components: [
        Box.new(SelectBox(
            width: 75,
            height: 10,
            options: ["Yes", "Maybe", "No"]
        )),
        Box.new(Button(
            width: 50,
            height: 10,
            label: "OK"
        )),
    ])

    screen.run()
}
```

```rust
use gui::{Button, Screen, Draw};

struct SelectBox {
    width: u32,
    height: u32,
    options: Vec<String>,
}

impl Draw for SelectBox {
    fn draw(&self) {
        // Code to actually draw a select box
    }
}

fn main() {
    let screen = Screen {
        components: vec![
            Box::new(SelectBox {
                width: 75,
                height: 10,
                options: vec![
                    String::from("Yes"),
                    String::from("Maybe"),
                    String::from("No"),
                ],
            }),
            Box::new(Button {
                width: 50,
                height: 10,
                label: String::from("OK"),
            }),
        ],
    };

    screen.run();
}
```

</Listing>

### Static Dispatch vs Dynamic Dispatch

When you use generics with spec bounds, Auto performs _static dispatch_ — the
compiler generates specialized code for each concrete type. This is the same as
monomorphization in Rust:

```auto
// Static dispatch: each T gets its own compiled version
fn draw_all<T Draw>(items List<T>) {
    for item in items {
        item.draw()
    }
}
```

When you use spec objects (`dyn Draw`), Auto performs _dynamic dispatch_ — the
method to call is determined at runtime via a vtable:

```auto
// Dynamic dispatch: method looked up at runtime
fn draw_all(items List<Box<dyn Draw>>) {
    for item in items {
        item.draw()
    }
}
```

| Aspect | Static Dispatch (Generics) | Dynamic Dispatch (`dyn`) |
|--------|---------------------------|--------------------------|
| Performance | Faster (can inline) | Slight overhead (vtable lookup) |
| Flexibility | Single type per call | Multiple types per call |
| Binary size | Larger (monomorphization) | Smaller |
| Use when | Type is uniform | Types are mixed |

## The State Pattern in Auto

A classic OOP design pattern is the _State pattern_, where an object's behavior
changes based on its internal state. Let's implement a blog post workflow that
transitions through states: draft → review → published.

### Implementing the State Pattern

<Listing number="18-9" file-name="src/lib.at" caption="Blog post workflow using the state pattern">

```auto
type Post {
    state Box<dyn State>
    content String
}

spec State {
    fn request_review() Box<dyn State>
    fn approve() Box<dyn State>
    fn content() String {
        ""  // Default: no content
    }
}

type Draft {}

spec State for Draft {
    fn request_review() Box<dyn State> {
        Box.new(PendingReview())
    }

    fn approve() Box<dyn State> {
        Box.new(Draft())  // Can't approve a draft
    }
}

type PendingReview {}

spec State for PendingReview {
    fn request_review() Box<dyn State> {
        Box.new(PendingReview())  // Stay in review
    }

    fn approve() Box<dyn State> {
        Box.new(Published())
    }
}

type Published {}

spec State for Published {
    fn content() String {
        .content  // Return actual content
    }
}

ext Post {
    fn new() Post {
        Post(
            state: Box.new(Draft()),
            content: ""
        )
    }

    fn add_text(mut, text String) {
        .content += text
    }

    fn request_review(mut) {
        .state = .state.request_review()
    }

    fn approve(mut) {
        .state = .state.approve()
    }

    fn content() String {
        .state.content()
    }
}
```

```rust
pub struct Post {
    state: Option<Box<dyn State>>,
    content: String,
}

trait State {
    fn request_review(self: Box<Self>) -> Option<Box<dyn State>>;
    fn approve(self: Box<Self>) -> Option<Box<dyn State>>;
    fn content<'a>(&self, _post: &'a Post) -> &'a str {
        ""
    }
}

struct Draft {}

impl State for Draft {
    fn request_review(self: Box<Self>) -> Option<Box<dyn State>> {
        Some(Box::new(PendingReview {}))
    }
    fn approve(self: Box<Self>) -> Option<Box<dyn State>> {
        Some(self)
    }
}

struct PendingReview {}

impl State for PendingReview {
    fn request_review(self: Box<Self>) -> Option<Box<dyn State>> {
        Some(self)
    }
    fn approve(self: Box<Self>) -> Option<Box<dyn State>> {
        Some(Box::new(Published {}))
    }
}

struct Published {}

impl State for Published {
    fn content<'a>(&self, post: &'a Post) -> &'a str {
        &post.content
    }
}

impl Post {
    pub fn new() -> Post {
        Post {
            state: Some(Box::new(Draft {})),
            content: String::new(),
        }
    }

    pub fn add_text(&mut self, text: &str) {
        self.content.push_str(text);
    }

    pub fn request_review(&mut self) {
        if let Some(s) = self.state.take() {
            self.state = Some(s.request_review());
        }
    }

    pub fn approve(&mut self) {
        if let Some(s) = self.state.take() {
            self.state = Some(s.approve());
        }
    }

    pub fn content(&self) -> &str {
        self.state.as_ref().unwrap().content(self)
    }
}
```

</Listing>

Using the post:

<Listing number="18-10" file-name="src/main.at" caption="Using the blog post state machine">

```auto
fn main() {
    let post = Post.new()
    post.add_text("I ate a salad for lunch today")

    post.request_review()
    post.approve()

    print(post.content())  // I ate a salad for lunch today
}
```

```rust
fn main() {
    let mut post = Post::new();
    post.add_text("I ate a salad for lunch today");

    post.request_review();
    post.approve();

    assert_eq!("I ate a salad for lunch today", post.content());
}
```

</Listing>

### Encoding State in the Type System

Auto's `is` keyword provides an alternative: encoding states directly into the
type system. Instead of runtime state transitions, we use different types for
each state:

<Listing number="18-11" file-name="src/main.at" caption="Encoding state in the type system">

```auto
type DraftPost {
    content String
}

ext DraftPost {
    fn add_text(mut, text String) {
        .content += text
    }

    fn request_review() ReviewPost {
        ReviewPost(content: .content)
    }
}

type ReviewPost {
    content String
}

ext ReviewPost {
    fn approve() PublishedPost {
        PublishedPost(content: .content)
    }

    fn reject() DraftPost {
        DraftPost(content: .content)
    }
}

type PublishedPost {
    content String
}

ext PublishedPost {
    fn content() String {
        .content
    }
}
```

```rust
pub struct DraftPost {
    content: String,
}

impl DraftPost {
    pub fn add_text(&mut self, text: &str) {
        self.content.push_str(text);
    }

    pub fn request_review(self) -> PendingReviewPost {
        PendingReviewPost {
            content: self.content,
        }
    }
}

pub struct PendingReviewPost {
    content: String,
}

impl PendingReviewPost {
    pub fn approve(self) -> Post {
        Post {
            content: self.content,
        }
    }
}

pub struct Post {
    content: String,
}

impl Post {
    pub fn content(&self) -> &str {
        &self.content
    }
}
```

</Listing>

This approach has a significant advantage: the _type system_ prevents invalid
operations at compile time. You can't call `content()` on a `DraftPost` — it
doesn't exist on that type. You can't call `approve()` on a `DraftPost` — only
`request_review()` is available. The compiler enforces the state transitions.

Usage:

```auto
fn main() {
    let draft = DraftPost(content: "")
    draft.add_text("I ate a salad for lunch today")

    let review = draft.request_review()
    let published = review.approve()

    print(published.content())
}
```

```rust
fn main() {
    let mut draft = DraftPost { content: String::new() };
    draft.add_text("I ate a salad for lunch today");

    let review = draft.request_review();
    let published = review.approve();

    println!("{}", published.content());
}
```

This is the idiomatic Auto approach: use the type system to make illegal states
unrepresentable, rather than relying on runtime checks.

## `is`/`has`/`spec` vs Rust's OOP

| OOP Concept | Rust | Auto |
|-------------|------|------|
| Interface / Trait | `trait` | `spec` |
| Implementation | `impl Trait for Type` | `spec Trait for Type` |
| Dynamic dispatch | `dyn Trait` | `dyn Spec` |
| Composition | Manual: `self.inner.method()` | `has`: automatic delegation |
| Field embedding | Manual: `self.inner.field` | `is`: flattened access |
| Default methods | `trait` with default body | `spec` with default body |
| No inheritance | No inheritance | No inheritance (use `is`/`has`) |
| State pattern | `Box<dyn State>` | `dyn State` or type-state |

Auto's `is` and `has` keywords remove boilerplate that Rust requires for
composition and delegation. In Rust, composing two structs and delegating
methods requires manual wrapper methods. In Auto, `has` generates those
wrappers automatically.

## Object-Oriented Patterns Quick Reference

| Feature | Auto | Rust |
|---------|------|------|
| Define interface | `spec Name { }` | `trait Name { }` |
| Implement interface | `spec Name for Type { }` | `impl Name for Type { }` |
| Dynamic dispatch | `dyn Spec` | `dyn Trait` |
| Compose fields | `is Type` | Manual embedding |
| Delegate methods | `has Type` | Manual delegation |
| Default method | Body in spec | Body in trait |
| Encapsulation | `pub` / private by default | `pub` / private by default |
| Polymorphism | Generics + spec bounds | Generics + trait bounds |

## Summary

Auto supports object-oriented patterns through a combination of features:

1. **`type` and `ext`** — packages data and behavior, like objects
2. **Encapsulation** — `pub` controls visibility, fields are private by default
3. **`spec`** — defines shared behavior, like interfaces or traits
4. **`is`** — composes types with flattened field access
5. **`has`** — delegates behavior through automatic method forwarding
6. **`dyn Spec`** — dynamic dispatch for heterogeneous collections
7. **Type-state pattern** — encode states in the type system for compile-time
   safety

Auto deliberately avoids inheritance in favor of composition (`is`/`has`) and
behavioral contracts (`spec`). This produces more flexible designs where types
only share the behavior they explicitly opt into, and the type system catches
invalid state transitions at compile time rather than runtime.

In the next chapter, we'll explore Auto's pattern matching with the `is`
keyword and how it compares to Rust's `match` expressions.
