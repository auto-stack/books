# Classes and Functions

At this point you know how to use functions to organize code and how to use built-in types to organize data. The next step is **object-oriented programming**, which uses programmer-defined types to organize both code and data.

Object-oriented programming is a big topic, so we will proceed gradually. In this chapter, we'll start with code that is not idiomatic -- that is, it is not the kind of code experienced programmers write -- but it is a good place to start. In the next two chapters, we will use additional features to write more idiomatic code.

## Programmer-defined types

We have used many of Auto's built-in types -- now we will define a new type. As a first example, we'll create a type called `Time` that represents a time of day. A programmer-defined type is also called a **class**.

In Auto, a type definition specifies the fields an object contains:

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}
```

The header indicates that the new type is called `Time`. The body lists three fields: `hour`, `minute`, and `second`. Defining a type creates a **class object**.

The class object is like a factory for creating objects. To create a `Time` object, you call `Time` with field values:

```auto
let lunch = Time{hour: 11, minute: 59, second: 1}
```

The result is a new object whose type is `Time`.

Creating a new object is called **instantiation**, and the object is an **instance** of the class.

## Attributes

An object contains variables, which are called **attributes**. In Auto, attributes are defined as part of the type declaration and accessed using dot notation:

```auto
print(lunch.hour)   // 11
print(lunch.minute) // 59
print(lunch.second) // 1
```

You can use an attribute as part of any expression:

```auto
let total_minutes = lunch.hour * 60 + lunch.minute
print(total_minutes)  // 719
```

And you can use the dot operator in an f-string:

```auto
print(f"{lunch.hour:02d}:{lunch.minute:02d}:{lunch.second:02d}")  // 11:59:01
```

The format specifiers `:02d` indicate that `minute` and `second` should be displayed with at least two digits and a leading zero if needed.

We can write a function that displays a `Time` object:

```auto
fn print_time(time: Time) {
    let s = f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}"
    print(s)
}
```

When we call it, we can pass `lunch` as an argument:

```auto
print_time(lunch)  // 11:59:01
```

## Objects as return values

Functions can return objects. For example, `make_time` takes parameters, stores them as fields in a `Time` object, and returns the new object:

```auto
fn make_time(hour: int, minute: int, second: int) -> Time {
    return Time{hour: hour, minute: minute, second: second}
}
```

Here's how we use `make_time` to create a `Time` object:

```auto
let time = make_time(11, 59, 1)
print_time(time)  // 11:59:01
```

<Listing number="14-1" file-name="defining_a_type.auto" caption="Defining a type and using attributes">

```auto
type Point {
    x: float,
    y: float,
}

fn print_point(p: Point) {
    print(f"({p.x}, {p.y})")
}

fn main() {
    // Creating a Point type and instantiating
    let lunch = Point{x: 0.0, y: 0.0}
    print(type(lunch))  // Point

    // Assigning attributes
    lunch.x = 11.0
    lunch.y = 59.0
    print_point(lunch)  // (11, 59)

    // Reading attributes
    print(lunch.x)  // 11.0

    // Using attributes in expressions
    let total_minutes = lunch.x * 60.0 + lunch.y
    print("Total minutes:", total_minutes)  // 719.0

    // Creating another Point
    let p = Point{x: 3.0, y: 4.0}
    print_point(p)  // (3, 4)

    // Distance from origin
    let distance = (p.x ** 2.0 + p.y ** 2.0) ** 0.5
    print("Distance:", distance)  // 5.0
}
```

```python
class Point:
    pass


def print_point(p):
    print(f"({p.x}, {p.y})")


def main():
    # Creating a Point type and instantiating
    lunch = Point()
    print(type(lunch))  # <class '__main__.Point'>

    # Assigning attributes
    lunch.x = 11.0
    lunch.y = 59.0
    print_point(lunch)  # (11.0, 59.0)

    # Reading attributes
    print(lunch.x)  # 11.0

    # Using attributes in expressions
    total_minutes = lunch.x * 60.0 + lunch.y
    print(f"Total minutes: {total_minutes}")  # 719.0

    # Creating another Point
    p = Point()
    p.x = 3.0
    p.y = 4.0
    print_point(p)  # (3.0, 4.0)

    # Distance from origin
    distance = (p.x ** 2 + p.y ** 2) ** 0.5
    print(f"Distance: {distance}")  # 5.0


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The `type` keyword defines a new struct-like type with named fields. In Auto, `type Point { x: float, y: float }` declares a `Point` type with two float fields. Objects are created using the `Point{x: ..., y: ...}` constructor syntax, and fields are accessed with dot notation (`p.x`, `p.y`).

In Python, the equivalent is a bare `class Point: pass`, with attributes assigned dynamically after instantiation. Auto's type declaration makes the structure explicit upfront.

## Objects are mutable

Suppose you are going to a screening of a movie that starts at 9:20 PM and runs for 92 minutes (one hour 32 minutes). What time will the movie end?

First, we'll create a `Time` object that represents the start time:

```auto
let mut start = make_time(9, 20, 0)
print_time(start)  // 09:20:00
```

To find the end time, we can modify the fields of the `Time` object, adding the duration of the movie:

```auto
start.hour += 1
start.minute += 32
print_time(start)  // 10:52:00
```

We can encapsulate this in a function:

```auto
fn increment_time(time: Time, hours: int, minutes: int, seconds: int) {
    time.hour += hours
    time.minute += minutes
    time.second += seconds
}
```

```auto
let mut start = make_time(9, 20, 0)
increment_time(start, 1, 32, 0)
print_time(start)  // 10:52:00
```

Inside the function, `time` is an alias for `start`, so when `time` is modified, `start` changes.

This function works, but after it runs, we're left with a variable named `start` that refers to an object that represents the *end* time, and we no longer have an object that represents the start time. It would be better to leave `start` unchanged and make a new object to represent the end time.

## Copying

In Python, the `copy` module provides a function that can duplicate any object. In Auto, you can create a new object with the same values:

```auto
let end = Time{hour: start.hour, minute: start.minute, second: start.second}
```

Now `start` and `end` contain the same data, but they are different objects.

A **shallow copy** duplicates the object itself, but if it contains references to other objects, those references are shared. A **deep copy** duplicates the object and everything it refers to. In most cases with simple types like `Time`, a shallow copy is sufficient.

## Objects as return values

Functions can return objects, which makes it easy to compose operations. For example, here's a function that creates a `Rectangle` type with a `Point` as one of its fields:

```auto
type Point {
    x: float,
    y: float,
}

type Rectangle {
    corner: Point,
    width: float,
    height: float,
}
```

A function like `find_center` can take a `Rectangle` and return a `Point`:

```auto
fn find_center(box: Rectangle) -> Point {
    let cx = box.corner.x + box.width / 2.0
    let cy = box.corner.y + box.height / 2.0
    return Point{x: cx, y: cy}
}
```

<Listing number="14-2" file-name="objects_as_return_values.auto" caption="Functions that create and return objects">

```auto
type Rectangle {
    corner: Point,
    width: float,
    height: float,
}

type Point {
    x: float,
    y: float,
}

fn print_point(p: Point) {
    print(f"({p.x}, {p.y})")
}

fn print_rect(box: Rectangle) {
    print("Corner:", box.corner)
    print(f"Width: {box.width}, Height: {box.height}")
}

fn find_center(box: Rectangle) -> Point {
    let cx = box.corner.x + box.width / 2.0
    let cy = box.corner.y + box.height / 2.0
    return Point{x: cx, y: cy}
}

fn grow_rectangle(box: Rectangle, dwidth: float, dheight: float) -> Rectangle {
    return Rectangle{
        corner: box.corner,
        width: box.width + dwidth,
        height: box.height + dheight,
    }
}

fn main() {
    // Creating a Point
    let origin = Point{x: 0.0, y: 0.0}

    // Creating a Rectangle (objects as fields)
    let box = Rectangle{corner: origin, width: 100.0, height: 200.0}
    print_rect(box)

    // Function returning an object
    let center = find_center(box)
    print("Center:")
    print_point(center)  // (50, 100)

    // Growing the rectangle returns a new object
    let grown = grow_rectangle(box, 50.0, 100.0)
    print_rect(grown)

    // Original is unchanged
    print_rect(box)
}
```

```python
class Point:
    pass


class Rectangle:
    pass


def print_point(p):
    print(f"({p.x}, {p.y})")


def print_rect(box):
    print(f"Corner: ({box.corner.x}, {box.corner.y})")
    print(f"Width: {box.width}, Height: {box.height}")


def find_center(box):
    cx = box.corner.x + box.width / 2
    cy = box.corner.y + box.height / 2
    result = Point()
    result.x = cx
    result.y = cy
    return result


def grow_rectangle(box, dwidth, dheight):
    result = Rectangle()
    result.corner = box.corner
    result.width = box.width + dwidth
    result.height = box.height + dheight
    return result


def main():
    # Creating a Point
    origin = Point()
    origin.x = 0.0
    origin.y = 0.0

    # Creating a Rectangle (objects as fields)
    box = Rectangle()
    box.corner = origin
    box.width = 100.0
    box.height = 200.0
    print_rect(box)

    # Function returning an object
    center = find_center(box)
    print("Center:")
    print_point(center)  # (50.0, 100.0)

    # Growing the rectangle returns a new object
    grown = grow_rectangle(box, 50.0, 100.0)
    print_rect(grown)

    # Original is unchanged
    print_rect(box)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

Objects can contain other objects as fields. The `Rectangle` type has a `corner` field of type `Point`. Functions can return new objects -- `find_center` computes and returns a new `Point`, while `grow_rectangle` returns a new `Rectangle` with modified dimensions.

This pattern of creating and returning new objects (rather than modifying existing ones) is the basis of **pure functions**.

## Pure functions

We can write pure functions that don't modify their parameters. A **pure function** does not modify any of the objects passed to it as arguments, and its only effect is to return a value.

For example, here's a function that converts a `Time` to an integer (seconds since midnight) and back:

```auto
fn time_to_int(time: Time) -> int {
    let minutes = time.hour * 60 + time.minute
    let seconds = minutes * 60 + time.second
    return seconds
}

fn int_to_time(seconds: int) -> Time {
    let (minute, second) = divmod(seconds, 60)
    let (hour, minute) = divmod(minute, 60)
    return make_time(hour, minute, second)
}
```

Using these conversion functions, we can write a concise `add_time`:

```auto
fn add_time(time: Time, hours: int, minutes: int, seconds: int) -> Time {
    let duration = make_time(hours, minutes, seconds)
    let total_seconds = time_to_int(time) + time_to_int(duration)
    return int_to_time(total_seconds)
}
```

The first line converts the arguments to a `Time` object. The second line converts both to seconds and adds them. The third line converts the sum back to a `Time` and returns it.

```auto
let start = make_time(9, 40, 0)
let end = add_time(start, 1, 32, 0)
print_time(start)  // 09:40:00  -- unchanged!
print_time(end)    // 11:12:00
```

Anything that can be done with impure functions (modifiers) can also be done with pure functions. Programs that use pure functions might be less error-prone, but impure functions are sometimes convenient and can be more efficient. In general, write pure functions whenever it is reasonable. This approach might be called a **functional programming style**.

<Listing number="14-3" file-name="pure_functions_vs_modifiers.auto" caption="Pure functions compared to modifiers">

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}

fn print_time(time: Time) {
    print(f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}")
}

fn make_time(hour: int, minute: int, second: int) -> Time {
    return Time{hour: hour, minute: minute, second: second}
}

fn time_to_int(time: Time) -> int {
    let minutes = time.hour * 60 + time.minute
    let seconds = minutes * 60 + time.second
    return seconds
}

fn int_to_time(seconds: int) -> Time {
    let (minute, second) = divmod(seconds, 60)
    let (hour, minute) = divmod(minute, 60)
    return make_time(hour, minute, second)
}

// Modifier: changes the object in place
fn increment_time(time: Time, hours: int, minutes: int, seconds: int) {
    time.hour += hours
    time.minute += minutes
    time.second += seconds
    let (carry, time.second) = divmod(time.second, 60)
    let (carry, time.minute) = divmod(time.minute + carry, 60)
    let (_, time.hour) = divmod(time.hour + carry, 24)
}

// Pure function: does not modify the original
fn add_time(time: Time, hours: int, minutes: int, seconds: int) -> Time {
    let duration = make_time(hours, minutes, seconds)
    let total_seconds = time_to_int(time) + time_to_int(duration)
    return int_to_time(total_seconds)
}

fn main() {
    // --- Modifier approach ---
    let mut start = make_time(9, 40, 0)
    print("Start (modifier):", end = " ")
    print_time(start)  // 09:40:00

    increment_time(start, 1, 32, 0)
    print("After increment: ", end = " ")
    print_time(start)  // 11:12:00
    // Note: start has been changed!

    // --- Pure function approach ---
    let fresh = make_time(9, 40, 0)
    let end = add_time(fresh, 1, 32, 0)
    print("Start (pure):    ", end = " ")
    print_time(fresh)  // 09:40:00  -- unchanged!
    print("End (pure):      ", end = " ")
    print_time(end)    // 11:12:00

    // Pure function with large values
    let end2 = add_time(fresh, 0, 90, 120)
    print("End (+90m +120s):", end = " ")
    print_time(end2)   // 11:12:00

    // Convert to/from int
    let t = make_time(1, 1, 1)
    let secs = time_to_int(t)
    print("01:01:01 =", secs, "seconds")  // 3661 seconds
    let back = int_to_time(secs)
    print_time(back)  // 01:01:01
}
```

```python
class Time:
    pass


def print_time(time):
    s = f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}"
    print(s)


def make_time(hour, minute, second):
    time = Time()
    time.hour = hour
    time.minute = minute
    time.second = second
    return time


def time_to_int(time):
    minutes = time.hour * 60 + time.minute
    seconds = minutes * 60 + time.second
    return seconds


def int_to_time(seconds):
    minute, second = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    return make_time(hour, minute, second)


# Modifier: changes the object in place
def increment_time(time, hours, minutes, seconds):
    time.hour += hours
    time.minute += minutes
    time.second += seconds
    carry, time.second = divmod(time.second, 60)
    carry, time.minute = divmod(time.minute + carry, 60)
    _, time.hour = divmod(time.hour + carry, 24)


# Pure function: does not modify the original
def add_time(time, hours, minutes, seconds):
    duration = make_time(hours, minutes, seconds)
    total_seconds = time_to_int(time) + time_to_int(duration)
    return int_to_time(total_seconds)


def main():
    # --- Modifier approach ---
    start = make_time(9, 40, 0)
    print("Start (modifier): ", end="")
    print_time(start)  # 09:40:00

    increment_time(start, 1, 32, 0)
    print("After increment:  ", end="")
    print_time(start)  # 11:12:00
    # Note: start has been changed!

    # --- Pure function approach ---
    fresh = make_time(9, 40, 0)
    end = add_time(fresh, 1, 32, 0)
    print("Start (pure):     ", end="")
    print_time(fresh)  # 09:40:00  -- unchanged!
    print("End (pure):       ", end="")
    print_time(end)  # 11:12:00

    # Pure function with large values
    end2 = add_time(fresh, 0, 90, 120)
    print("End (+90m +120s): ", end="")
    print_time(end2)  # 11:12:00

    # Convert to/from int
    t = make_time(1, 1, 1)
    secs = time_to_int(t)
    print(f"01:01:01 = {secs} seconds")  # 3661 seconds
    back = int_to_time(secs)
    print_time(back)  # 01:01:01


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The modifier `increment_time` changes the `Time` object in place -- after calling it, the original variable now holds a different value. The pure function `add_time` creates and returns a new `Time` object, leaving the original unchanged.

The conversion functions `time_to_int` and `int_to_time` provide a clean way to perform arithmetic on time values by converting to an integer representation (seconds since midnight), doing the math, and converting back. This avoids the complexity of handling carry between hours, minutes, and seconds manually.

## Prototype and patch

In the previous example, `increment_time` and `add_time` seem to work, but if we try another example, we'll see that they are not quite correct. Suppose the movie starts at 9:40, not 9:20:

```auto
let start = make_time(9, 40, 0)
let end = add_time(start, 1, 32, 0)
print_time(end)  // 11:12:00  -- correct!
```

But what if the duration is 92 minutes rather than 1 hour and 32 minutes?

```auto
let end = add_time(start, 0, 92, 0)
```

Without proper handling, the result is not a valid time. The insight is to use `divmod` to handle carry correctly:

```auto
fn increment_time(time: Time, hours: int, minutes: int, seconds: int) {
    time.hour += hours
    time.minute += minutes
    time.second += seconds
    let (carry, time.second) = divmod(time.second, 60)
    let (carry, time.minute) = divmod(time.minute + carry, 60)
    let (_, time.hour) = divmod(time.hour + carry, 24)
}
```

This section demonstrates a development plan called **prototype and patch** -- start with a simple prototype that works for the first example, test with more difficult examples, and fix errors as you find them. This approach can be effective, but incremental corrections can generate code that is unnecessarily complicated.

## Design-first development

An alternative plan is **design-first development**, which involves more planning before prototyping. In a design-first process, a high-level insight into the problem can make the programming much easier.

In this case, the insight is that we can think of a `Time` object as a three-digit number in base 60 (sexagesimal). The `second` field is the "ones column", the `minute` field is the "sixties column", and the `hour` field is the "thirty-six hundreds column".

This observation suggests converting `Time` objects to integers and taking advantage of the fact that Auto knows how to do integer arithmetic. The functions `time_to_int` and `int_to_time` shown in the previous section implement this approach.

Ironically, sometimes making a problem harder -- or more general -- makes it easier, because there are fewer special cases and fewer opportunities for error.

## Debugging

Auto provides several built-in functions that are useful for testing and debugging programs that work with objects. For example, you can check the type of an object:

```auto
print(type(start))  // Time
```

You can also use `isinstance` to check whether an object is an instance of a particular type:

```auto
print(isinstance(end, Time))  // true
```

To get all of the fields and their values, you can use `vars`:

```auto
print(vars(start))  // {hour: 9, minute: 40, second: 0}
```

## Glossary

**object-oriented programming:**
A style of programming that uses objects to organize code and data.

**class:**
A programmer-defined type. A class definition creates a new class object.

**class object:**
An object that represents a class -- it is the result of a type definition.

**instantiation:**
The process of creating an object that belongs to a class.

**instance:**
An object that belongs to a class.

**attribute:**
A variable associated with an object, also called an instance variable. In Auto, attributes are declared as fields in a type definition.

**format specifier:**
In an f-string, a format specifier determines how a value is converted to a string.

**pure function:**
A function that does not modify its parameters or have any effect other than returning a value.

**functional programming style:**
A way of programming that uses pure functions whenever possible.

**prototype and patch:**
A way of developing programs by starting with a rough draft and gradually adding features and fixing bugs.

**design-first development:**
A way of developing programs with more careful planning than prototype and patch.

## Exercises

### Exercise

Write a function called `subtract_time` that takes two `Time` objects and returns the interval between them in seconds -- assuming that they are two times during the same day.

### Exercise

Write a function called `is_after` that takes two `Time` objects and returns `true` if the first time is later in the day than the second, and `false` otherwise.

### Exercise

Here's a definition for a `Date` type that represents a date -- that is, a year, month, and day of the month.

```auto
type Date {
    year: int,
    month: int,
    day: int,
}
```

1. Write a function called `make_date` that takes `year`, `month`, and `day` as parameters and returns a new `Date` object. Create an object that represents June 22, 1933.

2. Write a function called `print_date` that takes a `Date` object, uses an f-string to format the fields, and prints the result. If you test it with the `Date` you created, the result should be `1933-06-22`.

3. Write a function called `is_after` that takes two `Date` objects and returns `true` if the first comes after the second. Create a second object that represents September 17, 1933, and check whether it comes after the first object.

Hint: You might find it useful to write a function called `date_to_tuple` that returns a tuple containing the fields of a `Date` in year, month, day order.
