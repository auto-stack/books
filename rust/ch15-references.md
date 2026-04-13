# References and Pointers

A _pointer_ is a general concept for a variable that contains an address in
memory. This address refers to, or "points at," some other data. The most common
kind of pointer in Auto is a _reference_, which you learned about in
[Chapter 4][ch4]. References borrow the value they point to. They don't have any
special capabilities other than referring to data, and they have no overhead.

_Smart pointers_, on the other hand, are data structures that act like a pointer
but also have additional metadata and capabilities. The concept of smart pointers
isn't unique to Rust: smart pointers originated in C++ and exist in other
languages as well. Rust has a variety of smart pointers defined in the standard
library that provide functionality beyond that provided by references. Auto
shares many of these concepts through its interop with Rust.

In Auto, with its concept of ownership and implicit move, there is an additional
difference between references and smart pointers: while references only borrow
data, in many cases smart pointers _own_ the data they point to.

Smart pointers are usually implemented using types. Unlike an ordinary type,
smart pointers implement specs that provide pointer-like behavior. The `Deref`
spec allows an instance of the smart pointer type to behave like a reference so
that you can write your code to work with either references or smart pointers.
The `Drop` spec allows you to customize the code that's run when an instance of
the smart pointer goes out of scope. In this chapter, we'll discuss both of
these specs and demonstrate why they're important to smart pointers.

Given that the smart pointer pattern is a general design pattern used
frequently, this chapter won't cover every existing smart pointer. Many
libraries have their own smart pointers, and you can even write your own. We'll
cover the most common smart pointer patterns:

- **Heap allocation**, for allocating values on the heap
- **Reference counting**, a type that enables multiple ownership
- **Interior mutability**, a type that enforces the borrowing rules at runtime
  instead of compile time

In addition, we'll cover the _interior mutability_ pattern where an immutable
type exposes an API for mutating an interior value. We'll also discuss reference
cycles: how they can leak memory and how to prevent them.

> **Note:** Auto's smart pointer types leverage Rust's standard library through
> the `use.rust` mechanism. While Auto has its own memory model (implicit move
> and AutoFree), the smart pointer patterns described here work identically when
> using Rust interop. Native Auto smart pointer APIs are planned for future
> releases.

Let's dive in!

## Using Heap Allocation to Point to Data

The most straightforward smart pointer is a _box_, which in Rust is written
`Box<T>`. Boxes allow you to store data on the heap rather than the stack. What
remains on the stack is the pointer to the heap data. Refer to [Chapter 4][ch4]
to review the difference between the stack and the heap.

Boxes don't have performance overhead, other than storing their data on the heap
instead of on the stack. But they don't have many extra capabilities either.
You'll use them most often in these situations:

- When you have a type whose size can't be known at compile time, and you want
  to use a value of that type in a context that requires an exact size
- When you have a large amount of data, and you want to transfer ownership but
  ensure that the data won't be copied when you do so
- When you want to own a value, and you care only that it's a type that
  implements a particular spec rather than being of a specific type

### Storing Data on the Heap

Listing 15-1 shows how to use a box to store an `int` value on the heap.

<Listing number="15-1" file-name="src/main.at" caption="Storing an `int` value on the heap using a box">

```auto
use.rust std::boxed::Box

fn main() {
    let b = Box.new(5)
    print(f"b = ${b}")
}
```

```rust
fn main() {
    let b = Box::new(5);
    println!("b = {b}");
}
```

</Listing>

We define the variable `b` to have the value of a `Box` that points to the value
`5`, which is allocated on the heap. This program will print `b = 5`; in this
case, we can access the data in the box similarly to how we would if this data
were on the stack. Just like any owned value, when a box goes out of scope, as
`b` does at the end of `main`, it will be deallocated. The deallocation happens
both for the box (stored on the stack) and the data it points to (stored on the
heap).

### Enabling Recursive Types with Boxes

A value of a _recursive type_ can have another value of the same type as part of
itself. Recursive types pose an issue because the compiler needs to know at
compile time how much space a type takes up. However, the nesting of values of
recursive types could theoretically continue infinitely, so the compiler can't
know how much space the value needs. Because boxes have a known size, we can
enable recursive types by inserting a box in the recursive type definition.

As an example of a recursive type, let's explore the cons list — a data type
commonly found in functional programming languages.

<Listing number="15-2" file-name="src/main.at" caption="Attempting to define a recursive enum (won't compile)">

```auto
// This won't compile — recursive type has infinite size
enum List {
    Cons(int, List)
    Nil
}

fn main() {}
```

```rust
enum List {
    Cons(i32, List),
    Nil,
}

fn main() {}
```

</Listing>

The error shows this type "has infinite size." The reason is that we've defined
`List` with a variant that is recursive: it holds another value of itself
directly. As a result, the compiler can't figure out how much space it needs to
store a `List` value.

Because a `Box<T>` is a pointer, the compiler always knows how much space a
`Box<T>` needs: a pointer's size doesn't change based on the amount of data it's
pointing to. This means we can put a `Box<T>` inside the `Cons` variant instead
of another `List` value directly.

<Listing number="15-3" file-name="src/main.at" caption="Definition of `List` using `Box<T>` for a known size">

```auto
use.rust std::boxed::Box

enum List {
    Cons(int, Box<List>)
    Nil
}

fn main() {
    let list = List.Cons(
        1,
        Box.new(List.Cons(
            2,
            Box.new(List.Cons(
                3,
                Box.new(List.Nil)
            ))
        ))
    )
}
```

```rust
enum List {
    Cons(i32, Box<List>),
    Nil,
}

use crate::List::{Cons, Nil};

fn main() {
    let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));
}
```

</Listing>

The `Cons` variant needs the size of an `int` plus the space to store the box's
pointer data. The `Nil` variant stores no values, so it needs less space on the
stack than the `Cons` variant. We now know that any `List` value will take up
the size of an `int` plus the size of a box's pointer data. By using a box,
we've broken the infinite, recursive chain, so the compiler can figure out the
size it needs to store a `List` value.

## Treating Smart Pointers Like Regular References

Implementing the `Deref` spec allows you to customize the behavior of the
_dereference operator_ `*`. By implementing `Deref` in such a way that a smart
pointer can be treated like a regular reference, you can write code that operates
on references and use that code with smart pointers too.

### Following the Pointer to the Value

A regular reference is a type of pointer, and one way to think of a pointer is
as an arrow to a value stored somewhere else. In Listing 15-4, we create a
reference to an `int` value and then use the dereference operator to follow the
reference to the value.

<Listing number="15-4" file-name="src/main.at" caption="Using the dereference operator to follow a reference">

```auto
fn main() {
    let x = 5
    let y = &x

    assert_eq(5, x)
    assert_eq(5, *y)
}
```

```rust
fn main() {
    let x = 5;
    let y = &x;

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```

</Listing>

The variable `x` holds an `int` value `5`. We set `y` equal to a reference to
`x`. We can assert that `x` is equal to `5`. However, if we want to make an
assertion about the value in `y`, we have to use `*y` to follow the reference to
the value it's pointing to.

### Using `Box<T>` Like a Reference

We can rewrite the code in Listing 15-4 to use a `Box<T>` instead of a
reference; the dereference operator used on the `Box<T>` functions in the same
way as the dereference operator used on the reference.

<Listing number="15-5" file-name="src/main.at" caption="Using the dereference operator on a `Box<int>`">

```auto
use.rust std::boxed::Box

fn main() {
    let x = 5
    let y = Box.new(x)

    assert_eq(5, x)
    assert_eq(5, *y)
}
```

```rust
fn main() {
    let x = 5;
    let y = Box::new(x);

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```

</Listing>

### Implementing the `Deref` Spec

To enable dereferencing with the `*` operator, a type implements the `Deref`
spec. The `Deref` spec requires implementing a `deref` method that borrows
`self` and returns a reference to the inner data.

<Listing number="15-6" file-name="src/main.at" caption="Implementing `Deref` on `MyBox<T>`">

```auto
type MyBox<T>(T)

ext MyBox {
    fn new(x T) MyBox<T> {
        MyBox(x)
    }
}

spec Deref for MyBox<T> {
    type Target = T

    fn deref() &T {
        &.0
    }
}

fn main() {
    let x = 5
    let y = MyBox.new(x)

    assert_eq(5, x)
    assert_eq(5, *y)
}
```

```rust
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn main() {
    let x = 5;
    let y = MyBox::new(x);

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```

</Listing>

The `type Target = T` syntax defines an associated type for the `Deref` spec.
We fill in the body of the `deref` method with `&.0` so that `deref` returns a
reference to the value we want to access with the `*` operator.

Without the `Deref` spec, the compiler can only dereference `&` references. The
`deref` method gives the compiler the ability to take a value of any type that
implements `Deref` and call the `deref` method to get a reference that it knows
how to dereference.

When we entered `*y`, behind the scenes the compiler actually ran `*(y.deref())`.
This feature lets us write code that functions identically whether we have a
regular reference or a type that implements `Deref`.

### Deref Coercion

_Deref coercion_ converts a reference to a type that implements the `Deref` spec
into a reference to another type. For example, deref coercion can convert
`&String` to `&str` because `String` implements `Deref` such that it returns
`&str`. Deref coercion happens automatically when we pass a reference to a
particular type's value as a function argument that doesn't match the parameter
type.

<Listing number="15-7" file-name="src/main.at" caption="Deref coercion in action">

```auto
fn hello(name String) {
    print(f"Hello, ${name}!")
}

fn main() {
    let m = MyBox.new(String.from("Auto"))
    hello(&m)  // deref coercion converts &MyBox<String> to &String
}
```

```rust
fn hello(name: &str) {
    println!("Hello, {name}!");
}

fn main() {
    let m = MyBox::new(String::from("Rust"));
    hello(&m);
}
```

</Listing>

Here we're calling the `hello` function with the argument `&m`, which is a
reference to a `MyBox<String>` value. Because `MyBox<T>` implements `Deref`, the
compiler can turn `&MyBox<String>` into `&String` by calling `deref`. The
standard library provides an implementation of `Deref` on `String` that returns a
string slice, and the compiler calls `deref` again to turn the `&String` into a
`&str`, which matches the `hello` function's definition.

Deref coercion also works with mutable references:

1. From `&T` to `&U` when `T: Deref<Target=U>`
2. From `&mut T` to `&mut U` when `T: DerefMut<Target=U>`
3. From `&mut T` to `&U` when `T: Deref<Target=U>`

The third case is trickier: the compiler will also coerce a mutable reference to
an immutable one. But the reverse is _not_ possible: immutable references will
never coerce to mutable references.

## Running Code on Cleanup with the `Drop` Spec

The second spec important to the smart pointer pattern is `Drop`, which lets you
customize what happens when a value is about to go out of scope. You can provide
an implementation for the `Drop` spec on any type, and that code can be used to
release resources like files or network connections.

In some languages, the programmer must call code to free memory or resources
every time they finish using an instance. If the programmer forgets, the system
might become overloaded and crash. In Auto, you can specify that a particular
bit of code be run whenever a value goes out of scope, and the compiler will
insert this code automatically. As a result, you don't need to be careful about
placing cleanup code everywhere in your program — you still won't leak
resources!

<Listing number="15-8" file-name="src/main.at" caption="A type that implements the `Drop` spec">

```auto
type CustomSmartPointer {
    data String
}

ext CustomSmartPointer {
    fn new(data String) CustomSmartPointer {
        CustomSmartPointer(data)
    }
}

spec Drop for CustomSmartPointer {
    fn drop() {
        print(f"Dropping CustomSmartPointer with data `${.data}`!")
    }
}

fn main() {
    let c = CustomSmartPointer.new(String.from("my stuff"))
    let d = CustomSmartPointer.new(String.from("other stuff"))
    print("CustomSmartPointers created")
}
```

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data `{}`!", self.data);
    }
}

fn main() {
    let c = CustomSmartPointer {
        data: String::from("my stuff"),
    };
    let d = CustomSmartPointer {
        data: String::from("other stuff"),
    };
    println!("CustomSmartPointers created");
}
```

</Listing>

When we run this program, we'll see the following output:

```text
CustomSmartPointers created
Dropping CustomSmartPointer with data `other stuff`!
Dropping CustomSmartPointer with data `my stuff`!
```

The compiler automatically called `drop` for us when our instances went out of
scope. Variables are dropped in the reverse order of their creation, so `d` was
dropped before `c`.

### Dropping a Value Early with `drop`

Occasionally, you might want to clean up a value early. One example is when
using smart pointers that manage locks: you might want to force the `drop`
method that releases the lock so that other code in the same scope can acquire
the lock. Auto doesn't let you call the `Drop` spec's `drop` method manually;
instead, you use the `drop()` function provided by the standard library.

<Listing number="15-9" file-name="src/main.at" caption="Calling `drop()` to explicitly drop a value before it goes out of scope">

```auto
type CustomSmartPointer {
    data String
}

spec Drop for CustomSmartPointer {
    fn drop() {
        print(f"Dropping CustomSmartPointer with data `${.data}`!")
    }
}

fn main() {
    let c = CustomSmartPointer(data: String.from("some data"))
    print("CustomSmartPointer created")
    drop(c)
    print("CustomSmartPointer dropped before the end of main")
}
```

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data `{}`!", self.data);
    }
}

fn main() {
    let c = CustomSmartPointer {
        data: String::from("some data"),
    };
    println!("CustomSmartPointer created");
    drop(c);
    println!("CustomSmartPointer dropped before the end of main");
}
```

</Listing>

Running this code will print:

```text
CustomSmartPointer created
Dropping CustomSmartPointer with data `some data`!
CustomSmartPointer dropped before the end of main
```

The `Dropping` message appears between the two `print` statements, showing that
`c` is dropped at that point. With the `Drop` spec and Auto's ownership system,
you don't have to remember to clean up — Auto does it automatically.

## Reference Counting: `Rc<T>`

In the majority of cases, ownership is clear: you know exactly which variable
owns a given value. However, there are cases when a single value might have
multiple owners. For example, in graph data structures, multiple edges might
point to the same node, and that node is conceptually owned by all of the edges
that point to it.

You have to enable multiple ownership explicitly by using the `Rc<T>` type,
which is an abbreviation for _reference counting_. The `Rc<T>` type keeps track
of the number of references to a value to determine whether or not the value is
still in use. If there are zero references to a value, the value can be cleaned
up without any references becoming invalid.

> **Note:** `Rc<T>` is only for use in single-threaded scenarios. When we
> discuss concurrency in [Chapter 16][ch16], we'll cover how to do reference
> counting in multithreaded programs.

### Sharing Data with `Rc<T>`

Let's return to our cons list example. This time, we'll create two lists that
both share ownership of a third list.

<Listing number="15-10" file-name="src/main.at" caption="Using `Rc<T>` to share ownership between two lists">

```auto
use.rust std::rc::Rc

enum List {
    Cons(int, Rc<List>)
    Nil
}

fn main() {
    let a = Rc.new(List.Cons(5, Rc.new(List.Cons(10, Rc.new(List.Nil)))))
    let b = List.Cons(3, Rc.clone(&a))
    let c = List.Cons(4, Rc.clone(&a))
}
```

```rust
use std::rc::Rc;

enum List {
    Cons(i32, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};

fn main() {
    let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
    let b = Cons(3, Rc::clone(&a));
    let c = Cons(4, Rc::clone(&a));
}
```

</Listing>

When we create `b`, instead of taking ownership of `a`, we clone the `Rc<List>`
that `a` is holding, thereby increasing the number of references from one to two
and letting `a` and `b` share ownership of the data. We also clone `a` when
creating `c`, increasing the number of references from two to three.

### Cloning to Increase the Reference Count

<Listing number="15-11" file-name="src/main.at" caption="Printing the reference count">

```auto
use.rust std::rc::Rc

enum List {
    Cons(int, Rc<List>)
    Nil
}

fn main() {
    let a = Rc.new(List.Cons(5, Rc.new(List.Cons(10, Rc.new(List.Nil)))))
    print(f"count after creating a = ${Rc.strong_count(&a)}")

    let b = List.Cons(3, Rc.clone(&a))
    print(f"count after creating b = ${Rc.strong_count(&a)}")

    {
        let c = List.Cons(4, Rc.clone(&a))
        print(f"count after creating c = ${Rc.strong_count(&a)}")
    }

    print(f"count after c goes out of scope = ${Rc.strong_count(&a)}")
}
```

```rust
use std::rc::Rc;

enum List {
    Cons(i32, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};

fn main() {
    let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
    println!("count after creating a = {}", Rc::strong_count(&a));
    let b = Cons(3, Rc::clone(&a));
    println!("count after creating b = {}", Rc::strong_count(&a));
    {
        let c = Cons(4, Rc::clone(&a));
        println!("count after creating c = {}", Rc::strong_count(&a));
    }
    println!("count after c goes out of scope = {}", Rc::strong_count(&a));
}
```

</Listing>

This code prints:

```text
count after creating a = 1
count after creating b = 2
count after creating c = 3
count after c goes out of scope = 2
```

We can see that the `Rc<List>` in `a` has an initial reference count of 1; then,
each time we call `clone`, the count goes up by 1. When `c` goes out of scope,
the count goes down by 1. We don't have to call a function to decrease the
reference count — the `Drop` implementation decreases it automatically when an
`Rc<T>` value goes out of scope.

## `RefCell<T>` and the Interior Mutability Pattern

_Interior mutability_ is a design pattern that allows you to mutate data even
when there are immutable references to that data; normally, this action is
disallowed by the borrowing rules. To mutate data, the pattern uses `sys`
(equivalent to Rust's `unsafe`) code inside a data structure to bend the usual
rules that govern mutation and borrowing. We will discuss `sys` more in
[Chapter 20][ch20].

### Enforcing Borrowing Rules at Runtime

Unlike `Rc<T>`, the `RefCell<T>` type represents single ownership over the data
it holds. Recall the borrowing rules you learned in [Chapter 4][ch4]:

- At any given time, you can have _either_ one mutable reference or any number
  of immutable references (but not both).
- References must always be valid.

With references and `Box<T>`, the borrowing rules' invariants are enforced at
compile time. With `RefCell<T>`, these invariants are enforced _at runtime_.
With references, if you break these rules, you'll get a compiler error. With
`RefCell<T>`, if you break these rules, your program will panic and exit.

Here is a recap of the reasons to choose `Box<T>`, `Rc<T>`, or `RefCell<T>`:

| Type | Owners | Borrow checking | Mutability |
|------|--------|----------------|------------|
| `Box<T>` | Single | Compile time | Immutable or mutable |
| `Rc<T>` | Multiple | Compile time | Immutable only |
| `RefCell<T>` | Single | Runtime | Immutable or mutable |

### Using Interior Mutability: Mock Objects

A practical use case for `RefCell<T>` is creating mock objects during testing.
Here's an example using a `Messenger` spec:

<Listing number="15-12" file-name="src/lib.at" caption="Using `RefCell<T>` to mutate an inner value while the outer value is immutable">

```auto
use.rust std::cell::RefCell

spec Messenger {
    fn send(msg String)
}

type LimitTracker<T Messenger> {
    messenger &T
    value int
    max int
}

ext LimitTracker {
    fn new(messenger &T, max int) LimitTracker<T> {
        LimitTracker(messenger, value: 0, max)
    }

    fn set_value(mut, value int) {
        .value = value
        let percentage = .value as f64 / .max as f64

        if percentage >= 1.0 {
            .messenger.send("Error: You are over your quota!")
        } else if percentage >= 0.9 {
            .messenger.send("Urgent warning: You've used up over 90% of your quota!")
        } else if percentage >= 0.75 {
            .messenger.send("Warning: You've used up over 75% of your quota!")
        }
    }
}

#[test]
fn it_sends_an_over_75_percent_warning_message() {
    type MockMessenger {
        sent_messages RefCell<List<String>>
    }

    ext MockMessenger {
        fn new() MockMessenger {
            MockMessenger(sent_messages: RefCell.new(List.new()))
        }
    }

    spec Messenger for MockMessenger {
        fn send(msg String) {
            .sent_messages.borrow_mut().push(msg)
        }
    }

    let mock_messenger = MockMessenger.new()
    var limit_tracker = LimitTracker.new(&mock_messenger, 100)

    limit_tracker.set_value(80)

    assert_eq(1, mock_messenger.sent_messages.borrow().len())
}
```

```rust
pub trait Messenger {
    fn send(&self, msg: &str);
}

pub struct LimitTracker<'a, T: Messenger> {
    messenger: &'a T,
    value: usize,
    max: usize,
}

impl<'a, T: Messenger> LimitTracker<'a, T> {
    pub fn new(messenger: &'a T, max: usize) -> LimitTracker<'a, T> {
        LimitTracker { messenger, value: 0, max }
    }

    pub fn set_value(&mut self, value: usize) {
        self.value = value;
        let percentage = self.value as f64 / self.max as f64;
        if percentage >= 1.0 {
            self.messenger.send("Error: You are over your quota!");
        } else if percentage >= 0.9 {
            self.messenger.send("Urgent warning: You've used up over 90%!");
        } else if percentage >= 0.75 {
            self.messenger.send("Warning: You've used up over 75%!");
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::RefCell;

    struct MockMessenger {
        sent_messages: RefCell<Vec<String>>,
    }

    impl MockMessenger {
        fn new() -> MockMessenger {
            MockMessenger { sent_messages: RefCell::new(vec![]) }
        }
    }

    impl Messenger for MockMessenger {
        fn send(&self, message: &str) {
            self.sent_messages.borrow_mut().push(String::from(message));
        }
    }

    #[test]
    fn it_sends_an_over_75_percent_warning_message() {
        let mock_messenger = MockMessenger::new();
        let mut limit_tracker = LimitTracker::new(&mock_messenger, 100);
        limit_tracker.set_value(80);
        assert_eq!(mock_messenger.sent_messages.borrow().len(), 1);
    }
}
```

</Listing>

The `sent_messages` field is now of type `RefCell<List<String>>`. The `send`
method calls `borrow_mut` on the `RefCell` to get a mutable reference to the
inner list. Even though `send` takes an immutable reference to `self`, we can
still mutate the inner data through `RefCell<T>`.

### Combining `Rc<T>` and `RefCell<T>`

A common way to use `RefCell<T>` is in combination with `Rc<T>`. Recall that
`Rc<T>` lets you have multiple owners of some data, but it only gives immutable
access to that data. If you have an `Rc<T>` that holds a `RefCell<T>`, you can
get a value that can have multiple owners _and_ that you can mutate.

<Listing number="15-13" file-name="src/main.at" caption="Using `Rc<RefCell<int>>` to create a `List` we can mutate">

```auto
use.rust std::cell::RefCell
use.rust std::rc::Rc

enum List {
    Cons(Rc<RefCell<int>>, Rc<List>)
    Nil
}

fn main() {
    let value = Rc.new(RefCell.new(5))

    let a = Rc.new(List.Cons(Rc.clone(&value), Rc.new(List.Nil)))

    let b = List.Cons(Rc.new(RefCell.new(3)), Rc.clone(&a))
    let c = List.Cons(Rc.new(RefCell.new(4)), Rc.clone(&a))

    *value.borrow_mut() += 10

    print(f"a after = ${a}")
    print(f"b after = ${b}")
    print(f"c after = ${c}")
}
```

```rust
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
enum List {
    Cons(Rc<RefCell<i32>>, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};

fn main() {
    let value = Rc::new(RefCell::new(5));
    let a = Rc::new(Cons(Rc::clone(&value), Rc::new(Nil)));
    let b = Cons(Rc::new(RefCell::new(3)), Rc::clone(&a));
    let c = Cons(Rc::new(RefCell::new(4)), Rc::clone(&a));
    *value.borrow_mut() += 10;
    println!("a after = {a:?}");
    println!("b after = {b:?}");
    println!("c after = {c:?}");
}
```

</Listing>

When we print `a`, `b`, and `c`, we can see that they all have the modified
value of `15` rather than `5`. By using `RefCell<T>`, we have an outwardly
immutable `List` value, but we can modify the data when we need to.

## Reference Cycles Can Leak Memory

Auto's memory safety guarantees make it difficult, but not impossible, to
accidentally create memory that is never cleaned up (known as a _memory leak_).
Preventing memory leaks entirely is not one of Auto's guarantees. We can see
that memory leaks are possible by using `Rc<T>` and `RefCell<T>`: it's possible
to create references where items refer to each other in a cycle. This creates
memory leaks because the reference count of each item in the cycle will never
reach 0, and the values will never be dropped.

### Creating a Reference Cycle

<Listing number="15-14" file-name="src/main.at" caption="Creating a reference cycle of two `List` values pointing to each other">

```auto
use.rust std::cell::RefCell
use.rust std::rc::Rc

enum List {
    Cons(int, RefCell<Rc<List>>)
    Nil
}

ext List {
    fn tail() ?&RefCell<Rc<List>> {
        self is
            List.Cons(_, item) -> Some(item)
            List.Nil -> None
    }
}

fn main() {
    let a = Rc.new(List.Cons(5, RefCell.new(Rc.new(List.Nil))))

    print(f"a initial rc count = ${Rc.strong_count(&a)}")

    let b = Rc.new(List.Cons(10, RefCell.new(Rc.clone(&a))))

    print(f"a rc count after b creation = ${Rc.strong_count(&a)}")
    print(f"b initial rc count = ${Rc.strong_count(&b)}")

    // Create a cycle: a points to b
    if let Some(link) = a.tail() {
        *link.borrow_mut() = Rc.clone(&b)
    }

    print(f"b rc count after changing a = ${Rc.strong_count(&b)}")
    print(f"a rc count after changing a = ${Rc.strong_count(&a)}")

    // Uncommenting the next line will overflow the stack:
    // print(f"a next item = ${a.tail()}")
}
```

```rust
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
enum List {
    Cons(i32, RefCell<Rc<List>>),
    Nil,
}

impl List {
    fn tail(&self) -> Option<&RefCell<Rc<List>>> {
        match self {
            Cons(_, item) => Some(item),
            Nil => None,
        }
    }
}

fn main() {
    let a = Rc::new(Cons(5, RefCell::new(Rc::new(Nil))));
    println!("a initial rc count = {}", Rc::strong_count(&a));
    let b = Rc::new(Cons(10, RefCell::new(Rc::clone(&a))));
    println!("a rc count after b creation = {}", Rc::strong_count(&a));
    println!("b initial rc count = {}", Rc::strong_count(&b));
    if let Some(link) = a.tail() {
        *link.borrow_mut() = Rc::clone(&b);
    }
    println!("b rc count after changing a = {}", Rc::strong_count(&b));
    println!("a rc count after changing a = {}", Rc::strong_count(&a));
}
```

</Listing>

The reference count of both `a` and `b` is 2 after we create the cycle. At the
end of `main`, the `Rc<List>` instances can't be dropped because their reference
counts never reach 0. The memory will remain uncollected.

### Preventing Reference Cycles with `Weak<T>`

You can create a _weak reference_ to the value within an `Rc<T>` by calling
`Rc::downgrade`. Weak references don't express an ownership relationship, and
their count doesn't affect when an `Rc<T>` instance is cleaned up.

<Listing number="15-15" file-name="src/main.at" caption="A tree structure using `Weak<T>` for parent references">

```auto
use.rust std::cell::RefCell
use.rust std::rc::{Rc, Weak}

type Node {
    value int
    parent RefCell<Weak<Node>>
    children RefCell<List<Rc<Node>>>
}

fn main() {
    let leaf = Rc.new(Node(
        value: 3,
        parent: RefCell.new(Weak.new()),
        children: RefCell.new(List.new())
    ))

    print(f"leaf parent = ${leaf.parent.borrow().upgrade()}")

    {
        let branch = Rc.new(Node(
            value: 5,
            parent: RefCell.new(Weak.new()),
            children: RefCell.new([Rc.clone(&leaf)])
        ))

        *leaf.parent.borrow_mut() = Rc.downgrade(&branch)

        print(f"branch strong = ${Rc.strong_count(&branch)}, weak = ${Rc.weak_count(&branch)}")
        print(f"leaf strong = ${Rc.strong_count(&leaf)}, weak = ${Rc.weak_count(&leaf)}")
    }

    print(f"leaf parent = ${leaf.parent.borrow().upgrade()}")
    print(f"leaf strong = ${Rc.strong_count(&leaf)}, weak = ${Rc.weak_count(&leaf)}")
}
```

```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

#[derive(Debug)]
struct Node {
    value: i32,
    parent: RefCell<Weak<Node>>,
    children: RefCell<Vec<Rc<Node>>>,
}

fn main() {
    let leaf = Rc::new(Node {
        value: 3,
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![]),
    });
    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());
    {
        let branch = Rc::new(Node {
            value: 5,
            parent: RefCell::new(Weak::new()),
            children: RefCell::new(vec![Rc::clone(&leaf)]),
        });
        *leaf.parent.borrow_mut() = Rc::downgrade(&branch);
        println!("branch strong = {}, weak = {}",
            Rc::strong_count(&branch), Rc::weak_count(&branch));
        println!("leaf strong = {}, weak = {}",
            Rc::strong_count(&leaf), Rc::weak_count(&leaf));
    }
    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());
    println!("leaf strong = {}, weak = {}",
        Rc::strong_count(&leaf), Rc::weak_count(&leaf));
}
```

</Listing>

When the inner scope ends, `branch` goes out of scope and the strong count of
the `Rc<Node>` decreases to 0, so its `Node` is dropped. The weak count of 1
from `leaf.parent` has no bearing on whether the `Node` is dropped, so we don't
get any memory leaks!

If we try to access the parent of `leaf` after the end of the scope, we'll get
`None` again. All of the logic that manages the counts and value dropping is
built into `Rc<T>` and `Weak<T>` and their implementations of the `Drop` spec.

## Smart Pointers Quick Reference

| Feature | Auto | Rust |
|---------|------|------|
| Heap allocation | `Box.new(v)` via `use.rust` | `Box::new(v)` |
| Reference counting | `Rc.new(v)` via `use.rust` | `Rc::new(v)` |
| Interior mutability | `RefCell.new(v)` via `use.rust` | `RefCell::new(v)` |
| Dereference spec | `spec Deref` | `impl Deref` |
| Cleanup spec | `spec Drop` | `impl Drop` |
| Weak reference | `Rc.downgrade(&v)` | `Rc::downgrade(&v)` |
| Shared + mutable | `Rc<RefCell<T>>` | `Rc<RefCell<T>>` |

## Summary

This chapter covered how to use smart pointers to make different guarantees and
trade-offs from those Auto makes by default with regular references:

1. **`Box<T>`** — heap allocation with single ownership, enables recursive types
2. **`Deref` spec** — treating smart pointers like regular references, with
   automatic deref coercion
3. **`Drop` spec** — running cleanup code automatically when values go out of
   scope
4. **`Rc<T>`** — reference counting for multiple owners of the same data
5. **`RefCell<T>`** — interior mutability with runtime borrow checking
6. **`Weak<T>`** — preventing reference cycles that can cause memory leaks

In the next chapter, we'll explore Auto's concurrency model, which uses the
actor pattern rather than Rust's thread-based model.

[ch4]: ch04-ownership.md
[ch16]: ch16-concurrency.md
[ch20]: ch20-advanced.md
