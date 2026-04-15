# Python Extras

The previous chapters cover the core features of Python (as expressed in Auto). But Python has many additional features that are useful and worth knowing. This chapter covers a selection of these extras.

## Sets

A **set** is a collection of elements that is unordered and contains no duplicates. Auto provides `HashSet` from the standard library.

<Listing number="18-1" file-name="hashset.auto" caption="Creating and using a HashSet">

```auto
use std::collections::HashSet

fn main() {
    // Creating a HashSet from a list
    let languages: HashSet<str> = ["Python", "Auto", "Java", "C++", "Python"]
    print(languages)
    // {"Python", "Auto", "Java", "C++"}

    // Adding elements
    languages.add("Rust")
    print(languages)
    // {"Python", "Auto", "Java", "C++", "Rust"}

    // Checking membership
    print("Auto" in languages)   // true
    print("Go" in languages)     // false

    // Removing elements
    languages.remove("C++")
    print(languages)
    // {"Python", "Auto", "Java", "Rust"}

    // Set size
    print(languages.len())       // 4

    // Set operations
    let a: HashSet<int> = [1, 2, 3, 4]
    let b: HashSet<int> = [3, 4, 5, 6]

    // Union
    print(a | b)   // {1, 2, 3, 4, 5, 6}

    // Intersection
    print(a & b)   // {3, 4}

    // Difference
    print(a - b)   // {1, 2}

    // Symmetric difference
    print(a ^ b)   // {1, 2, 5, 6}
}
```

```python
from __future__ import annotations

def main():
    # Creating a set from a list
    languages = {"Python", "Auto", "Java", "C++", "Python"}
    print(languages)
    # {"Python", "Auto", "Java", "C++"}

    # Adding elements
    languages.add("Rust")
    print(languages)
    # {"Python", "Auto", "Java", "C++", "Rust"}

    # Checking membership
    print("Auto" in languages)   # True
    print("Go" in languages)     # False

    # Removing elements
    languages.remove("C++")
    print(languages)
    # {"Python", "Auto", "Java", "Rust"}

    # Set size
    print(len(languages))        # 4

    # Set operations
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}

    # Union
    print(a | b)   # {1, 2, 3, 4, 5, 6}

    # Intersection
    print(a & b)   # {3, 4}

    # Difference
    print(a - b)   # {1, 2}

    # Symmetric difference
    print(a ^ b)   # {1, 2, 5, 6}


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

In Auto, `HashSet` is imported from `std::collections`. You can create a `HashSet` from a list literal -- duplicate values are automatically removed. The `add` and `remove` methods modify the set in place. Set operations like union (`|`), intersection (`&`), difference (`-`), and symmetric difference (`^`) work the same way in both Auto and Python.

> **Note for Python Programmers:**
>
> Auto uses `HashSet<str>` with explicit type parameters, while Python uses the built-in `set` type. Auto's `HashSet` requires importing from `std::collections`, but the operations are identical.

Sets are useful for removing duplicates from a collection and for checking membership efficiently. The `in` operator for sets is generally faster than for lists because sets use hash tables internally.

## Counters and defaultdict

Python's `collections` module provides `Counter` and `defaultdict`, which are convenient wrappers around dictionaries. In Auto, you can achieve the same results with regular dictionaries and helper functions.

<Listing number="18-2" file-name="list_comprehensions.auto" caption="List comprehensions and counting patterns">

```auto
fn main() {
    // List comprehension equivalent: Auto uses for loops
    let squares: [int] = []
    for i in 0..10 {
        squares.append(i * i)
    }
    print(squares)
    // [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

    // Python list comprehension: [i * i for i in range(10)]

    // Filtering with a for loop
    let even_squares: [int] = []
    for i in 0..10 {
        if i % 2 == 0 {
            even_squares.append(i * i)
        }
    }
    print(even_squares)
    // [0, 4, 16, 36, 64]

    // Python: [i * i for i in range(10) if i % 2 == 0]

    // Counter pattern: counting word frequencies
    let words = ["the", "cat", "in", "the", "hat", "in", "the"]
    let mut counts: HashMap<str, int> = {}
    for word in words {
        counts[word] = counts.get(word, 0) + 1
    }
    print(counts)
    // {"the": 3, "cat": 1, "in": 2, "hat": 1}

    // Python: Counter(words)

    // Finding the most common
    let mut max_word = ""
    let mut max_count = 0
    for (word, count) in counts {
        if count > max_count {
            max_word = word
            max_count = count
        }
    }
    print(f"Most common: '{max_word}' appears {max_count} times")
    // Most common: 'the' appears 3 times

    // Grouping with a dictionary (defaultdict pattern)
    let letters = "abracadabra"
    let mut positions: HashMap<str, [int]> = {}
    for (i, letter) in enumerate(letters) {
        if letter not in positions {
            positions[letter] = []
        }
        positions[letter].append(i)
    }
    print(positions)
    // {"a": [0, 3, 5, 7, 10], "b": [1, 8], "r": [2, 9], "c": [4], "d": [6]}
}
```

```python
def main():
    # List comprehension equivalent: Auto uses for loops
    squares = []
    for i in range(10):
        squares.append(i * i)
    print(squares)
    # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

    # Filtering with a for loop
    even_squares = []
    for i in range(10):
        if i % 2 == 0:
            even_squares.append(i * i)
    print(even_squares)
    # [0, 4, 16, 36, 64]

    # Counter pattern: counting word frequencies
    words = ["the", "cat", "in", "the", "hat", "in", "the"]
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    print(counts)
    # {"the": 3, "cat": 1, "in": 2, "hat": 1}

    # Finding the most common
    max_word = ""
    max_count = 0
    for word, count in counts.items():
        if count > max_count:
            max_word = word
            max_count = count
    print(f"Most common: '{max_word}' appears {max_count} times")
    # Most common: 'the' appears 3 times

    # Grouping with a dictionary (defaultdict pattern)
    letters = "abracadabra"
    positions = {}
    for i, letter in enumerate(letters):
        if letter not in positions:
            positions[letter] = []
        positions[letter].append(i)
    print(positions)
    # {"a": [0, 3, 5, 7, 10], "b": [1, 8], "r": [2, 9], "c": [4], "d": [6]}


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

Auto does not have list comprehensions. Instead, you use explicit `for` loops with `append`. The resulting Python code from the `a2p` transpiler also uses `for` loops rather than comprehensions, which some may find more readable.

For counting, Auto uses the `HashMap.get(key, default)` pattern instead of Python's `Counter`. For grouping (the `defaultdict` pattern), you check if the key exists and initialize it if not.

> **Note for Python Programmers:**
>
> Auto uses `HashMap` explicitly rather than Python's `dict`. The `a2p` transpiler converts Auto's `HashMap<K, V>` to Python's `dict`. While Python has `Counter` and `defaultdict` for convenience, Auto achieves the same results with a few extra lines of explicit code.

## Conditional expressions

Python has a **conditional expression**, also called a "ternary operator," which allows you to write an `if`/`else` in a single expression. Auto supports the same pattern.

```auto
let x = 5
let label = if x < 10 { "low" } else { "high" }
print(label)  // low
```

The equivalent in Python:

```python
x = 5
label = "low" if x < 10 else "high"
print(label)  # low
```

Conditional expressions are often shorter than an `if` statement, but they are not always easier to read. Use them when the logic is simple and the expression is short.

## Named tuples

A **named tuple** is a tuple where each element has a name. Named tuples are useful when you want a simple object with named attributes, but you don't need the full functionality of a class.

In Auto, you achieve the same thing with a `type` definition, which is more explicit and provides the same benefits.

<Listing number="18-3" file-name="named_tuples.auto" caption="Named tuples using Auto type definitions">

```auto
type Point {
    x: float,
    y: float,
}

fn main() {
    // Creating a Point (equivalent to a named tuple)
    let p = Point(3.0, 4.0)
    print(p.x)  // 3.0
    print(p.y)  // 4.0

    // Points are comparable by their fields
    let p2 = Point(1.0, 2.0)
    let p3 = Point(3.0, 4.0)
    print(p == p3)  // true
    print(p == p2)  // false

    // You can also convert to a tuple for unpacking
    let (a, b) = (p.x, p.y)
    print(f"Unpacked: a={a}, b={b}")  // Unpacked: a=3.0, b=4.0

    // Computing distance
    let distance = (p.x ** 2 + p.y ** 2) ** 0.5
    print(f"Distance from origin: {distance}")  // Distance from origin: 5.0

    // Using as dictionary keys (via tuple conversion)
    let mut grid: HashMap<(float, float), str> = {}
    grid[(1.0, 2.0)] = "A"
    grid[(3.0, 4.0)] = "B"
    print(grid)  // {(1.0, 2.0): "A", (3.0, 4.0): "B"}

    // A more complex named tuple: representing a date
    type Date {
        year: int,
        month: int,
        day: int,
    }

    let birthday = Date(2000, 1, 15)
    print(f"Year: {birthday.year}, Month: {birthday.month}, Day: {birthday.day}")
    // Year: 2000, Month: 1, Day: 15

    // Comparing dates (lexicographic comparison)
    let today = Date(2025, 4, 15)
    print(today > birthday)  // true
}
```

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __gt__(self, other):
        if self.year != other.year:
            return self.year > other.year
        if self.month != other.month:
            return self.month > other.month
        return self.day > other.day


def main():
    p = Point(3.0, 4.0)
    print(p.x)  # 3.0
    print(p.y)  # 4.0

    p2 = Point(1.0, 2.0)
    p3 = Point(3.0, 4.0)
    print(p == p3)  # True
    print(p == p2)  # False

    a, b = p.x, p.y
    print(f"Unpacked: a={a}, b={b}")  # Unpacked: a=3.0, b=4.0

    distance = (p.x ** 2 + p.y ** 2) ** 0.5
    print(f"Distance from origin: {distance}")  # Distance from origin: 5.0

    grid = {}
    grid[(1.0, 2.0)] = "A"
    grid[(3.0, 4.0)] = "B"
    print(grid)  # {(1.0, 2.0): "A", (3.0, 4.0): "B"}

    birthday = Date(2000, 1, 15)
    print(f"Year: {birthday.year}, Month: {birthday.month}, Day: {birthday.day}")
    # Year: 2000, Month: 1, Day: 15

    today = Date(2025, 4, 15)
    print(today > birthday)  # True


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

In Auto, a `type` definition serves the same purpose as Python's `namedtuple`. Both provide objects with named attributes. Auto's `type` is more flexible -- you can add methods, use default values, and define custom behavior.

The `a2p` transpiler converts Auto's `type` definitions into Python classes with `__init__`, `__eq__`, and comparison methods as needed.

> **Note for Python Programmers:**
>
> Python's `namedtuple` is lightweight and immutable. Auto's `type` is also lightweight but is mutable by default. If you want immutability, use `let` for the fields. The `a2p` transpiler generates Python classes rather than `namedtuple` instances, giving you more control over behavior.

## any and all

Python provides built-in functions `any` and `all` that take an iterable of boolean values and return a single boolean result.

- `any` returns `true` if **at least one** element is truthy.
- `all` returns `true` if **all** elements are truthy.

In Auto, you can use these functions from the standard library, or implement the logic yourself with a loop.

<Listing number="18-4" file-name="conditional_expressions.auto" caption="Conditional expressions, any, and all">

```auto
fn main() {
    // Conditional expressions (ternary operator)
    let age = 20
    let category = if age < 13 { "child" } else if age < 18 { "teenager" } else { "adult" }
    print(f"Age {age}: {category}")  // Age 20: adult

    let score = 85
    let grade = if score >= 90 { "A" } else if score >= 80 { "B" } else if score >= 70 { "C" } else if score >= 60 { "D" } else { "F" }
    print(f"Score {score}: Grade {grade}")  // Score 85: Grade B

    // any: at least one element is truthy
    let numbers = [0, 0, 0, 1, 0]
    print(any(numbers))   // true

    let empty: [int] = []
    print(any(empty))     // false

    let all_zeros = [0, 0, 0]
    print(any(all_zeros)) // false

    // all: all elements are truthy
    let positives = [1, 2, 3, 4]
    print(all(positives))  // true

    let mixed = [1, 2, 0, 4]
    print(all(mixed))      // false

    // Practical example: checking if all strings are non-empty
    let words = ["hello", "world", "auto"]
    let mut all_nonempty = true
    for word in words {
        if word.len() == 0 {
            all_nonempty = false
            break
        }
    }
    print(all_nonempty)  // true

    // Practical example: checking if any string contains a digit
    let inputs = ["hello", "test123", "world"]
    let mut has_digit = false
    for s in inputs {
        for c in s {
            if c.isdigit() {
                has_digit = true
                break
            }
        }
        if has_digit {
            break
        }
    }
    print(has_digit)  // true

    // Combining conditional expressions with any/all
    let scores = [65, 72, 88, 91, 45]
    let passing = [s for s in scores if s >= 60]  // Auto uses for loop
    // Python: passing = [s for s in scores if s >= 60]

    let mut filtered: [int] = []
    for s in scores {
        if s >= 60 {
            filtered.append(s)
        }
    }
    print(filtered)     // [65, 72, 88, 91]
    print(all(filtered)) // true (all >= 60)

    // Using any with a generator-like pattern
    let mut any_failing = false
    for s in scores {
        if s < 60 {
            any_failing = true
            break
        }
    }
    print(any_failing)  // true
}
```

```python
def main():
    # Conditional expressions (ternary operator)
    age = 20
    category = "child" if age < 13 else ("teenager" if age < 18 else "adult")
    print(f"Age {age}: {category}")  # Age 20: adult

    score = 85
    grade = ("A" if score >= 90 else ("B" if score >= 80 else ("C" if score >= 70 else ("D" if score >= 60 else "F"))))
    print(f"Score {score}: Grade {grade}")  # Score 85: Grade B

    # any: at least one element is truthy
    numbers = [0, 0, 0, 1, 0]
    print(any(numbers))   # True

    empty = []
    print(any(empty))     # False

    all_zeros = [0, 0, 0]
    print(any(all_zeros)) # False

    # all: all elements are truthy
    positives = [1, 2, 3, 4]
    print(all(positives))  # True

    mixed = [1, 2, 0, 4]
    print(all(mixed))      # False

    # Practical example: checking if all strings are non-empty
    words = ["hello", "world", "auto"]
    all_nonempty = True
    for word in words:
        if len(word) == 0:
            all_nonempty = False
            break
    print(all_nonempty)  # True

    # Practical example: checking if any string contains a digit
    inputs = ["hello", "test123", "world"]
    has_digit = False
    for s in inputs:
        for c in s:
            if c.isdigit():
                has_digit = True
                break
        if has_digit:
            break
    print(has_digit)  # True

    # Combining conditional expressions with any/all
    scores = [65, 72, 88, 91, 45]

    filtered = []
    for s in scores:
        if s >= 60:
            filtered.append(s)
    print(filtered)     # [65, 72, 88, 91]
    print(all(filtered)) # True (all >= 60)

    # Using any with a generator-like pattern
    any_failing = False
    for s in scores:
        if s < 60:
            any_failing = True
            break
    print(any_failing)  # True


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

Auto's conditional expression syntax is `if condition { value1 } else { value2 }`, which is similar to Python's `value1 if condition else value2` but with the condition first (like an `if` statement). For chained conditions, Auto nests the expressions naturally.

The `any` and `all` functions work the same in both Auto and Python. They take an iterable and return a boolean. In Auto, when you need early termination (like `break`), you use explicit loops instead of generator expressions.

> **Note for Python Programmers:**
>
> Python's conditional expression puts the value first: `x if condition else y`. Auto puts the condition first: `if condition { x } else { y }`. Python's generator expressions (like `any(x > 0 for x in numbers)`) don't have a direct Auto equivalent -- use explicit loops instead.

## Debugging

When you are working with sets, dictionaries, and other collections, there are a few common sources of errors:

**Mutable default arguments:** In Python, using a mutable object (like a list or dict) as a default argument can cause unexpected behavior because the same object is shared across all calls. In Auto, default values are evaluated each time, so this is not an issue.

**Set/dict key types:** Only immutable types can be used as keys in a dictionary or elements in a set. In Python, this means strings, numbers, and tuples of immutables. Auto follows the same rule -- you cannot use a list as a dictionary key.

**Modifying while iterating:** Modifying a collection while iterating over it can cause errors or unexpected behavior. If you need to modify a collection during iteration, iterate over a copy.

```auto
// WRONG: modifying list while iterating
let mut items = [1, 2, 3, 4, 5]
for item in items {
    if item == 3 {
        items.remove(item)  // undefined behavior!
    }
}

// CORRECT: collect items to remove, then remove them
let mut items = [1, 2, 3, 4, 5]
let mut to_remove: [int] = []
for item in items {
    if item == 3 {
        to_remove.append(item)
    }
}
for item in to_remove {
    items.remove(item)
}
```

## Glossary

**set:**
An unordered collection of unique elements. In Auto, represented by `HashSet`.

**HashSet:**
Auto's set type, imported from `std::collections`.

**set operation:**
Operations like union (`|`), intersection (`&`), difference (`-`), and symmetric difference (`^`) that combine sets.

**Counter:**
A dictionary that maps elements to their frequencies. In Python, provided by `collections.Counter`. In Auto, implemented with a regular `HashMap`.

**defaultdict:**
A dictionary that provides a default value for missing keys. In Python, provided by `collections.defaultdict`. In Auto, implemented with explicit key checking.

**list comprehension:**
A Python expression that creates a list by applying an expression to each element of an iterable, optionally filtered by a condition. Auto uses explicit `for` loops instead.

**conditional expression:**
An expression that returns one of two values depending on a boolean condition. Also called a "ternary operator."

**named tuple:**
A tuple with named elements. In Auto, achieved with a `type` definition.

**any:**
A function that returns `true` if at least one element of an iterable is truthy.

**all:**
A function that returns `true` if all elements of an iterable are truthy.

## Exercises

### Exercise 1

Write a function called `has_duplicates` that takes a list and returns `true` if any element appears more than once. It should not modify the original list.

### Exercise 2

Write a function called `word_frequency` that takes a string and returns a dictionary that maps each word to the number of times it appears. Convert the string to lowercase and remove punctuation before counting.

### Exercise 3

Write a function called `unique_words` that takes a list of words and returns a list of the unique words in alphabetical order, using a `HashSet`.

### Exercise 4

Python's `dict` has a method called `setdefault` that sets a value in a dictionary only if the key is not already present. The equivalent in Auto is:

```auto
let mut d: HashMap<str, [int]> = {}
// Instead of d.setdefault(key, []).append(value):
if key not in d {
    d[key] = []
}
d[key].append(value)
```

Use this pattern to write a function called `invert_dict` that takes a dictionary and returns a new dictionary where the keys and values are swapped. If the original dictionary has duplicate values, the inverted dictionary should map each value to a list of keys.
