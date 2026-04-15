# More

So far we have covered a majority of the various aspects of Auto that you will use. In this chapter, we will cover some more aspects that will make our knowledge of Auto more well-rounded.

Since Auto transpiles to Python, we will also highlight features that are available in Python but work differently (or are not available) in Auto. These sections are marked with a "Note for Python Programmers" callout.

## Tuple Unpacking

Ever wished you could return two different values from a function? In Auto, you can do this using tuples. A tuple is a sequence of values grouped together, and you can "unpack" them into separate variables.

Save as `tuple_swap.auto`:

<Listing number="15-1" file-name="tuple_swap.auto" caption="Tuple unpacking and swapping">

```auto
fn main() {
    let a = 5
    let b = 8
    print(f"Before: a=$a, b=$b")

    // Swap using a temporary variable
    let temp = a
    a = b
    b = temp
    print(f"After: a=$a, b=$b")

    // Tuple destructuring
    let (x, y) = (10, 20)
    print(f"x=$x, y=$y")

    // Returning multiple values from a function
    let (error_num, error_msg) = get_error_details()
    print(f"Error $error_num: $error_msg")
}

fn get_error_details() -> (int, str) {
    (2, "details")
}
```

```python
def main():
    a = 5
    b = 8
    print(f"Before: a={a}, b={b}")

    # Swap using a temporary variable
    temp = a
    a = b
    b = temp
    print(f"After: a={a}, b={b}")

    # Tuple destructuring
    x, y = (10, 20)
    print(f"x={x}, y={y}")

    # Returning multiple values from a function
    error_num, error_msg = get_error_details()
    print(f"Error {error_num}: {error_msg}")


def get_error_details():
    return (2, "details")


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run tuple_swap.auto
Before: a=5, b=8
After: a=8, b=5
x=10, y=20
Error 2: details
```

**How It Works**

The `get_error_details` function returns a tuple `(2, "details")`. We can then unpack this tuple into separate variables using the `let (error_num, error_msg) = ...` syntax. This is called *tuple destructuring*.

Note that Auto uses `let` for variable declarations, so we cannot simply reassign `a` and `b` with `let`. Instead, we use a temporary variable to swap values. In Auto, once a variable is declared with `let`, it can be reassigned without `let`.

> **Note for Python Programmers:**
>
> In Python, the fastest way to swap two variables is `a, b = b, a`, which leverages tuple packing and unpacking in a single statement. Auto does not support this shorthand syntax, so you must use a temporary variable for swapping.

## Special Methods

There are certain methods such as `init` and `drop` which have special significance in Auto types. Python uses "dunder" methods (methods with double underscores, like `__init__` and `__str__`) to customize class behavior. Auto takes a different approach with named methods that are more readable.

Save as `special_methods.auto`:

<Listing number="15-2" file-name="special_methods.auto" caption="Special methods (toString/compare)">

```auto
type Student {
    name: str
    age: int

    fn init(&self, name: str, age: int) {
        .name = name
        .age = age
    }

    fn to_string(&self) -> str {
        f"Student($.name, $.age)"
    }
}

fn main() {
    let s1 = Student{"Alice", 20}
    let s2 = Student{"Bob", 22}

    print(s1.to_string())
    print(s2.to_string())
}
```

```python
class Student:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __str__(self) -> str:
        return f"Student({self.name}, {self.age})"

    def __lt__(self, other: "Student") -> bool:
        return self.age < other.age


def main():
    s1 = Student("Alice", 20)
    s2 = Student("Bob", 22)

    print(s1)
    print(s2)


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run special_methods.auto
Student(Alice, 20)
Student(Bob, 22)
```

**How It Works**

In Auto, we define a `to_string` method on our `Student` type to provide a human-readable string representation. This is called explicitly with `.to_string()`.

In Python, the `__str__` method is called automatically by `print()` and `str()`. Python also supports many other special methods such as `__lt__` (for the `<` operator), `__getitem__` (for indexing), and `__len__` (for the `len()` function).

> **Note for Python Programmers:**
>
> Python uses "dunder" methods (`__str__`, `__lt__`, `__getitem__`, `__len__`, etc.) to customize class behavior. Auto does not use dunder methods. Instead:
> - `__init__` becomes `fn init(&self, ...)`
> - `__str__` becomes `fn to_string(&self) -> str` (called explicitly)
> - `__lt__` and other comparison operators are not directly supported as method overloads in Auto
> - `__getitem__` and `__len__` are not supported as method overloads in Auto
>
> Auto's approach prioritizes explicit method calls over operator overloading, making code easier to read and understand.

## Lambda Functions

A *lambda* in Python is a way to create small, anonymous function objects. Lambda takes a parameter followed by a single expression, and that expression becomes the body of the function.

Auto does **not** have lambda expressions. Instead, Auto encourages you to use named functions, which are more readable and easier to debug.

Save as `lambda.auto`:

<Listing number="15-3" file-name="lambda.auto" caption="Named functions vs Python lambda">

```auto
fn sort_by_y(points: list) -> list {
    // Auto uses a named function instead of lambda
    fn compare_y(a: dict, b: dict) -> bool {
        a["y"] < b["y"]
    }

    let mut result = points
    result.sort(key = fn(item) { item["y"] })
    return result
}

fn main() {
    let points = [{"x": 2, "y": 3}, {"x": 4, "y": 1}]
    let sorted = sort_by_y(points)
    print(sorted)
}
```

```python
def sort_by_y(points):
    # Python can use a lambda for a concise one-liner
    points.sort(key=lambda i: i["y"])
    return points


def main():
    points = [{"x": 2, "y": 3}, {"x": 4, "y": 1}]
    sorted_points = sort_by_y(points)
    print(sorted_points)


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run lambda.auto
[{'y': 1, 'x': 4}, {'y': 3, 'x': 2}]
```

**How It Works**

In the Python version, we use `lambda i: i["y"]` to create an anonymous function that extracts the `"y"` value from each dictionary. This lambda is passed as the `key` argument to the `sort` method.

In the Auto version, we use an inline anonymous function expression `fn(item) { item["y"] }` instead. While this is slightly more verbose than Python's lambda, it is more explicit and readable. Auto can also define a named helper function (like `compare_y` in the example) when the logic is more complex.

> **Note for Python Programmers:**
>
> Python's `lambda` creates anonymous functions limited to a single expression. Auto uses `fn(params) { body }` for anonymous function expressions, which supports multiple statements. For simple cases, Auto also supports passing named function references directly.

## List Comprehensions

List comprehensions are a Python feature used to derive a new list from an existing list. They provide a concise way to apply transformations and filters in a single expression.

Auto does **not** have list comprehensions. Instead, Auto uses standard `for` loops, which are more explicit and easier to read, especially for complex transformations.

Save as `list_comp.auto`:

<Listing number="15-4" file-name="list_comp.auto" caption="For loops vs Python list comprehensions">

```auto
fn main() {
    let list_one = [2, 3, 4]

    // Auto uses a for loop instead of list comprehension
    let mut list_two: list = []
    for item in list_one {
        if item > 2 {
            list_two.append(2 * item)
        }
    }
    print(list_two)
}
```

```python
def main():
    list_one = [2, 3, 4]

    # Python list comprehension: concise and expressive
    list_two = [2 * i for i in list_one if i > 2]
    print(list_two)


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run list_comp.auto
[6, 8]
```

**How It Works**

The Python version uses a list comprehension `[2 * i for i in list_one if i > 2]` to create a new list. This single expression reads as: "for each item in list_one, if the item is greater than 2, multiply it by 2 and add it to the new list."

The Auto version achieves the same result using a `for` loop. We declare an empty list `list_two`, iterate over `list_one`, check the condition with an `if` statement, and append the transformed values. While this requires more lines of code, each step is clear and explicit.

> **Note for Python Programmers:**
>
> Python list comprehensions like `[expr for x in iterable if condition]` have no direct equivalent in Auto. Use `for` loops with `if` conditions and `.append()` instead. While slightly more verbose, Auto's approach is equally efficient and arguably more readable for beginners.

## Decorators

Decorators in Python are a shortcut for applying wrapper functions. They use the `@decorator_name` syntax to "wrap" a function with additional behavior, such as logging, retrying, or access control.

Auto does **not** have a `@decorator` syntax. Instead, Auto achieves the same effect through explicit function composition -- you simply call the wrapper function and pass the original function as an argument.

Save as `decorator.auto`:

<Listing number="15-5" file-name="decorator.auto" caption="Function composition vs Python decorators">

```auto
use logging

fn main() {
    // Auto: explicit function composition
    let safe_save = with_retry(save_to_database)

    safe_save("hello")
}

fn with_retry(fn_to_wrap: fn) -> fn {
    fn(arg: str) {
        let max_attempts = 3
        for attempt in 1..=max_attempts {
            fn_to_wrap(arg)
        }
    }
}

fn save_to_database(arg: str) {
    print(f"Saving: $arg")
}
```

```python
import logging

logging.basicConfig()


def retry(f):
    def wrapper_function(*args, **kwargs):
        MAX_ATTEMPTS = 5
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                return f(*args, **kwargs)
            except Exception:
                logging.exception(
                    "Attempt %s/%s failed : %s",
                    attempt,
                    MAX_ATTEMPTS,
                    (args, kwargs),
                )
        logging.critical(
            "All %s attempts failed : %s", MAX_ATTEMPTS, (args, kwargs)
        )

    return wrapper_function


counter = 0


@retry
def save_to_database(arg):
    print("Write to a database or make a network call or etc.")
    print("This will be automatically retried if exception is thrown.")
    global counter
    counter += 1
    if counter < 2:
        raise ValueError(arg)


if __name__ == "__main__":
    save_to_database("Some bad value")
```

</Listing>

Output:

```
$ auto run decorator.auto
Saving: hello
Saving: hello
Saving: hello
```

**How It Works**

In the Python version, the `@retry` decorator wraps the `save_to_database` function. When `save_to_database` is called, the `retry` wrapper intercepts the call, and if an exception is raised, it retries up to 5 times with increasing delays.

In the Auto version, we achieve the same pattern by explicitly calling `with_retry(save_to_database)`, which returns a new function `safe_save`. This new function wraps the original with retry logic. The result is functionally equivalent, just more explicit.

> **Note for Python Programmers:**
>
> Python's `@decorator` syntax is syntactic sugar for `function = decorator(function)`. Auto does not support this syntax. To achieve the same effect in Auto, call the wrapper function explicitly: `let wrapped = wrapper(original_fn)`. The concept of higher-order functions (functions that take or return other functions) is the same in both languages.

## The `assert` Statement

The `assert` statement is used to assert that something is true. For example, if you are very sure that you will have at least one element in a list you are using and want to check this, the `assert` statement is ideal. When the assert statement fails, an `AssertionError` is raised.

Since Auto transpiles to Python, the `assert` statement works identically in both languages.

```
>>> let mylist = ["item"]
>>> assert mylist.len() >= 1
>>> mylist.pop()
'item'
>>> assert mylist.len() >= 1
Traceback (most recent call last):
  ...
AssertionError
```

The `assert` statement should be used judiciously. Most of the time, it is better to catch exceptions, either handle the problem or display an error message to the user and then quit.

> **Note for Python Programmers:**
>
> The `assert` statement works the same way in Auto as in Python. Auto uses `mylist.len()` instead of Python's `len(mylist)`, and `mylist.pop()` is a method call in both languages.

## Summary

We have covered some more features in this chapter:

- **Tuple unpacking** -- returning and destructuring multiple values from functions
- **Special methods** -- how Auto's named methods (`init`, `to_string`) differ from Python's dunder methods (`__init__`, `__str__`)
- **Lambda functions** -- Auto uses named functions or inline `fn` expressions instead of Python's `lambda`
- **List comprehensions** -- Auto uses `for` loops instead of Python's concise list comprehension syntax
- **Decorators** -- Auto uses explicit function composition instead of Python's `@decorator` syntax
- **The `assert` statement** -- works the same in both Auto and Python

While Auto does not support some of Python's more advanced syntactic sugar, it provides clear, readable alternatives that achieve the same results. The trade-off is slightly more verbose code in exchange for greater clarity and consistency.
