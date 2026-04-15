# Tuples

This chapter introduces one more built-in type, the tuple, and then shows how lists, dictionaries, and tuples work together. It also presents tuple assignment and a useful feature for functions with variable-length argument lists.

In the exercises, we'll use tuples, along with lists and dictionaries, to solve more word puzzles and implement efficient algorithms.

## Tuples are like lists

A tuple is a sequence of values. The values can be any type, and they are indexed by integers, so tuples are a lot like lists. The important difference is that tuples are immutable.

To create a tuple, you can write a comma-separated list of values enclosed in parentheses.

```auto
let t: Tuple = ('l', 'u', 'p', 'i', 'n')
print(type(t))  // Tuple
```

To create a tuple with a single element, you have to include a final comma.

```auto
let t1: Tuple = ('p',)
```

Another way to create a tuple is the built-in `Tuple` type. With no argument, it creates an empty tuple. If the argument is a sequence, the result is a tuple with the elements of the sequence.

```auto
let t: Tuple = Tuple("lupin")
print(t)  // ('l', 'u', 'p', 'i', 'n')
```

Most list operators also work with tuples. For example, the bracket operator indexes an element.

```auto
print(t[0])  // 'l'
```

And the slice operator selects a range of elements.

```auto
print(t[1:3])  // ('u', 'p')
```

The `+` operator concatenates tuples.

```auto
print(Tuple("lup") + ('i', 'n'))  // ('l', 'u', 'p', 'i', 'n')
```

The `sorted` function works with tuples -- but the result is a list, not a tuple.

```auto
let s = sorted(t)
print(s)  // ['i', 'l', 'n', 'p', 'u']
```

> **Note for Python Programmers:**
>
> Auto uses `Tuple` (capitalized) instead of Python's `tuple`. The `a2p` transpiler converts `Tuple` to `tuple` automatically.

## Tuples are immutable

If you try to modify a tuple with the bracket operator, you get an error. Tuples don't have any of the methods that modify lists, like `append` and `remove`.

Because tuples are immutable, they are hashable, which means they can be used as keys in a dictionary. For example, the following dictionary contains two tuples as keys that map to integers.

```auto
let mut d: HashMap<Tuple, int> = {}
d[(1, 2)] = 3
d[(3, 4)] = 7
print(d[(1, 2)])  // 3
```

Or if we have a variable that refers to a tuple, we can use it as a key.

```auto
let t: Tuple = (3, 4)
print(d[t])  // 7
```

Tuples can also appear as values in a dictionary.

```auto
let d: HashMap<str, Tuple> = {"key": ('a', 'b', 'c')}
print(d)  // {"key": ('a', 'b', 'c')}
```

<Listing number="11-1" file-name="tuple_basics.auto" caption="Tuple creation and indexing">

```auto
fn main() {
    // Creating tuples
    let t: Tuple = ('l', 'u', 'p', 'i', 'n')
    print("Tuple:", t)

    // Tuple from a string
    let t2: Tuple = Tuple("hello")
    print("Tuple from string:", t2)

    // Single-element tuple
    let single: Tuple = ('p',)
    print("Single element:", single)

    // Indexing
    print("First element:", t[0])
    print("Last element:", t[-1])

    // Slicing
    print("Slice [1:3]:", t[1:3])

    // Concatenation
    let combined = Tuple("lup") + ('i', 'n')
    print("Concatenated:", combined)

    // Length
    print("Length:", len(t))

    // Sorted (returns a list)
    print("Sorted:", sorted(t))

    // Tuple as dictionary key
    let mut d: HashMap<Tuple, int> = {}
    d[(1, 2)] = 3
    d[(3, 4)] = 7
    print("Dict with tuple keys:", d)
    print("d[(1, 2)]:", d[(1, 2)])
}
```

```python
def main():
    # Creating tuples
    t = ('l', 'u', 'p', 'i', 'n')
    print(f"Tuple: {t}")

    # Tuple from a string
    t2 = tuple("hello")
    print(f"Tuple from string: {t2}")

    # Single-element tuple
    single = ('p',)
    print(f"Single element: {single}")

    # Indexing
    print(f"First element: {t[0]}")
    print(f"Last element: {t[-1]}")

    # Slicing
    print(f"Slice [1:3]: {t[1:3]}")

    # Concatenation
    combined = tuple("lup") + ('i', 'n')
    print(f"Concatenated: {combined}")

    # Length
    print(f"Length: {len(t)}")

    # Sorted (returns a list)
    print(f"Sorted: {sorted(t)}")

    # Tuple as dictionary key
    d = {}
    d[(1, 2)] = 3
    d[(3, 4)] = 7
    print(f"Dict with tuple keys: {d}")
    print(f"d[(1, 2)]: {d[(1, 2)]}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

Tuples are created with parentheses containing comma-separated values. A single-element tuple requires a trailing comma to distinguish it from a parenthesized expression. The `Tuple()` constructor can convert other sequences (like strings) into tuples.

Like lists, tuples support indexing, slicing, concatenation, and `len()`. Unlike lists, tuples are immutable -- you cannot modify elements, append, or remove. This immutability makes tuples hashable, so they can be used as dictionary keys, as shown in the last section of the example.

## Tuple assignment

You can put a tuple of variables on the left side of an assignment, and a tuple of values on the right.

```auto
let (a, b) = (1, 2)
print(a, b)  // 1 2
```

The values are assigned to the variables from left to right. More generally, if the left side of an assignment is a tuple, the right side can be any kind of sequence -- string, list or tuple. For example, to split an email address into a user name and a domain, you could write:

```auto
let email = "monty@python.org"
let (username, domain) = email.split("@")
print(username)  // "monty"
print(domain)    // "python.org"
```

Tuple assignment is useful if you want to swap the values of two variables.

```auto
let mut (a, b) = (1, 2)
let (a, b) = (b, a)
print(a, b)  // 2 1
```

We can also use tuple assignment in a `for` statement. For example, to loop through the items in a dictionary, we can use the `items` method.

```auto
let d: HashMap<str, int> = {"one": 1, "two": 2}
for (key, value) in d.items() {
    print(f"$key -> $value")
}
```

Each time through the loop, a key and the corresponding value are assigned directly to `key` and `value`.

## Tuples as return values

Strictly speaking, a function can only return one value, but if the value is a tuple, the effect is the same as returning multiple values.

The built-in function `divmod` takes two arguments and returns a tuple of two values, the quotient and remainder.

```auto
let result: Tuple = divmod(7, 3)
print(result)  // (2, 1)
```

We can use tuple assignment to store the elements of the tuple in two variables.

```auto
let (quotient, remainder) = divmod(7, 3)
print(quotient)   // 2
print(remainder)  // 1
```

Here is an example of a function that returns a tuple.

```auto
fn min_max(t: Tuple) -> Tuple {
    return (min(t), max(t))
}
```

`max` and `min` are built-in functions that find the largest and smallest elements of a sequence. `min_max` computes both and returns a tuple of two values.

<Listing number="11-2" file-name="tuple_assign.auto" caption="Tuple assignment and return values">

```auto
fn min_max(t: Tuple) -> Tuple {
    return (min(t), max(t))
}

fn swap(a: int, b: int) -> Tuple {
    return (b, a)
}

fn main() {
    // Tuple assignment
    let (x, y) = (10, 20)
    print("x:", x, "y:", y)

    // Splitting a string with tuple assignment
    let email = "monty@python.org"
    let (username, domain) = email.split("@")
    print("Username:", username)
    print("Domain:", domain)

    // Swapping variables
    let mut (a, b) = (3, 7)
    print("Before swap: a =", a, "b =", b)
    let (a, b) = swap(a, b)
    print("After swap:  a =", a, "b =", b)

    // divmod -- returning a tuple
    let (quotient, remainder) = divmod(17, 5)
    print("17 / 5 =", quotient, "remainder", remainder)

    // Function returning a tuple
    let numbers: Tuple = (4, 1, 7, 2, 9, 3)
    let (low, high) = min_max(numbers)
    print("Numbers:", numbers)
    print("Min:", low, "Max:", high)

    // Iterating dictionary items with tuple assignment
    let scores: HashMap<str, int> = {"Alice": 95, "Bob": 87, "Charlie": 92}
    print("Scores:")
    for (name, score) in scores.items() {
        print(f"  $name: $score")
    }
}
```

```python
def min_max(t):
    return (min(t), max(t))


def swap(a, b):
    return (b, a)


def main():
    # Tuple assignment
    x, y = 10, 20
    print(f"x: {x} y: {y}")

    # Splitting a string with tuple assignment
    email = "monty@python.org"
    username, domain = email.split("@")
    print(f"Username: {username}")
    print(f"Domain: {domain}")

    # Swapping variables
    a, b = 3, 7
    print(f"Before swap: a = {a} b = {b}")
    a, b = swap(a, b)
    print(f"After swap:  a = {a} b = {b}")

    # divmod -- returning a tuple
    quotient, remainder = divmod(17, 5)
    print(f"17 / 5 = {quotient} remainder {remainder}")

    # Function returning a tuple
    numbers = (4, 1, 7, 2, 9, 3)
    low, high = min_max(numbers)
    print(f"Numbers: {numbers}")
    print(f"Min: {low} Max: {high}")

    # Iterating dictionary items with tuple assignment
    scores = {"Alice": 95, "Bob": 87, "Charlie": 92}
    print("Scores:")
    for name, score in scores.items():
        print(f"  {name}: {score}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

Tuple assignment lets you assign multiple variables at once. The number of variables on the left must match the number of values on the right. This is particularly useful for functions that return multiple values, like `divmod` or our custom `min_max`.

The `swap` function demonstrates a common pattern: returning a tuple and using tuple assignment to unpack it. When iterating over `d.items()`, each iteration yields a key-value pair that we can destructure directly in the `for` loop header.

## Zip

Tuples are useful for looping through the elements of two sequences and performing operations on corresponding elements. For example, suppose two teams play a series of seven games, and we record their scores in two lists.

```auto
let scores1: List<int> = [1, 2, 4, 5, 1, 5, 2]
let scores2: List<int> = [5, 5, 2, 2, 5, 2, 3]
```

We'll use `zip`, which is a built-in function that takes two or more sequences and pairs up the elements.

```auto
let mut wins = 0
for (team1, team2) in zip(scores1, scores2) {
    if team1 > team2 {
        wins += 1
    }
}
print("Team 1 wins:", wins)  // 3
```

If you have a list of keys and a list of values, you can use `zip` and `dict` to make a dictionary.

```auto
let letters = "abcdefghijklmnopqrstuvwxyz"
let numbers = 0..len(letters)
let letter_map: HashMap<str, int> = dict(zip(letters, numbers))
print(letter_map["a"])  // 0
print(letter_map["z"])  // 25
```

## Comparing and sorting

The relational operators work with tuples and other sequences. For example, if you use the `<` operator with tuples, it starts by comparing the first element from each sequence. If they are equal, it goes on to the next pair of elements, and so on.

```auto
print((0, 1, 2) < (0, 3, 4))         // true
print((0, 1, 2000000) < (0, 3, 4))    // true
```

This way of comparing tuples is useful for sorting a list of tuples, or finding the minimum or maximum. You can use the `sorted` function with a `key` parameter to control the sort order.

## Inverting a dictionary

Suppose you want to invert a dictionary so you can look up a value and get the corresponding key. But there's a problem -- the keys in a dictionary have to be unique, but the values don't.

So one way to invert a dictionary is to create a new dictionary where the values are lists of keys from the original. The following function takes a dictionary and returns its inverse as a new dictionary.

```auto
fn invert_dict(d: HashMap<str, int>) -> HashMap<int, List<str>> {
    let mut new: HashMap<int, List<str>> = {}
    for (key, value) in d.items() {
        if !new.contains_key(value) {
            new[value] = [key]
        } else {
            new[value].append(key)
        }
    }
    return new
}
```

We can test it like this:

```auto
let d: HashMap<str, int> = value_counts("parrot")
print(d)           // {"p": 1, "a": 1, "r": 2, "o": 1, "t": 1}
print(invert_dict(d))  // {1: ["p", "a", "o", "t"], 2: ["r"]}
```

This is the first example we've seen where the values in the dictionary are lists. We will see more!

<Listing number="11-3" file-name="tuple_zip.auto" caption="Zip and dictionary inversion">

```auto
fn value_counts(string: str) -> HashMap<str, int> {
    let mut counter: HashMap<str, int> = {}
    for letter in string {
        if !counter.contains_key(letter) {
            counter[letter] = 1
        } else {
            counter[letter] += 1
        }
    }
    return counter
}

fn invert_dict(d: HashMap<str, int>) -> HashMap<int, List<str>> {
    let mut new: HashMap<int, List<str>> = {}
    for (key, value) in d.items() {
        if !new.contains_key(value) {
            new[value] = [key]
        } else {
            new[value].append(key)
        }
    }
    return new
}

fn main() {
    // Zip: pairing elements from two sequences
    let names: List<str> = ["Alice", "Bob", "Charlie", "Diana"]
    let scores: List<int> = [95, 87, 92, 88]
    print("Zipped pairs:")
    for (name, score) in zip(names, scores) {
        print(f"  $name: $score")
    }

    // Building a dictionary from two lists with zip
    let letters = "abcde"
    let values = [10, 20, 30, 40, 50]
    let letter_values: HashMap<str, int> = dict(zip(letters, values))
    print("Letter values:", letter_values)

    // Enumerate: pairing elements with their indices
    print("Enumerated:")
    for (index, letter) in enumerate("hello") {
        print(f"  $index: $letter")
    }

    // Dictionary inversion
    let d = value_counts("parrot")
    print("Original:", d)
    let inverted = invert_dict(d)
    print("Inverted:", inverted)

    // Comparing tuples
    print((0, 1, 2) < (0, 3, 4))         // true
    print((0, 1, 2000000) < (0, 3, 4))    // true
}
```

```python
def value_counts(string):
    counter = {}
    for letter in string:
        if letter not in counter:
            counter[letter] = 1
        else:
            counter[letter] += 1
    return counter


def invert_dict(d):
    new = {}
    for key, value in d.items():
        if value not in new:
            new[value] = [key]
        else:
            new[value].append(key)
    return new


def main():
    # Zip: pairing elements from two sequences
    names = ["Alice", "Bob", "Charlie", "Diana"]
    scores = [95, 87, 92, 88]
    print("Zipped pairs:")
    for name, score in zip(names, scores):
        print(f"  {name}: {score}")

    # Building a dictionary from two lists with zip
    letters = "abcde"
    values = [10, 20, 30, 40, 50]
    letter_values = dict(zip(letters, values))
    print(f"Letter values: {letter_values}")

    # Enumerate: pairing elements with their indices
    print("Enumerated:")
    for index, letter in enumerate("hello"):
        print(f"  {index}: {letter}")

    # Dictionary inversion
    d = value_counts("parrot")
    print(f"Original: {d}")
    inverted = invert_dict(d)
    print(f"Inverted: {inverted}")

    # Comparing tuples
    print((0, 1, 2) < (0, 3, 4))
    print((0, 1, 2000000) < (0, 3, 4))


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`zip` pairs up elements from two (or more) sequences, producing an iterator of tuples. This is useful for iterating over corresponding elements -- for example, matching names with scores. When combined with `dict()`, `zip` can build a dictionary from separate lists of keys and values.

`enumerate` is a special case of `zip` that pairs each element with its index. It's a common pattern when you need both the position and the value of each element.

`invert_dict` demonstrates a classic pattern: swapping the roles of keys and values in a dictionary. Since values may not be unique, the inverted dictionary maps each original value to a *list* of keys that had that value.

## Debugging

Lists, dictionaries and tuples are **data structures**. In this chapter we are starting to see compound data structures, like lists of tuples, or dictionaries that contain tuples as keys and lists as values. Compound data structures are useful, but they are prone to errors caused when a data structure has the wrong type, size, or structure.

To help debug these kinds of errors, it is often enough to print the type and structure of a value. For dictionaries, printing the number of items and a few sample entries can help verify that the data looks right.

## Glossary

**tuple:**
An immutable sequence of values.

**tuple assignment:**
An assignment with a tuple on the left side and a sequence on the right. The right side is unpacked and the elements are assigned to the variables on the left.

**pack:**
Collect multiple arguments into a tuple.

**unpack:**
Treat a tuple (or other sequence) as multiple arguments.

**zip object:**
The result of calling the built-in function `zip`, can be used to loop through a sequence of tuples.

**enumerate object:**
The result of calling the built-in function `enumerate`, can be used to loop through a sequence of index-element tuples.

**sort key:**
A value, or function that computes a value, used to sort the elements of a collection.

**data structure:**
A collection of values, organized to perform certain operations efficiently.

## Exercises

### Exercise

If a tuple contains a mutable value, like a list, the tuple is no longer hashable. Write a line of code that appends a value to a list inside a tuple, then confirm that the tuple cannot be used as a dictionary key.

### Exercise

Write a function called `shift_word` that takes a string and an integer, and returns a new string with each letter shifted by the given number of places in the alphabet. Use the modulus operator to wrap around from `'z'` back to `'a'`.

### Exercise

Write a function called `most_frequent_letters` that takes a string and prints the letters in decreasing order of frequency.

### Exercise

Write a program that takes a list of words and prints all the sets of words that are anagrams. Hint: For each word, sort the letters and join them back into a string. Make a dictionary that maps from this sorted string to a list of anagrams.

### Exercise

Write a function called `word_distance` that takes two words with the same length and returns the number of places where the two words differ. Hint: Use `zip` to loop through the corresponding letters.
