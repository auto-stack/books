# Classes and Methods

Auto is an **object-oriented language** -- that is, it provides features that support object-oriented programming, which has these defining characteristics:

-   Most of the computation is expressed in terms of operations on objects.

-   Objects often represent things in the real world, and methods often correspond to the ways things in the real world interact.

-   Programs include type and method definitions.

For example, in the previous chapter we defined a `Time` type that corresponds to the way people record the time of day, and we defined functions that correspond to the kinds of things people do with times. But there was no explicit connection between the definition of the `Time` type and the function definitions that follow.

We can make the connection explicit by rewriting a function as a **method**, which is defined inside a type definition.

## Defining methods

In the previous chapter we defined a type named `Time` and wrote a function named `print_time` that displays a time of day.

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}

fn print_time(time: Time) {
    let s = f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}"
    print(s)
}
```

To make `print_time` a method, we define it with `&self` as the first parameter. The `&self` parameter refers to the object the method is called on -- it is the **receiver**.

```auto
type Time {
    hour: int,
    minute: int,
    second: int,

    fn print_time(&self) {
        let s = f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
        print(s)
    }
}
```

To call this method, you invoke it on a `Time` instance using dot notation:

```auto
let start = make_time(9, 45, 0)
start.print_time()  // 09:45:00
```

In this version, `start` is the object the method is invoked on, which is called the **receiver**. Inside the method, `self` refers to the same object as `start`.

## Another method

Here's the `time_to_int` function from the previous chapter, rewritten as a method:

```auto
fn time_to_int(&self) -> int {
    let minutes = self.hour * 60 + self.minute
    let seconds = minutes * 60 + self.second
    return seconds
}
```

As in the previous example, the method uses `&self` as the first parameter and accesses fields through `self`. Other than that, the method is identical to the function.

```auto
let start = make_time(9, 45, 0)
let secs = start.time_to_int()
print("Seconds:", secs)  // 35100
```

It is common to say that we "call" a function and "invoke" a method, but they mean the same thing.

## Static methods

As another example, let's consider the `int_to_time` function. This function takes `seconds` as a parameter and returns a new `Time` object. If we transform it into a method, we have to invoke it on a `Time` object. But if we're trying to create a new `Time` object, what are we supposed to invoke it on?

We can solve this problem using a **static method**, which is a method that does not have `&self` as a parameter and is invoked on the type itself rather than on an instance.

```auto
fn int_to_time(seconds: int) -> Time {
    let (minute, second) = divmod(seconds, 60)
    let (hour, minute) = divmod(minute, 60)
    return make_time(hour, minute, second)
}
```

Because it is a static method, it does not have `&self` as a parameter. To invoke it, we use `Time`, which is the type name:

```auto
let start = Time.int_to_time(34800)
start.print_time()  // 09:40:00
```

The result is a new object that represents 9:40.

<Listing number="15-1" file-name="defining_methods.auto" caption="Defining a type with instance and static methods">

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}

fn print_time(&self) {
    let s = f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
    print(s)
}

fn time_to_int(&self) -> int {
    let minutes = self.hour * 60 + self.minute
    let seconds = minutes * 60 + self.second
    return seconds
}

fn add_time(&self, hours: int, minutes: int, seconds: int) -> Time {
    let duration = make_time(hours, minutes, seconds)
    let total = Time.time_to_int(self) + Time.time_to_int(duration)
    return Time.int_to_time(total)
}

fn int_to_time(seconds: int) -> Time {
    let (minute, second) = divmod(seconds, 60)
    let (hour, minute) = divmod(minute, 60)
    return make_time(hour, minute, second)
}

fn make_time(hour: int, minute: int, second: int) -> Time {
    return Time{hour: hour, minute: minute, second: second}
}

fn main() {
    let start = make_time(9, 45, 0)

    // Calling a method on an instance
    start.print_time()  // 09:45:00

    // Another method
    let secs = start.time_to_int()
    print("Seconds since midnight:", secs)  // 35100

    // Calling a method that returns a new object
    let end = start.add_time(1, 32, 0)
    end.print_time()  // 11:17:00

    // Calling the static method via the type
    let t = Time.int_to_time(3661)
    t.print_time()  // 01:01:01
}
```

```python
class Time:
    """Represents the time of day."""

    def print_time(self):
        s = f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
        print(s)

    def time_to_int(self):
        minutes = self.hour * 60 + self.minute
        seconds = minutes * 60 + self.second
        return seconds

    def add_time(self, hours, minutes, seconds):
        duration = make_time(hours, minutes, seconds)
        total = Time.time_to_int(self) + Time.time_to_int(duration)
        return Time.int_to_time(total)

    @staticmethod
    def int_to_time(seconds):
        minute, second = divmod(seconds, 60)
        hour, minute = divmod(minute, 60)
        return make_time(hour, minute, second)


def make_time(hour, minute, second):
    time = Time()
    time.hour = hour
    time.minute = minute
    time.second = second
    return time


def main():
    start = make_time(9, 45, 0)

    # Calling a method on an instance
    start.print_time()  # 09:45:00

    # Another method
    secs = start.time_to_int()
    print(f"Seconds since midnight: {secs}")  # 35100

    # Calling a method that returns a new object
    end = start.add_time(1, 32, 0)
    end.print_time()  # 11:17:00

    # Calling the static method via the class
    t = Time.int_to_time(3661)
    t.print_time()  # 01:01:01


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

Instance methods (with `&self`) are called on an object: `start.print_time()`. Inside the method, `self` refers to the receiving object. Static methods (without `&self`) are called on the type itself: `Time.int_to_time(3661)`. They don't operate on a specific instance and are useful for utility functions that create objects or perform computations related to the type.

## Comparing Time objects

As one more example, let's write `is_after` as a method. Because we're comparing two objects, and the first parameter is `self`, we'll call the second parameter `other`:

```auto
fn is_after(&self, other: Time) -> bool {
    return self.time_to_int() > other.time_to_int()
}
```

To use this method, we invoke it on one object and pass the other as an argument:

```auto
let end = make_time(11, 17, 0)
print(end.is_after(start))    // true
print(start.is_after(end))    // false
```

One nice thing about this syntax is that it almost reads like a question: "`end` is after `start`?"

## The init method

The most important special method is `init`, so-called because it initializes the fields of a new object. An `init` method for the `Time` type might look like this:

```auto
fn init(&self, hour: int = 0, minute: int = 0, second: int = 0) {
    self.hour = hour
    self.minute = minute
    self.second = second
}
```

Now when we instantiate a `Time` object, Auto invokes `init` and passes along the arguments. So we can create an object and initialize the fields at the same time:

```auto
let time = Time(9, 40, 0)
print(time)  // 09:40:00
```

In this example, the parameters have default values, so if you call `Time` with no arguments, you get the defaults:

```auto
let time = Time()
print(time)  // 00:00:00
```

If you provide one argument, it overrides `hour`:

```auto
let time = Time(9)
print(time)  // 09:00:00
```

And if you provide three arguments, they override all three default values.

When writing a new type, it is good practice to start by writing `init`, which makes it easier to create objects, and `to_string`, which is useful for debugging.

<Listing number="15-2" file-name="init_constructor.auto" caption="The init constructor for initializing objects">

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}

// The init constructor -- called automatically on instantiation
fn init(&self, hour: int = 0, minute: int = 0, second: int = 0) {
    self.hour = hour
    self.minute = minute
    self.second = second
}

fn to_string(&self) -> str {
    return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
}

fn main() {
    // Creating with all arguments
    let t1 = Time(9, 40, 0)
    print(t1.to_string())  // 09:40:00

    // Creating with default values (no arguments)
    let t2 = Time()
    print(t2.to_string())  // 00:00:00

    // Partial arguments
    let t3 = Time(9)
    print(t3.to_string())  // 09:00:00

    let t4 = Time(9, 45)
    print(t4.to_string())  // 09:45:00

    // Named arguments
    let t5 = Time(minute = 30, second = 15)
    print(t5.to_string())  // 00:30:15
}
```

```python
class Time:
    """Represents the time of day."""

    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"


def main():
    # Creating with all arguments
    t1 = Time(9, 40, 0)
    print(t1.__str__())  # 09:40:00

    # Creating with default values (no arguments)
    t2 = Time()
    print(t2.__str__())  # 00:00:00

    # Partial arguments
    t3 = Time(9)
    print(t3.__str__())  # 09:00:00

    t4 = Time(9, 45)
    print(t4.__str__())  # 09:45:00

    # Named arguments
    t5 = Time(minute=30, second=15)
    print(t5.__str__())  # 00:30:15


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The `init` method in Auto corresponds to `__init__` in Python. It is called automatically when you create a new object using `Time(...)`. The parameters can have default values, allowing you to create objects with varying levels of specificity -- from `Time()` (all defaults) to `Time(9, 40, 0)` (all specified). Named arguments let you override specific fields without providing preceding ones.

> **Note for Python Programmers:**
>
> Auto uses `fn init(&self, ...)` instead of Python's `def __init__(self, ...)`. The `a2p` transpiler converts `init` to `__init__` automatically.

## The `to_string` method

When you write a method, you can choose almost any name you want. However, some names have special meanings. If an object has a method named `to_string`, Auto uses that method to convert the object to a string when needed -- for example, when printing or using in an f-string.

This is Auto's equivalent of Python's `__str__` method.

```auto
fn to_string(&self) -> str {
    return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
}
```

You can invoke this method in the usual way:

```auto
let s = end.to_string()
print(s)  // 11:17:00
```

But Auto can also invoke it for you. If you print a `Time` object, Auto uses the `to_string` method:

```auto
print(end)  // 11:17:00
```

And it does the same if you use the object in an f-string:

```auto
print(f"The time is {end}")  // The time is 11:17:00
```

<Listing number="15-3" file-name="to_string_method.auto" caption="The to_string method for string representation">

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}

fn init(&self, hour: int = 0, minute: int = 0, second: int = 0) {
    self.hour = hour
    self.minute = minute
    self.second = second
}

// The to_string method -- Auto's equivalent of __str__
fn to_string(&self) -> str {
    return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
}

fn main() {
    let start = Time(9, 45, 30)

    // Calling to_string explicitly
    let s = start.to_string()
    print(s)  // 09:45:30

    // to_string is called automatically by print
    print(start)  // 09:45:30

    // Using f-string interpolation
    print(f"The time is {start}")  // The time is 09:45:30

    // Comparing two times via their string representation
    let end = Time(10, 30, 0)
    print(start.to_string() < end.to_string())  // true (lexicographic)

    // Demonstrating formatting control
    let noon = Time(12, 0, 0)
    print(noon.to_string())  // 12:00:00
}
```

```python
class Time:
    """Represents the time of day."""

    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"


def main():
    start = Time(9, 45, 30)

    # Calling __str__ explicitly
    s = start.__str__()
    print(s)  # 09:45:30

    # __str__ is called automatically by print
    print(start)  # 09:45:30

    # Using f-string interpolation
    print(f"The time is {start}")  # The time is 09:45:30

    # Comparing two times via their string representation
    end = Time(10, 30, 0)
    print(start.__str__() < end.__str__())  # True (lexicographic)

    # Demonstrating formatting control
    noon = Time(12, 0, 0)
    print(noon.__str__())  # 12:00:00


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The `to_string` method in Auto corresponds to `__str__` in Python. It returns a string representation of the object. When you print an object or use it in an f-string, Auto (via the `a2p` transpiler) automatically calls this method. The format specifiers `:02d` ensure that minutes and seconds are always displayed with two digits.

> **Note for Python Programmers:**
>
> Auto uses `fn to_string(&self)` instead of Python's `def __str__(self)`. The `a2p` transpiler converts `to_string` to `__str__` automatically. When reading Auto code, any method named `to_string` is the string representation method.

## Operator overloading

By defining special methods, you can specify the behavior of operators on programmer-defined types. For example, if you define a method named `__add__` for the `Time` type, you can use the `+` operator on Time objects.

Here is an `__add__` method:

```auto
fn __add__(&self, other: Time) -> Time {
    let seconds = self.time_to_int() + other.time_to_int()
    return Time.int_to_time(seconds)
}
```

We can use it like this:

```auto
let start = Time(9, 45, 0)
let duration = Time(1, 32, 0)
let end = start + duration
print(end)  // 11:17:00
```

There is a lot happening when we run these three lines of code:

- When we instantiate a `Time` object, the `init` method is invoked.
- When we use the `+` operator with a `Time` object, its `__add__` method is invoked.
- And when we print a `Time` object, its `to_string` method is invoked.

Changing the behavior of an operator so that it works with programmer-defined types is called **operator overloading**. For every operator, like `+`, there is a corresponding special method, like `__add__`.

We can also overload the `==` operator for equality comparison:

```auto
fn __eq__(&self, other: Time) -> bool {
    return self.time_to_int() == other.time_to_int()
}
```

```auto
print(start == Time(9, 45, 0))  // true
print(start == duration)        // false
```

<Listing number="15-4" file-name="operator_overloading.auto" caption="Operator overloading for comparison and addition">

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}

fn init(&self, hour: int = 0, minute: int = 0, second: int = 0) {
    self.hour = hour
    self.minute = minute
    self.second = second
}

fn to_string(&self) -> str {
    return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
}

fn time_to_int(&self) -> int {
    let minutes = self.hour * 60 + self.minute
    let seconds = minutes * 60 + self.second
    return seconds
}

fn int_to_time(seconds: int) -> Time {
    let (minute, second) = divmod(seconds, 60)
    let (hour, minute) = divmod(minute, 60)
    return Time(hour, minute, second)
}

// Operator overloading: is_after comparison
fn is_after(&self, other: Time) -> bool {
    return self.time_to_int() > other.time_to_int()
}

// Operator overloading: + operator (add)
fn __add__(&self, other: Time) -> Time {
    let seconds = self.time_to_int() + other.time_to_int()
    return Time.int_to_time(seconds)
}

// Operator overloading: == operator (eq)
fn __eq__(&self, other: Time) -> bool {
    return self.time_to_int() == other.time_to_int()
}

fn main() {
    let start = Time(9, 45, 0)
    let end = Time(11, 17, 0)
    let duration = Time(1, 32, 0)

    // Comparing: is_after
    print(end.is_after(start))    // true
    print(start.is_after(end))    // false
    print(end.is_after(end))      // false

    // Operator overloading: +
    let result = start + duration
    print(result.to_string())  // 11:17:00

    // Chaining additions
    let result2 = start + duration + Time(0, 30, 0)
    print(result2.to_string())  // 11:47:00

    // Operator overloading: ==
    print(start == Time(9, 45, 0))  // true
    print(start == end)             // false

    // Combining operators
    let total = duration + Time(0, 30, 0)
    let finish = start + total
    print(finish.to_string())  // 11:47:00
}
```

```python
class Time:
    """Represents the time of day."""

    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"

    def time_to_int(self):
        minutes = self.hour * 60 + self.minute
        seconds = minutes * 60 + self.second
        return seconds

    @staticmethod
    def int_to_time(seconds):
        minute, second = divmod(seconds, 60)
        hour, minute = divmod(minute, 60)
        return Time(hour, minute, second)

    # Operator overloading: comparison
    def is_after(self, other):
        return self.time_to_int() > other.time_to_int()

    # Operator overloading: + operator
    def __add__(self, other):
        seconds = self.time_to_int() + other.time_to_int()
        return Time.int_to_time(seconds)

    # Operator overloading: == operator
    def __eq__(self, other):
        return self.time_to_int() == other.time_to_int()


def main():
    start = Time(9, 45, 0)
    end = Time(11, 17, 0)
    duration = Time(1, 32, 0)

    # Comparing: is_after
    print(end.is_after(start))  # True
    print(start.is_after(end))  # False
    print(end.is_after(end))  # False

    # Operator overloading: +
    result = start + duration
    print(result.__str__())  # 11:17:00

    # Chaining additions
    result2 = start + duration + Time(0, 30, 0)
    print(result2.__str__())  # 11:47:00

    # Operator overloading: ==
    print(start == Time(9, 45, 0))  # True
    print(start == end)  # False

    # Combining operators
    total = duration + Time(0, 30, 0)
    finish = start + total
    print(finish.__str__())  # 11:47:00


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

Operator overloading lets you define how operators like `+` and `==` work with your custom types. The `__add__` method is called when you use `+`, and `__eq__` is called when you use `==`. Both are instance methods that take `&self` and `other` as parameters.

The `is_after` method is not an operator overload -- it's a regular method with a descriptive name. But it demonstrates the same pattern of comparing objects by converting them to a simpler representation (integers) first.

## Debugging

A `Time` object is valid if the values of `minute` and `second` are between `0` and `60` -- including `0` but not `60` -- and if `hour` is positive. Also, `hour` and `minute` should be integer values. Requirements like these are called **invariants** because they should always be true.

Writing code to check invariants can help detect errors and find their causes. For example, you might have a method like `is_valid` that returns `false` if an invariant is violated:

```auto
fn is_valid(&self) -> bool {
    if self.hour < 0 or self.minute < 0 or self.second < 0 {
        return false
    }
    if self.minute >= 60 or self.second >= 60 {
        return false
    }
    return true
}
```

Then, at the beginning of each method you can check the arguments to make sure they are valid:

```auto
fn is_after(&self, other: Time) -> bool {
    assert self.is_valid(), "self is not a valid Time"
    assert other.is_valid(), "other is not a valid Time"
    return self.time_to_int() > other.time_to_int()
}
```

The `assert` statement evaluates the expression that follows. If the result is `true`, it does nothing; if the result is `false`, it causes an error.

## Glossary

**object-oriented language:**
A language that provides features to support object-oriented programming, notably user-defined types.

**method:**
A function that is defined inside a type definition and is invoked on instances of that type.

**receiver:**
The object a method is invoked on.

**static method:**
A method that can be invoked without an object as receiver. In Auto, this is a method without `&self` as a parameter.

**instance method:**
A method that must be invoked with an object as receiver. In Auto, this is a method with `&self` as a parameter.

**special method:**
A method that changes the way operators and some functions work with an object. In Auto, these include `init`, `to_string`, `__add__`, `__eq__`, etc.

**operator overloading:**
The process of using special methods to change the way operators work with user-defined types.

**invariant:**
A condition that should always be true during the execution of a program.

## Exercises

### Exercise

In the previous chapter, a series of exercises asked you to write a `Date` type and several functions that work with `Date` objects. Now let's practice rewriting those functions as methods.

1. Write a definition for a `Date` type that represents a date -- that is, a year, month, and day of the month. Include an `init` method that takes `year`, `month`, and `day` as parameters.

2. Write a `to_string` method that uses an f-string to format the fields and returns the result. If you test it with the `Date` you created, the result should be `1933-06-22`.

3. Write a method called `is_after` that takes two `Date` objects and returns `true` if the first comes after the second. Create a second object that represents September 17, 1933, and check whether it comes after the first object.

Hint: You might find it useful to write a method called `to_tuple` that returns a tuple that contains the fields of a `Date` object in year-month-day order.
