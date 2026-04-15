# Dictionaries

This chapter presents a built-in type called a dictionary (called `HashMap` in Auto, `dict` in Python). It is one of the best features of both languages -- and the building block of many efficient and elegant algorithms.

We'll use dictionaries to compute the number of unique words in a book and the number of times each one appears. And in the exercises, we'll use dictionaries to solve word puzzles.

## A dictionary is a mapping

A **dictionary** is like a list, but more general. In a list, the indices have to be integers; in a dictionary they can be (almost) any type. For example, suppose we make a list of number words, like this.

```auto
let lst = ["zero", "one", "two"]
```

We can use an integer as an index to get the corresponding word.

```auto
print(lst[1])  // "one"
```

But suppose we want to go in the other direction, and look up a word to get the corresponding integer. We can't do that with a list, but we can with a dictionary. We'll start by creating an empty dictionary and assigning it to `numbers`.

```auto
let mut numbers: HashMap<str, int> = {}
```

In Auto, dictionaries are created with the `HashMap` type, which maps keys of one type to values of another. The `{}` syntax creates an empty dictionary.

To add items to the dictionary, we'll use square brackets.

```auto
numbers["zero"] = 0
```

This assignment adds to the dictionary an **item**, which represents the association of a **key** and a **value**. In this example, the key is the string `"zero"` and the value is the integer `0`.

We can add more items like this.

```auto
numbers["one"] = 1
numbers["two"] = 2
print(numbers)  // {"zero": 0, "one": 1, "two": 2}
```

To look up a key and get the corresponding value, we use the bracket operator.

```auto
print(numbers["two"])  // 2
```

The `len` function works on dictionaries; it returns the number of items.

```auto
print(len(numbers))  // 3
```

In mathematical language, a dictionary represents a **mapping** from keys to values, so you can also say that each key "maps to" a value.

> **Note for Python Programmers:**
>
> Auto uses `HashMap<K, V>` where Python uses `dict`. The `a2p` transpiler converts `HashMap` to `dict` automatically. Auto uses `len()` the same way as Python.

## Creating dictionaries

In the previous section we created an empty dictionary and added items one at a time using the bracket operator. Instead, we could have created the dictionary all at once like this.

```auto
let numbers: HashMap<str, int> = {"zero": 0, "one": 1, "two": 2}
```

Each item consists of a key and a value separated by a colon. The items are separated by commas and enclosed in curly braces.

We can also make a copy of a dictionary like this.

```auto
let numbers_copy: HashMap<str, int> = HashMap::copy(numbers)
```

It is often useful to make a copy before performing operations that modify dictionaries.

## The `in` operator

In Auto, the `contains_key` method checks whether a key exists in a dictionary. In Python, the `in` operator does this.

```auto
print(numbers.contains_key("one"))  // true
```

The `contains_key` method checks whether something appears as a *key* in the dictionary. To check whether something appears as a *value*, you would need to iterate through the values.

The items in a dictionary are stored in a **hash table**, which is a way of organizing data that has a remarkable property: looking up a key takes about the same amount of time no matter how many items are in the dictionary. That makes it possible to write some remarkably efficient algorithms.

> **Note for Python Programmers:**
>
> Auto uses `d.contains_key("key")` where Python uses `"key" in d`. The `a2p` transpiler converts this automatically. Auto also supports `d.get("key", default)` just like Python.

<Listing number="10-1" file-name="dict_basics.auto" caption="Creating and accessing dictionaries">

```auto
fn main() {
    // Creating an empty dictionary
    let mut numbers: HashMap<str, int> = {}
    numbers["zero"] = 0
    numbers["one"] = 1
    numbers["two"] = 2
    print("numbers:", numbers)

    // Creating a dictionary all at once
    let scores: HashMap<str, int> = {"Alice": 95, "Bob": 87, "Charlie": 92}
    print("scores:", scores)

    // Accessing values
    print("Alice's score:", scores["Alice"])
    print("Length of scores:", len(scores))

    // Checking if a key exists
    print("Contains 'Alice':", scores.contains_key("Alice"))
    print("Contains 'David':", scores.contains_key("David"))

    // Using get with a default value
    print("Eve's score:", scores.get("Eve", 0))
    print("Bob's score:", scores.get("Bob", 0))
}
```

```python
def main():
    # Creating an empty dictionary
    numbers = {}
    numbers["zero"] = 0
    numbers["one"] = 1
    numbers["two"] = 2
    print(f"numbers: {numbers}")

    # Creating a dictionary all at once
    scores = {"Alice": 95, "Bob": 87, "Charlie": 92}
    print(f"scores: {scores}")

    # Accessing values
    print(f"Alice's score: {scores['Alice']}")
    print(f"Length of scores: {len(scores)}")

    # Checking if a key exists
    print(f"Contains 'Alice': {'Alice' in scores}")
    print(f"Contains 'David': {'David' in scores}")

    # Using get with a default value
    print(f"Eve's score: {scores.get('Eve', 0)}")
    print(f"Bob's score: {scores.get('Bob', 0)}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The first section demonstrates creating a dictionary incrementally: start with an empty `HashMap<str, int>` and add items using bracket notation. The second shows the literal syntax for creating a dictionary with initial values.

Accessing values uses the same bracket notation. `len()` returns the number of items. The `contains_key` method (Python: `in` operator) checks for key existence. The `get` method returns the value for a key if it exists, or a default value otherwise -- this avoids errors when looking up keys that might not be present.

## A collection of counters

Suppose you are given a string and you want to count how many times each letter appears. A dictionary is a good tool for this job. We'll start with an empty dictionary.

```auto
let mut counter: HashMap<str, int> = {}
```

As we loop through the letters in the string, suppose we see the letter `'a'` for the first time. We can add it to the dictionary like this.

```auto
counter["a"] = 1
```

Later, if we see the same letter again, we can increment the counter like this.

```auto
counter["a"] += 1
```

The following function uses these features to count the number of times each letter appears in a string.

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
```

Each time through the loop, if `letter` is not in the dictionary, we create a new item with key `letter` and value `1`. If `letter` is already in the dictionary we increment the value associated with `letter`.

Here's an example.

```auto
let counter = value_counts("brontosaurus")
print(counter)  // {"b": 1, "r": 2, "o": 2, "n": 1, "t": 1, "s": 2, "a": 1, "u": 1}
```

## Looping and dictionaries

If you use a dictionary in a `for` statement, it traverses the keys of the dictionary. To demonstrate, let's make a dictionary that counts the letters in `"banana"`.

```auto
let counter = value_counts("banana")
```

The following loop prints the keys, which are the letters.

```auto
for key in counter.keys() {
    print(key)
}
```

To print the values, we can use the `values` method.

```auto
for value in counter.values() {
    print(value)
}
```

To print the keys and values, we can loop through the keys and look up the corresponding values.

```auto
for key in counter.keys() {
    let value = counter[key]
    print(key, value)
}
```

In the next chapter, we'll see a more concise way to do the same thing using tuples.

<Listing number="10-2" file-name="dict_looping.auto" caption="Looping and counting with dictionaries">

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

fn main() {
    // Counting letters in a word
    let counter = value_counts("brontosaurus")
    print("Letter counts:", counter)
    print("Number of unique letters:", len(counter))

    // Looping through keys
    print("Keys:")
    for key in counter.keys() {
        print(key, end=" ")
    }
    print()

    // Looping through values
    print("Values:")
    for value in counter.values() {
        print(value, end=" ")
    }
    print()

    // Looping through keys and values
    print("Key-value pairs:")
    for key in counter.keys() {
        let value = counter[key]
        print(f"$key: $value")
    }

    // Building a dictionary from a list
    let words = ["apple", "banana", "cherry", "date", "elderberry"]
    let mut word_lengths: HashMap<str, int> = {}
    for word in words {
        word_lengths[word] = len(word)
    }
    print("Word lengths:", word_lengths)
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


def main():
    # Counting letters in a word
    counter = value_counts("brontosaurus")
    print(f"Letter counts: {counter}")
    print(f"Number of unique letters: {len(counter)}")

    # Looping through keys
    print("Keys:")
    for key in counter:
        print(key, end=" ")
    print()

    # Looping through values
    print("Values:")
    for value in counter.values():
        print(value, end=" ")
    print()

    # Looping through keys and values
    print("Key-value pairs:")
    for key in counter:
        value = counter[key]
        print(f"{key}: {value}")

    # Building a dictionary from a list
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    word_lengths = {}
    for word in words:
        word_lengths[word] = len(word)
    print(f"Word lengths: {word_lengths}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`value_counts` demonstrates the histogram pattern: initialize an empty dictionary, loop through each element, and either create a new entry or increment an existing one. This is one of the most common uses of dictionaries.

The three looping patterns show different ways to traverse a dictionary: by keys only, by values only, and by key-value pairs (looking up each value from its key). The final example shows the accumulator pattern applied to dictionaries -- building a new dictionary by mapping each element of a list to a computed value.

## Lists and dictionaries

You can put a list in a dictionary as a value. For example, here's a dictionary that maps from the number `4` to a list of four letters.

```auto
let d: HashMap<int, List<str>> = {4: ["r", "o", "u", "s"]}
```

But you can't put a list in a dictionary as a key. Dictionaries use hash tables, and that means that the keys have to be **hashable**. Since lists are mutable, they are not hashable and cannot be used as keys.

Since dictionaries are mutable, they can't be used as keys either. But they *can* be used as values.

## Accumulating a list

For many programming tasks, it is useful to loop through one list or dictionary while building another. As an example, we'll loop through the words in a dictionary and make a list of palindromes -- that is, words that are spelled the same backward and forward, like "noon" and "rotator".

```auto
fn is_palindrome(word: str) -> bool {
    return word == word.reversed()
}
```

We can use a similar pattern to make a list of palindromes.

```auto
let mut palindromes: List<str> = []
for word in word_dict.keys() {
    if is_palindrome(word) {
        palindromes.append(word)
    }
}
```

In this loop, `palindromes` is used as an **accumulator**, which is a variable that collects or accumulates data during a computation.

Looping through a list like this, selecting some elements and omitting others, is called **filtering**.

## Memos

If you ran the `fibonacci` function from Chapter 6, maybe you noticed that the bigger the argument you provide, the longer the function takes to run. Furthermore, the run time increases quickly.

```auto
fn fibonacci(n: int) -> int {
    if n == 0 {
        return 0
    }
    if n == 1 {
        return 1
    }
    return fibonacci(n - 1) + fibonacci(n - 2)
}
```

One solution is to keep track of values that have already been computed by storing them in a dictionary. A previously computed value that is stored for later use is called a **memo**. Here is a "memoized" version of `fibonacci`:

```auto
let mut known: HashMap<int, int> = {0: 0, 1: 1}

fn fibonacci_memo(n: int) -> int {
    if known.contains_key(n) {
        return known[n]
    }
    let res = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    known[n] = res
    return res
}
```

`known` is a dictionary that keeps track of the Fibonacci numbers we already know. It starts with two items: `0` maps to `0` and `1` maps to `1`.

Whenever `fibonacci_memo` is called, it checks `known`. If the result is already there, it can return immediately. Otherwise it has to compute the new value, add it to the dictionary, and return it.

Comparing the two functions, `fibonacci(40)` takes about 30 seconds to run. `fibonacci_memo(40)` takes about 30 microseconds, so it's a million times faster.

<Listing number="10-3" file-name="dict_memo.auto" caption="Memoization with Fibonacci">

```auto
let mut known: HashMap<int, int> = {0: 0, 1: 1}

fn fibonacci_memo(n: int) -> int {
    if known.contains_key(n) {
        return known[n]
    }
    let res = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    known[n] = res
    return res
}

fn main() {
    // Computing Fibonacci numbers with memoization
    print("Fibonacci numbers with memoization:")
    for i in 0..=10 {
        print(f"fib($i) = ${fibonacci_memo(i)}")
    }

    // Large Fibonacci number -- fast with memoization
    print()
    print("fib(40) =", fibonacci_memo(40))

    // Show what's in the cache
    print()
    print("Cache contains", len(known), "entries")

    // Demonstrate reusing the cache
    print("fib(35) from cache:", known[35])
}
```

```python
known = {0: 0, 1: 1}


def fibonacci_memo(n):
    if n in known:
        return known[n]
    res = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    known[n] = res
    return res


def main():
    # Computing Fibonacci numbers with memoization
    print("Fibonacci numbers with memoization:")
    for i in range(11):
        print(f"fib({i}) = {fibonacci_memo(i)}")

    # Large Fibonacci number -- fast with memoization
    print()
    print(f"fib(40) = {fibonacci_memo(40)}")

    # Show what's in the cache
    print()
    print(f"Cache contains {len(known)} entries")

    # Demonstrate reusing the cache
    print(f"fib(35) from cache: {known[35]}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

Memoization is a powerful optimization technique. The `known` dictionary stores previously computed Fibonacci numbers. Before computing `fibonacci_memo(n)`, the function checks whether the result is already in the cache. If it is, the function returns immediately -- no recursive calls needed.

Without memoization, `fibonacci(40)` makes about 330 million recursive calls. With memoization, it makes only 39 calls (one for each number from 2 to 40). This is the difference between seconds and microseconds.

The key insight is that the dictionary lookup takes constant time, regardless of how many items are stored. So checking `known.contains_key(n)` is essentially free compared to the cost of recursive computation.

## Debugging

As you work with bigger datasets it can become unwieldy to debug by printing and checking the output by hand. Here are some suggestions for debugging large datasets:

1. **Scale down the input**: If possible, reduce the size of the dataset. For example, if the program reads a text file, start with just the first 10 lines, or with the smallest example you can find. If there is an error, you can reduce the size to the smallest value where the error occurs. As you find and correct errors, you can increase the size gradually.

2. **Check summaries and types**: Instead of printing and checking the entire dataset, consider printing summaries of the data -- for example, the number of items in a dictionary or the total of a list of numbers. A common cause of runtime errors is a value that is not the right type.

3. **Write self-checks**: Sometimes you can write code to check for errors automatically. For example, if you are computing the average of a list of numbers, you could check that the result is not greater than the largest element in the list or less than the smallest. This is called a "sanity check." Another kind of check compares the results of two different computations to see if they are consistent -- a "consistency check."

4. **Format the output**: Formatting debugging output can make it easier to spot an error. Time you spend building scaffolding can reduce the time you spend debugging.

## Glossary

**dictionary:**
An object that contains key-value pairs, also called items. In Auto, the type is `HashMap`; in Python, it is `dict`.

**item:**
In a dictionary, another name for a key-value pair.

**key:**
An object that appears in a dictionary as the first part of a key-value pair.

**value:**
An object that appears in a dictionary as the second part of a key-value pair.

**mapping:**
A relationship in which each element of one set corresponds to an element of another set.

**hash table:**
A collection of key-value pairs organized so that we can look up a key and find its value efficiently.

**hashable:**
Immutable types like integers, floats and strings are hashable. Mutable types like lists and dictionaries are not.

**accumulator:**
A variable used in a loop to add up or accumulate a result.

**filtering:**
Looping through a sequence and selecting or omitting elements.

**call graph:**
A diagram that shows every frame created during the execution of a program, with an arrow from each caller to each callee.

**memo:**
A computed value stored to avoid unnecessary future computation.

## Exercises

### Exercise

Write a more concise version of `value_counts` using the `get` method. You should be able to eliminate the `if` statement.

### Exercise

Write a function named `has_duplicates` that takes a sequence -- like a list or string -- as a parameter and returns `true` if there is any element that appears in the sequence more than once.

### Exercise

Write a function called `find_repeats` that takes a dictionary that maps from each key to a counter, like the result from `value_counts`. It should loop through the dictionary and return a list of keys that have counts greater than `1`.

### Exercise

Suppose you run `value_counts` with two different words and save the results in two dictionaries. Write a function called `add_counters` that takes two dictionaries like this and returns a new dictionary that contains all of the letters and the total number of times they appear in either word.

### Exercise

A word is "interlocking" if we can split it into two words by taking alternating letters. For example, "schooled" is an interlocking word because it can be split into "shoe" and "cold". Write a function called `is_interlocking` that takes a word as an argument and returns `true` if it can be split into two interlocking words.
