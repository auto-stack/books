# Classes and Objects

At this point we have defined classes and created objects that represent the time of day and the day of the year. And we've defined methods that create, modify, and perform computations with these objects.

In this chapter we'll continue our tour of object-oriented programming (OOP) by defining classes that represent geometric objects, including points, lines, and rectangles. We'll write methods that create and modify these objects.

We'll use these classes to demonstrate OOP topics including object identity and equivalence, shallow and deep copying, and polymorphism.

## Creating a Point

In computer graphics a location on the screen is often represented using a pair of coordinates in an `x`-`y` plane. By convention, the point `(0, 0)` usually represents the upper-left corner of the screen, and `(x, y)` represents the point `x` units to the right and `y` units down from the origin.

There are several ways we might represent a point in Auto:

- We can store the coordinates separately in two variables, `x` and `y`.

- We can store the coordinates as elements in a list or tuple.

- We can create a new type to represent points as objects.

In object-oriented programming, it would be most idiomatic to create a new type. To do that, we'll start with a class definition for `Point`.

```auto
type Point {
    x: float,
    y: float,
}

fn init(&self, x: float = 0.0, y: float = 0.0) {
    self.x = x
    self.y = y
}

fn to_string(&self) -> str {
    return f"Point({self.x}, {self.y})"
}
```

The `init` method takes the coordinates as parameters and assigns them to attributes `x` and `y`. The `to_string` method returns a string representation of the `Point`.

Now we can instantiate and display a `Point` object like this.

```auto
let start = Point(0.0, 0.0)
print(start)  // Point(0, 0)
```

As usual, a programmer-defined type is represented by a box with the name of the type outside and the attributes inside.

In general, programmer-defined types are mutable, so we can write a method like `translate` that takes two numbers, `dx` and `dy`, and adds them to the attributes `x` and `y`.

```auto
fn translate(&self, dx: float, dy: float) {
    self.x += dx
    self.y += dy
}
```

This method translates the `Point` from one location in the plane to another. It modifies the existing object in place.

## Creating a Line

Now let's define a class that represents the line segment between two points. As usual, we'll start with an `init` method and a `to_string` method.

```auto
type Line {
    p1: Point,
    p2: Point,
}

fn init(&self, p1: Point, p2: Point) {
    self.p1 = p1
    self.p2 = p2
}

fn to_string(&self) -> str {
    return f"Line({self.p1}, {self.p2})"
}
```

With those two methods, we can instantiate and display a `Line` object:

```auto
let line = Line(start, end)
print(line)  // Line(Point(0, 0), Point(300, 150))
```

When we call `print` and pass `line` as a parameter, `print` invokes `to_string` on `line`. The `to_string` method uses an f-string to create a string representation of the `line`.

The f-string contains two expressions in curly braces, `self.p1` and `self.p2`. When those expressions are evaluated, the results are `Point` objects. Then, when they are converted to strings, the `to_string` method from the `Point` class gets invoked.

That's why, when we display a `Line`, the result contains the string representations of the `Point` objects.

This is an example of **composition** -- a `Line` is composed of two `Point` objects. Composition is a way to combine simple objects into more complex ones.

<Listing number="16-1" file-name="point_line_classes.auto" caption="Point and Line classes with composition">

```auto
type Point {
    x: float,
    y: float,
}

fn init(&self, x: float = 0.0, y: float = 0.0) {
    self.x = x
    self.y = y
}

fn to_string(&self) -> str {
    return f"Point(${self.x}, ${self.y})"
}

fn __eq__(&self, other: Point) -> bool {
    return self.x == other.x and self.y == other.y
}

fn translate(&self, dx: float, dy: float) {
    self.x += dx
    self.y += dy
}

type Line {
    p1: Point,
    p2: Point,
}

fn init(&self, p1: Point, p2: Point) {
    self.p1 = p1
    self.p2 = p2
}

fn to_string(&self) -> str {
    return f"Line(${self.p1}, ${self.p2})"
}

fn __eq__(&self, other: Line) -> bool {
    return (self.p1 == other.p1 and self.p2 == other.p2) or
           (self.p1 == other.p2 and self.p2 == other.p1)
}

fn midpoint(&self) -> Point {
    let mx = (self.p1.x + self.p2.x) / 2.0
    let my = (self.p1.y + self.p2.y) / 2.0
    return Point(mx, my)
}

fn main() {
    // Creating Point objects
    let start = Point(0.0, 0.0)
    print(start)  // Point(0, 0)

    let end = Point(300.0, 150.0)
    print(end)    // Point(300, 150)

    // Equivalence vs identity
    let p1 = Point(200.0, 100.0)
    let p2 = Point(200.0, 100.0)
    print(p1 == p2)  // true  (equivalent)
    print(p1 is p2)  // false (different objects)

    // Translating a point
    end.translate(50.0, 25.0)
    print(end)  // Point(350, 175)

    // Composition: Line contains Point objects
    let line1 = Line(start, end)
    print(line1)  // Line(Point(0, 0), Point(350, 175))

    // Line equivalence (order-independent)
    let line2 = Line(end, start)
    print(line1 == line2)  // true

    // Midpoint of a line
    let mid = line1.midpoint()
    print(mid)  // Point(175, 87.5)
}
```

```python
class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return f"Line({self.p1}, {self.p2})"

    def __eq__(self, other):
        return ((self.p1 == other.p1 and self.p2 == other.p2) or
                (self.p1 == other.p2 and self.p2 == other.p1))

    def midpoint(self):
        mx = (self.p1.x + self.p2.x) / 2
        my = (self.p1.y + self.p2.y) / 2
        return Point(mx, my)


def main():
    # Creating Point objects
    start = Point(0.0, 0.0)
    print(start)  # Point(0.0, 0.0)

    end = Point(300.0, 150.0)
    print(end)    # Point(300.0, 150.0)

    # Equivalence vs identity
    p1 = Point(200.0, 100.0)
    p2 = Point(200.0, 100.0)
    print(p1 == p2)  # True  (equivalent)
    print(p1 is p2)  # False (different objects)

    # Translating a point
    end.translate(50.0, 25.0)
    print(end)  # Point(350.0, 175.0)

    # Composition: Line contains Point objects
    line1 = Line(start, end)
    print(line1)  # Line(Point(0.0, 0.0), Point(350.0, 175.0))

    # Line equivalence (order-independent)
    line2 = Line(end, start)
    print(line1 == line2)  # True

    # Midpoint of a line
    mid = line1.midpoint()
    print(mid)  # Point(175.0, 87.5)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The `Point` type has fields `x` and `y`, with an `init` constructor and `to_string` method. The `__eq__` method defines equivalence based on coordinates, and `translate` modifies the point in place. The `Line` type demonstrates **composition** -- it contains two `Point` objects as fields. The `__eq__` method for `Line` checks equivalence in either order (since a line from A to B is the same as a line from B to A). The `midpoint` method returns a new `Point` at the midpoint of the line.

## Equivalence and identity

Suppose we create two points with the same coordinates.

```auto
let p1 = Point(200.0, 100.0)
let p2 = Point(200.0, 100.0)
```

If we use the `==` operator to compare them, and we have defined `__eq__`, it checks whether the attributes are equal.

```auto
print(p1 == p2)  // true
```

But the `is` operator still indicates that they are different objects.

```auto
print(p1 is p2)  // false
```

It's not possible to override the `is` operator -- it always checks whether the objects are identical. But for programmer-defined types, you can override the `==` operator so it checks whether the objects are equivalent. And you can define what equivalent means.

## Creating a Rectangle

Now let's define a class that represents rectangles. To keep things simple, we'll assume that the rectangles are either vertical or horizontal, not at an angle.

What attributes should we use to specify the location and size of a rectangle? There are at least two possibilities:

- You could specify the width and height of the rectangle and the location of one corner.

- You could specify two opposing corners.

Let's implement the first one. Here is the class definition.

```auto
type Rectangle {
    width: float,
    height: float,
    corner: Point,
}

fn init(&self, width: float, height: float, corner: Point) {
    self.width = width
    self.height = height
    self.corner = corner
}

fn to_string(&self) -> str {
    return f"Rectangle({self.width}, {self.height}, {self.corner})"
}
```

The `Rectangle` type has three fields: `width`, `height`, and `corner`, where `corner` is a `Point` object. This is another example of composition.

Now we can instantiate a `Rectangle` object, using a `Point` as the location of the upper-left corner.

```auto
let corner = Point(30.0, 20.0)
let box = Rectangle(100.0, 50.0, corner)
print(box)  // Rectangle(100, 50, Point(30, 20))
```

## Changing rectangles

Now let's consider two methods that modify rectangles, `grow` and `translate`.

`grow` takes two numbers, `dwidth` and `dheight`, and adds them to the `width` and `height` attributes of the rectangle.

```auto
fn grow(&self, dwidth: float, dheight: float) {
    self.width += dwidth
    self.height += dheight
}
```

`translate` takes two numbers, `dx` and `dy`, and moves the rectangle the given distances in the `x` and `y` directions.

```auto
fn translate(&self, dx: float, dy: float) {
    self.corner.translate(dx, dy)
}
```

## Deep copy

When we use `copy` to duplicate a `Rectangle`, it copies the `Rectangle` object but not the `Point` object it contains. So the two `Rectangle` objects are different, as intended, but their `corner` attributes refer to the same object.

```auto
let box2 = copy(box1)
print(box1 is box2)                  // false
print(box1.corner is box2.corner)    // true (shared!)
```

What `copy` does is called a **shallow copy** because it copies the object but not the objects it contains. As a result, changing the `width` or `height` of one `Rectangle` does not affect the other, but changing the attributes of the shared `Point` affects both!

This behavior is confusing and error-prone. For example, if we translate `box2`, both rectangles appear to move:

```auto
box2.translate(30.0, 20.0)
print(box1)  // Rectangle(100, 50, Point(60, 40))  <-- bug!
```

Fortunately, Auto provides `deepcopy`, which copies not only the object but also the objects it refers to, and the objects *they* refer to, and so on. This operation is called a **deep copy**.

```auto
let box4 = deepcopy(box3)
print(box3.corner is box4.corner)  // false (independent!)
```

Because `box3` and `box4` are completely separate objects, we can modify one without affecting the other.

<Listing number="16-2" file-name="rectangle_deepcopy.auto" caption="Rectangle class with shallow and deep copy">

```auto
type Point {
    x: float,
    y: float,
}

fn init(&self, x: float = 0.0, y: float = 0.0) {
    self.x = x
    self.y = y
}

fn to_string(&self) -> str {
    return f"Point(${self.x}, ${self.y})"
}

fn __eq__(&self, other: Point) -> bool {
    return self.x == other.x and self.y == other.y
}

fn translate(&self, dx: float, dy: float) {
    self.x += dx
    self.y += dy
}

type Rectangle {
    width: float,
    height: float,
    corner: Point,
}

fn init(&self, width: float, height: float, corner: Point) {
    self.width = width
    self.height = height
    self.corner = corner
}

fn to_string(&self) -> str {
    return f"Rectangle(${self.width}, ${self.height}, ${self.corner})"
}

fn grow(&self, dwidth: float, dheight: float) {
    self.width += dwidth
    self.height += dheight
}

fn translate(&self, dx: float, dy: float) {
    self.corner.translate(dx, dy)
}

fn main() {
    // Creating a Rectangle with a Point as its corner
    let corner = Point(30.0, 20.0)
    let box1 = Rectangle(100.0, 50.0, corner)
    print(box1)  // Rectangle(100, 50, Point(30, 20))

    // Shallow copy -- corner is shared
    let box2 = copy(box1)
    print(box1 is box2)          // false
    print(box1.corner is box2.corner)  // true (shared!)

    // Growing box2 does not affect box1
    box2.grow(60.0, 40.0)
    print(box1)  // Rectangle(100, 50, Point(30, 20))
    print(box2)  // Rectangle(160, 90, Point(30, 20))

    // Translating box2 moves its corner, which is shared with box1!
    box2.translate(30.0, 20.0)
    print(box1)  // Rectangle(100, 50, Point(60, 40))  <-- bug!
    print(box2)  // Rectangle(160, 90, Point(60, 40))

    // Deep copy -- corner is independent
    let corner2 = Point(20.0, 20.0)
    let box3 = Rectangle(100.0, 50.0, corner2)
    let box4 = deepcopy(box3)
    print(box3.corner is box4.corner)  // false (independent!)

    box3.translate(50.0, 30.0)
    box4.grow(100.0, 60.0)
    print(box3)  // Rectangle(100, 50, Point(70, 50))
    print(box4)  // Rectangle(200, 110, Point(20, 20))
}
```

```python
from copy import copy, deepcopy


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy


class Rectangle:
    def __init__(self, width, height, corner):
        self.width = width
        self.height = height
        self.corner = corner

    def __str__(self):
        return f"Rectangle({self.width}, {self.height}, {self.corner})"

    def grow(self, dwidth, dheight):
        self.width += dwidth
        self.height += dheight

    def translate(self, dx, dy):
        self.corner.translate(dx, dy)


def main():
    # Creating a Rectangle with a Point as its corner
    corner = Point(30.0, 20.0)
    box1 = Rectangle(100.0, 50.0, corner)
    print(box1)  # Rectangle(100.0, 50.0, Point(30.0, 20.0))

    # Shallow copy -- corner is shared
    box2 = copy(box1)
    print(box1 is box2)                  # False
    print(box1.corner is box2.corner)    # True (shared!)

    # Growing box2 does not affect box1
    box2.grow(60.0, 40.0)
    print(box1)  # Rectangle(100.0, 50.0, Point(30.0, 20.0))
    print(box2)  # Rectangle(160.0, 90.0, Point(30.0, 20.0))

    # Translating box2 moves its corner, which is shared with box1!
    box2.translate(30.0, 20.0)
    print(box1)  # Rectangle(100.0, 50.0, Point(60.0, 40.0))  <-- bug!
    print(box2)  # Rectangle(160.0, 90.0, Point(60.0, 40.0))

    # Deep copy -- corner is independent
    corner2 = Point(20.0, 20.0)
    box3 = Rectangle(100.0, 50.0, corner2)
    box4 = deepcopy(box3)
    print(box3.corner is box4.corner)    # False (independent!)

    box3.translate(50.0, 30.0)
    box4.grow(100.0, 60.0)
    print(box3)  # Rectangle(100.0, 50.0, Point(70.0, 50.0))
    print(box4)  # Rectangle(200.0, 110.0, Point(20.0, 20.0))


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The `Rectangle` type demonstrates composition with `Point`. The `grow` method changes width and height, while `translate` delegates to the `Point`'s `translate` method. The critical lesson is the difference between `copy` (shallow copy) and `deepcopy`: a shallow copy shares nested objects, so modifying the shared `Point` affects both rectangles. A deep copy creates independent copies of all nested objects, making the two rectangles completely separate.

## Polymorphism

In the previous example, we worked with `Line` and `Rectangle` objects. We can do something more interesting by making a list of objects of different types that all provide a `draw` method, then looping through the list and invoking `draw` on each one.

```auto
let shapes = [line1, line2, box3, box4]

for shape in shapes {
    shape.draw()
}
```

The first and second time through the loop, `shape` refers to a `Line` object, so when `draw` is invoked, the method that runs is the one defined in the `Line` class.

The third and fourth time through the loop, `shape` refers to a `Rectangle` object, so when `draw` is invoked, the method that runs is the one defined in the `Rectangle` class.

In a sense, each object knows how to draw itself. This feature is called **polymorphism**. The word comes from Greek roots that mean "many shaped". In object-oriented programming, polymorphism is the ability of different types to provide the same methods, which makes it possible to perform many computations -- like drawing shapes -- by invoking the same method on different types of objects.

<Listing number="16-3" file-name="polymorphism_shapes.auto" caption="Polymorphism with different types and the same interface">

```auto
type Point {
    x: float,
    y: float,
}

fn init(&self, x: float = 0.0, y: float = 0.0) {
    self.x = x
    self.y = y
}

fn to_string(&self) -> str {
    return f"Point(${self.x}, ${self.y})"
}

type Line {
    p1: Point,
    p2: Point,
}

fn init(&self, p1: Point, p2: Point) {
    self.p1 = p1
    self.p2 = p2
}

fn to_string(&self) -> str {
    return f"Line(${self.p1}, ${self.p2})"
}

fn draw(&self) {
    print(f"Drawing line from (${self.p1.x}, ${self.p1.y}) to (${self.p2.x}, ${self.p2.y})")
}

type Rectangle {
    width: float,
    height: float,
    corner: Point,
}

fn init(&self, width: float, height: float, corner: Point) {
    self.width = width
    self.height = height
    self.corner = corner
}

fn to_string(&self) -> str {
    return f"Rectangle(${self.width}, ${self.height}, ${self.corner})"
}

fn draw(&self) {
    let p1 = self.corner
    let p2 = Point(self.corner.x + self.width, self.corner.y)
    let p3 = Point(self.corner.x + self.width, self.corner.y + self.height)
    let p4 = Point(self.corner.x, self.corner.y + self.height)
    print(f"Drawing rectangle with corners (${p1.x},${p1.y}), (${p2.x},${p2.y}), (${p3.x},${p3.y}), (${p4.x},${p4.y})")
}

type Circle {
    center: Point,
    radius: float,
}

fn init(&self, center: Point, radius: float) {
    self.center = center
    self.radius = radius
}

fn to_string(&self) -> str {
    return f"Circle(center=${self.center}, radius=${self.radius})"
}

fn draw(&self) {
    print(f"Drawing circle at (${self.center.x}, ${self.center.y}) with radius ${self.radius}")
}

fn draw_shapes(shapes: list) {
    for shape in shapes {
        shape.draw()
    }
}

fn main() {
    let origin = Point(0.0, 0.0)
    let line1 = Line(origin, Point(300.0, 0.0))
    let line2 = Line(origin, Point(0.0, 150.0))
    let rect = Rectangle(100.0, 50.0, Point(30.0, 20.0))
    let circle = Circle(Point(80.0, 45.0), 25.0)

    // Polymorphism: same interface, different types
    let shapes = [line1, line2, rect, circle]
    draw_shapes(shapes)
    // Drawing line from (0, 0) to (300, 0)
    // Drawing line from (0, 0) to (0, 150)
    // Drawing rectangle with corners (30,20), (130,20), (130,70), (30,70)
    // Drawing circle at (80, 45) with radius 25
}
```

```python
class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return f"Line({self.p1}, {self.p2})"

    def draw(self):
        print(f"Drawing line from ({self.p1.x}, {self.p1.y}) to ({self.p2.x}, {self.p2.y})")


class Rectangle:
    def __init__(self, width, height, corner):
        self.width = width
        self.height = height
        self.corner = corner

    def __str__(self):
        return f"Rectangle({self.width}, {self.height}, {self.corner})"

    def draw(self):
        p1 = self.corner
        p2 = Point(self.corner.x + self.width, self.corner.y)
        p3 = Point(self.corner.x + self.width, self.corner.y + self.height)
        p4 = Point(self.corner.x, self.corner.y + self.height)
        print(f"Drawing rectangle with corners ({p1.x},{p1.y}), ({p2.x},{p2.y}), ({p3.x},{p3.y}), ({p4.x},{p4.y})")


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __str__(self):
        return f"Circle(center={self.center}, radius={self.radius})"

    def draw(self):
        print(f"Drawing circle at ({self.center.x}, {self.center.y}) with radius {self.radius}")


def draw_shapes(shapes):
    for shape in shapes:
        shape.draw()


def main():
    origin = Point(0.0, 0.0)
    line1 = Line(origin, Point(300.0, 0.0))
    line2 = Line(origin, Point(0.0, 150.0))
    rect = Rectangle(100.0, 50.0, Point(30.0, 20.0))
    circle = Circle(Point(80.0, 45.0), 25.0)

    # Polymorphism: same interface, different types
    shapes = [line1, line2, rect, circle]
    draw_shapes(shapes)
    # Drawing line from (0.0, 0.0) to (300.0, 0.0)
    # Drawing line from (0.0, 0.0) to (0.0, 150.0)
    # Drawing rectangle with corners (30.0,20.0), (130.0,20.0), (130.0,70.0), (30.0,70.0)
    # Drawing circle at (80.0, 45.0) with radius 25.0


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

Polymorphism is demonstrated by putting `Line`, `Rectangle`, and `Circle` objects into a single list and calling `draw()` on each one. Even though the objects are different types, they all provide a `draw` method. When `shape.draw()` is called in the loop, Auto dispatches to the correct method based on the actual type of the object. The `draw_shapes` function doesn't need to know what types are in the list -- it just calls `draw()` and each object handles its own drawing.

> **Note for Python Programmers:**
>
> Auto's polymorphism works the same way as Python's. Both languages use dynamic dispatch to call the correct method based on the object's type at runtime.

## Debugging

In this chapter, we ran into a subtle bug that happened because we created a `Point` that was shared by two `Rectangle` objects, and then we modified the `Point`.

In general, there are two ways to avoid problems like this: you can avoid sharing objects or you can avoid modifying them.

To avoid sharing objects, you can use deep copy, as we did in this chapter.

To avoid modifying objects, consider replacing impure functions like `translate` with pure functions that create new objects. For example, here's a version of `translated` that creates a new `Point` and never modifies its attributes.

```auto
fn translated(&self, dx: float = 0.0, dy: float = 0.0) -> Point {
    return Point(self.x + dx, self.y + dy)
}
```

Creating a new object takes more time than modifying an existing one, but the difference seldom matters in practice. Programs that avoid shared objects and impure functions are often easier to develop, test, and debug -- and the best kind of debugging is the kind you don't have to do.

## Glossary

**shallow copy:**
A copy operation that does not copy nested objects.

**deep copy:**
A copy operation that also copies nested objects.

**composition:**
The ability to define a type that contains objects of other types as fields.

**polymorphism:**
The ability of a method or operator to work with multiple types of objects.

## Exercises

### Exercise

Write a `__eq__` method for the `Line` class that returns `true` if the `Line` objects refer to `Point` objects that are equivalent, in either order.

### Exercise

Write a `Line` method called `midpoint` that computes the midpoint of a line segment and returns the result as a `Point` object.

### Exercise

Write a `Rectangle` method called `midpoint` that finds the point in the center of a rectangle and returns the result as a `Point` object.

### Exercise

Write a definition for a class named `Circle` with attributes `center` and `radius`, where `center` is a Point object and `radius` is a number. Include `init`, `to_string`, and a `draw` method. Then demonstrate polymorphism by adding the `Circle` to a list of shapes and drawing them all.
