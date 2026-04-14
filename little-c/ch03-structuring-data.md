# Structuring Data

This chapter covers how Auto structures data using types, enums, and specs, and
how these map to C's structs, unions, typedefs, and function pointer patterns.
You will build real data structures and see how Auto's design prevents common
errors.

## 31. Structures

C uses `struct` to group related fields:

```c
struct Point {
    int x;
    int y;
};
struct Point p = {3, 4};
```

Auto uses `type` to define structures. Fields are comma-separated and the
constructor uses named initialization:

<Listing name="structures" file="listings/ch03/listing-03-01">

```auto
type Point {
    x int
    y int
}

fn Point.modulus() float {
    float(self.x * self.x + self.y * self.y)
}

fn main() {
    let p Point = Point(3, 4)
    print("Point: (", p.x, ",", p.y, ")")
    print("Modulus:", p.modulus())
}
```

</Listing>

Auto's `Point(3, 4)` transpiles to C's `(struct Point){.x = 3, .y = 4}` using
designated initializers. Methods like `Point.modulus()` become standalone
functions `Point_Modulus(struct Point *self)` in C.

## 32. Unions

C unions allow different types to share the same memory:

```c
union Value {
    int i;
    float f;
};
```

Plain C unions are unsafe — there is no tag to tell which variant is active.
Auto's `enum` creates tagged unions that carry both a tag and a value:

<Listing name="unions" file="listings/ch03/listing-03-02">

```auto
enum Shape {
    Circle float
    Rect float, float
    Triangle float, float, float
}

fn area(s Shape) float {
    is s {
        Circle(r) => 3.14159 * r * r
        Rect(w, h) => w * h
        Triangle(a, b, c) => {
            let s float = (a + b + c) / 2.0
            (s * (s - a) * (s - b) * (s - c)) ** 0.5
        }
    }
}

fn main() {
    let c Shape = Shape.Circle(5.0)
    let r Shape = Shape.Rect(3.0, 4.0)
    print("Circle area:", area(c))
    print("Rect area:", area(r))
}
```

</Listing>

In C, `enum Shape` becomes a struct with a `tag` field and a `union as` field.
The `is` expression transpiles to a `switch` on the tag.

## 33. Typedef vs Auto type

C uses `typedef` to create type aliases:

```c
typedef int UserId;
typedef float Score;
```

Auto's `type` with a single field creates the same effect without the `typedef`
keyword:

<Listing name="typedef" file="listings/ch03/listing-03-03">

```auto
type UserId int
type Score float

fn make_user(id int, score float) {
    let uid UserId = UserId(id)
    let s Score = Score(score)
    print("User ID:", uid)
    print("Score:", s)
}

fn main() {
    make_user(1, 95.5)
}
```

</Listing>

Auto's wrapper types are more expressive than C's `typedef` because they create
distinct types — you cannot accidentally pass a `UserId` where a plain `int` is
expected.

## 34. Bitfields

C allows specifying the bit width of struct fields:

```c
struct Flags {
    unsigned int is_active : 1;
    unsigned int priority : 3;
};
```

Bitfields are a C-only feature for memory-constrained environments. Auto does
not provide bitfields. Use `bool` and `int` fields instead; the compiler
optimizes when possible.

## 35. Enumerations

C `enum` assigns integer constants:

```c
enum Color { RED, GREEN, BLUE };
enum Color c = GREEN;
```

Auto's `enum` (without payload) maps to C's `enum` with a `NAME_VARIANT` prefix
to avoid name collisions:

```auto
enum Color { RED, GREEN, BLUE }
```

becomes:

```c
enum Color { COLOR_RED, COLOR_GREEN, COLOR_BLUE };
```

## 36. Linked Lists

Linked lists are a fundamental data structure. Each node holds a value and a
reference to the next node. Auto's `?T` optional type naturally represents the
"next or nothing" link.

<Listing name="linked-list" file="listings/ch03/listing-03-04">

```auto
type Node {
    value int
    next ?Node
}

fn new_node(val int) Node {
    Node(val, nil)
}

fn print_list(head ?Node) {
    var current ?Node = head
    while current != nil {
        print(current.value)
        current = current.next
    }
}

fn main() {
    let a Node = new_node(1)
    let b Node = new_node(2)
    let c Node = new_node(3)
    a.next = b
    b.next = c
    print("Linked list:")
    print_list(a)
}
```

</Listing>

In C, `?Node` becomes `struct Node*` (a nullable pointer). The `nil` literal
maps to `NULL`.

## 37. Stacks and Queues

A stack is a last-in, first-out (LIFO) data structure. Implement it with an
array and a top index.

<Listing name="stack" file="listings/ch03/listing-03-05">

```auto
type Stack {
    items [100]int
    top int
}

fn Stack.new() Stack {
    Stack([100]int{}, 0)
}

fn Stack.push(s Stack, val int) {
    s.items[s.top] = val
    s.top = s.top + 1
}

fn Stack.pop(s Stack) int {
    s.top = s.top - 1
    s.items[s.top]
}

fn main() {
    var s Stack = Stack.new()
    s.push(s, 10)
    s.push(s, 20)
    s.push(s, 30)
    print("Popped:", s.pop(s))
    print("Popped:", s.pop(s))
    print("Top:", s.top)
}
```

</Listing>

A queue would use two indices (front and rear) or a ring buffer. The principle
is the same: wrap an array in a `type` and provide `push`/`pop` methods.

## 38. Hash Tables

A simple hash table uses an array of buckets and a hash function. In C, you
would use function pointers for the hash and equality strategies. In Auto, the
`spec` system provides this cleanly:

```auto
spec Hasher {
    fn hash(key str) int
}
```

Each bucket can be a linked list (for collision chaining). The full
implementation is beyond this chapter's scope, but the pattern follows the
same `spec` + `type` approach used in Chapter 2 for function pointers.

## 39. OOP in C and Auto's spec/type

C does not have classes, but you can simulate object-oriented programming with
structs and function pointers. Auto's `spec` and `type` system makes this
idiomatic and type-safe.

<Listing name="oop" file="listings/ch03/listing-03-06">

```auto
spec Drawable {
    fn draw()
}

type CircleObj {
    radius float
}

fn CircleObj.draw() {
    print("Drawing circle with radius:", self.radius)
}

type SquareObj {
    side float
}

fn SquareObj.draw() {
    print("Drawing square with side:", self.side)
}

fn render(d Drawable) {
    d.draw()
}

fn main() {
    let c CircleObj = CircleObj(5.0)
    let s SquareObj = SquareObj(3.0)
    render(c)
    render(s)
}
```

</Listing>

The `spec Drawable` generates a vtable struct in C with function pointers.
Each implementing type (`CircleObj`, `SquareObj`) gets a vtable instance and
concrete method functions.

## 40. Practice: Library System

Build a small library management system using types, methods, and state
management.

<Listing name="library" file="listings/ch03/listing-03-07">

```auto
type Book {
    title str
    author str
    available bool
}

fn Book.new(title str, author str) Book {
    Book(title, author, true)
}

fn Book.borrow(b Book) {
    if b.available {
        b.available = false
        print("Borrowed:", b.title)
    } else {
        print("Not available:", b.title)
    }
}

fn Book.return_book(b Book) {
    b.available = true
    print("Returned:", b.title)
}

fn main() {
    let b1 Book = Book.new("The C Programming Language", "K&R")
    let b2 Book = Book.new("Auto Programming", "Auto Team")
    b1.borrow(b1)
    b1.borrow(b1)
    b1.return_book(b1)
    b1.borrow(b1)
}
```

</Listing>

This exercise combines `type` definitions, methods, state mutation, and
conditional logic — all the concepts from this chapter.

## Quick Reference

| Concept | Auto | C |
|---------|------|---|
| Structure | `type Name { fields }` | `struct Name { fields };` |
| Constructor | `Name(v1, v2)` | `(struct Name){.f1=v1, .f2=v2}` |
| Method | `fn Name.method()` | `void Name_method(struct Name *self)` |
| Tagged union | `enum Tag { Variant fields }` | `struct Tag { tag; union as; }` |
| Type alias | `type Name BaseType` | `typedef BaseType Name;` |
| Enumeration | `enum Color { RED }` | `enum Color { COLOR_RED };` |
| Optional | `?T` | `T*` (nullable) |
| Linked list node | `type Node { val, ?Node }` | `struct Node { val; Node* next; }` |
| Interface | `spec Name { fn ... }` | vtable with function pointers |
| Implementation | `type Foo as Spec { }` | vtable instance + methods |
| Null | `nil` | `NULL` |
| Field access | `self.field` | `self->field` |
