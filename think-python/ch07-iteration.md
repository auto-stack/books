# Iteration and Search

In 1939 Ernest Vincent Wright published a 50,000 word novel called *Gadsby* that does not contain the letter "e". Since "e" is the most common letter in English, writing even a few words without using it is difficult.

To get a sense of how difficult, in this chapter we'll compute the fraction of English words that have at least one "e". For that, we'll use `for` loops to iterate through the letters in a string, and we'll update variables in a loop to count occurrences. We'll use the `in` operator to check whether a letter appears in a word, and you'll learn a programming pattern called a "linear search".

## Loops and strings

In Chapter 3 we saw a `for` loop that uses a range expression to display a sequence of numbers:

```auto
for i in 0..3 {
    print(i, end=" ")
}
```

We can also use a `for` loop to iterate through the letters in a string:

```auto
for letter in "Gadsby" {
    print(letter, end=" ")
}
```

The variable defined in a `for` loop is called the **loop variable**. In this example, we changed the name from `i` to `letter`, which provides more information about the value it refers to.

Now that we can loop through the letters in a word, we can check whether it contains the letter "e". Here's a function that returns `true` if the word contains an "e" and `false` otherwise:

```auto
fn has_e(word: str) -> bool {
    for letter in word {
        if letter == 'E' || letter == 'e' {
            return true
        }
    }
    return false
}
```

This function loops through each letter in the word. If it finds an 'E' or 'e', it returns `true` immediately. If it gets through the entire loop without finding one, it returns `false`.

> **Note for Python Programmers:**
>
> Auto uses `||` instead of Python's `or`. The `a2p` transpiler converts `||` to `or` automatically.

<Listing number="7-1" file-name="loop_strings.auto" caption="Looping over strings and checking for letters">

```auto
fn has_e(word: str) -> bool {
    for letter in word {
        if letter == 'E' || letter == 'e' {
            return true
        }
    }
    return false
}

fn main() {
    // Looping over characters in a string
    print("Letters in Gadsby:")
    for letter in "Gadsby" {
        print(letter, end=" ")
    }
    print()

    // Checking for 'e' in a word
    print("has_e('Gadsby'):", has_e("Gadsby"))
    print("has_e('Emma'):", has_e("Emma"))
    print("has_e('hello'):", has_e("hello"))
    print("has_e('world'):", has_e("world"))
}
```

```python
def has_e(word):
    for letter in word:
        if letter == "E" or letter == "e":
            return True
    return False


def main():
    # Looping over characters in a string
    print("Letters in Gadsby:")
    for letter in "Gadsby":
        print(letter, end=" ")
    print()

    # Checking for 'e' in a word
    print(f"has_e('Gadsby'): {has_e('Gadsby')}")
    print(f"has_e('Emma'): {has_e('Emma')}")
    print(f"has_e('hello'): {has_e('hello')}")
    print(f"has_e('world'): {has_e('world')}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The first loop iterates over each character in the string `"Gadsby"` and prints it with a space separator. The `end=" "` argument to `print` prevents a newline after each character.

The `has_e` function demonstrates an early-return pattern: it loops through each letter and returns `true` as soon as it finds a match. If the loop completes without finding a match, the function returns `false`. Notice that the second `return` is outside the loop -- a common mistake is to put both `return` statements inside the loop, which would only check the first letter.

## Reading the word list

To see how many words contain an "e", we'll need a word list. In Python, we can use the `open` function to read a file, and then use a `for` loop to process each line.

In Auto, file I/O works similarly. Here's the basic pattern for reading lines from a file:

```auto
for line in open("words.txt") {
    let word = line.strip()
    print(word)
}
```

The `strip` method removes whitespace characters -- including spaces, tabs, and newlines -- from the beginning and end of the string. This is necessary because each line from the file ends with a newline character.

## Updating variables

As you may have discovered, it is legal to make more than one assignment to the same variable. A new assignment makes an existing variable refer to a new value (and stop referring to the old value).

```auto
let mut x = 5
x = 7
```

A common kind of assignment is an **update**, where the new value of the variable depends on the old:

```auto
let mut x = 7
x = x + 1
```

This statement means "get the current value of `x`, add one, and assign the result back to `x`."

If you try to update a variable that doesn't exist, you get an error, because the expression on the right is evaluated before the assignment on the left. Before you can update a variable, you have to **initialize** it, usually with a simple assignment.

Increasing the value of a variable is called an **increment**; decreasing the value is called a **decrement**. Because these operations are so common, Auto provides **augmented assignment operators** that update a variable more concisely:

```auto
let mut z = 0
z += 2
```

> **Note for Python Programmers:**
>
> Auto requires `let mut` to declare a variable that will be reassigned. The `a2p` transpiler converts `let mut` to a plain assignment. Augmented assignment operators like `+=`, `-=`, and `*=` work the same in both languages.

## Looping and counting

The following program counts the number of words in a word list:

```auto
let mut total = 0

for line in open("words.txt") {
    let word = line.strip()
    total += 1
}
```

It starts by initializing `total` to `0`. Each time through the loop, it increments `total` by `1`. So when the loop exits, `total` refers to the total number of words.

A variable like this, used to count the number of times something happens, is called a **counter**.

<Listing number="7-2" file-name="for_range.auto" caption="For loops with ranges and the accumulator pattern">

```auto
fn main() {
    // for loop with range
    print("Counting from 0 to 4:")
    for i in 0..5 {
        print(i, end=" ")
    }
    print()

    // for loop with step range
    print("Even numbers from 0 to 10:")
    for i in 0..=10 {
        if i % 2 == 0 {
            print(i, end=" ")
        }
    }
    print()

    // for loop over string
    print("Letters in Auto:")
    for letter in "Auto" {
        print(letter, end=" ")
    }
    print()

    // Accumulator pattern: sum from 1 to 10
    let mut total = 0
    for i in 1..=10 {
        total += i
    }
    print("Sum from 1 to 10:", total)
}
```

```python
def main():
    # for loop with range
    print("Counting from 0 to 4:")
    for i in range(5):
        print(i, end=" ")
    print()

    # for loop with step range
    print("Even numbers from 0 to 10:")
    for i in range(11):
        if i % 2 == 0:
            print(i, end=" ")
    print()

    # for loop over string
    print("Letters in Auto:")
    for letter in "Auto":
        print(letter, end=" ")
    print()

    # Accumulator pattern: sum from 1 to 10
    total = 0
    for i in range(1, 11):
        total += i
    print(f"Sum from 1 to 10: {total}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The first loop counts from 0 to 4 using `0..5`. In Auto, `0..5` produces the values 0, 1, 2, 3, 4 (the upper bound is exclusive). The second loop uses `0..=10`, which is an **inclusive range** that includes 10, combined with an `if` statement to filter even numbers.

The third loop iterates over the characters in the string `"Auto"`.

The final example demonstrates the **accumulator pattern**: initialize a variable (`total = 0`), then repeatedly update it inside a loop (`total += i`). This pattern is used constantly in programming for computing sums, counts, and other aggregates.

## The `in` operator

The version of `has_e` we wrote earlier is more complicated than it needs to be. Python provides an operator, `in`, that checks whether a character appears in a string. In Auto, we can use the `contains` method or the `in` operator similarly:

```auto
let word = "Gadsby"
print('e' in word)
```

So we can rewrite `has_e` more simply. And because the conditional of an `if` statement has a boolean value, we can return the boolean directly:

```auto
fn has_e(word: str) -> bool {
    return 'e' in word.to_lowercase()
}
```

The `to_lowercase` method converts the letters in a string to lowercase, making a new string without modifying the original. This way, we only need to check for lowercase 'e'.

## Search

Based on this simpler version of `has_e`, let's write a more general function called `uses_any` that takes a second parameter that is a string of letters. It returns `true` if the word uses any of the letters and `false` otherwise:

```auto
fn uses_any(word: str, letters: str) -> bool {
    for letter in word.to_lowercase() {
        if letters.to_lowercase().contains(letter) {
            return true
        }
    }
    return false
}
```

The structure of `uses_any` is similar to `has_e`. It loops through the letters in `word` and checks them one at a time. If it finds one that appears in `letters`, it returns `true` immediately. If it gets all the way through the loop without finding any, it returns `false`.

This pattern is called a **linear search**.

<Listing number="7-3" file-name="search.auto" caption="Linear search with uses_any and find">

```auto
fn uses_any(word: str, letters: str) -> bool {
    for letter in word.to_lowercase() {
        if letters.to_lowercase().contains(letter) {
            return true
        }
    }
    return false
}

fn find(word: str, letter: str) -> int {
    let mut index = 0
    for ch in word {
        if ch == letter {
            return index
        }
        index += 1
    }
    return -1
}

fn main() {
    // Testing uses_any (linear search)
    print("uses_any('banana', 'aeiou'):", uses_any("banana", "aeiou"))
    print("uses_any('apple', 'xyz'):", uses_any("apple", "xyz"))
    print("uses_any('Banana', 'AEIOU'):", uses_any("Banana", "AEIOU"))

    // Testing find (search for first occurrence)
    print("find('hello', 'l'):", find("hello", "l"))
    print("find('hello', 'o'):", find("hello", "o"))
    print("find('hello', 'z'):", find("hello", "z"))
}
```

```python
def uses_any(word, letters):
    for letter in word.lower():
        if letter in letters.lower():
            return True
    return False


def find(word, letter):
    index = 0
    for ch in word:
        if ch == letter:
            return index
        index += 1
    return -1


def main():
    # Testing uses_any (linear search)
    print(f"uses_any('banana', 'aeiou'): {uses_any('banana', 'aeiou')}")
    print(f"uses_any('apple', 'xyz'): {uses_any('apple', 'xyz')}")
    print(f"uses_any('Banana', 'AEIOU'): {uses_any('Banana', 'AEIOU')}")

    # Testing find (search for first occurrence)
    print(f"find('hello', 'l'): {find('hello', 'l')}")
    print(f"find('hello', 'o'): {find('hello', 'o')}")
    print(f"find('hello', 'z'): {find('hello', 'z')}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`uses_any` converts both `word` and `letters` to lowercase using `to_lowercase()` (which becomes `.lower()` in Python), then performs a linear search: it checks each letter of the word against the allowed letters. As soon as it finds a match, it returns `true`. If no match is found after checking all letters, it returns `false`.

`find` demonstrates another search pattern: it looks for the first occurrence of a specific letter in a word and returns its index. It maintains a counter (`index`) that increments with each iteration. If the letter is found, it returns the current index; if the loop completes without finding the letter, it returns `-1` to indicate "not found".

> **Note for Python Programmers:**
>
> Auto uses `to_lowercase()` instead of Python's `.lower()` method. The `a2p` transpiler converts this automatically. Auto uses `contains()` method or the `in` operator for membership testing, both of which translate to Python's `in` operator.

## Doctest

We can use docstrings to test functions. Here's a version of `uses_any` with a docstring that includes tests:

```python
def uses_any(word, letters):
    """Checks if a word uses any of a list of letters.

    >>> uses_any('banana', 'aeiou')
    True
    >>> uses_any('apple', 'xyz')
    False
    """
    for letter in word.lower():
        if letter in letters.lower():
            return True
    return False
```

Each test begins with `>>>`, which is used as a prompt in some Python environments. The following line indicates the value the expression should have if the function works correctly.

To run these tests, we use the `doctest` module. If all tests pass, no output is displayed -- in that case, no news is good news. If a test fails, the output includes the example that failed, the expected value, and the actual value.

## Counting with accumulators

Let's put together the patterns we've learned. Here's a function that counts how many times a specific letter appears in a word, and then uses it to count how many words in a list contain a particular letter:

<Listing number="7-4" file-name="counting.auto" caption="Counting with the accumulator pattern">

```auto
fn count_letter(word: str, target: str) -> int {
    let mut count = 0
    for letter in word {
        if letter == target {
            count += 1
        }
    }
    return count
}

fn main() {
    // Counting with accumulator pattern
    print("Counting 'l' in 'hello':", count_letter("hello", "l"))
    print("Counting 'e' in 'Emma':", count_letter("Emma", "e"))
    print("Counting 'a' in 'banana':", count_letter("banana", "a"))
    print("Counting 'z' in 'hello':", count_letter("hello", "z"))

    // Counting words with 'e' from a list
    let words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    let mut total = 0
    let mut count_e = 0
    for word in words {
        total += 1
        if count_letter(word, "e") > 0 {
            count_e += 1
        }
    }
    print("Total words:", total)
    print("Words with 'e':", count_e)
    print("Percentage with 'e':", count_e * 100 / total)
}
```

```python
def count_letter(word, target):
    count = 0
    for letter in word:
        if letter == target:
            count += 1
    return count


def main():
    # Counting with accumulator pattern
    print(f"Counting 'l' in 'hello': {count_letter('hello', 'l')}")
    print(f"Counting 'e' in 'Emma': {count_letter('Emma', 'e')}")
    print(f"Counting 'a' in 'banana': {count_letter('banana', 'a')}")
    print(f"Counting 'z' in 'hello': {count_letter('hello', 'z')}")

    # Counting words with 'e' from a list
    words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    total = 0
    count_e = 0
    for word in words:
        total += 1
        if count_letter(word, "e") > 0:
            count_e += 1
    print(f"Total words: {total}")
    print(f"Words with 'e': {count_e}")
    print(f"Percentage with 'e': {count_e * 100 // total}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`count_letter` demonstrates the counter/accumulator pattern: initialize `count` to 0, loop through each letter, increment `count` when a match is found, and return the final count.

In `main()`, we first test `count_letter` with several examples. Then we use it in a larger pattern: we iterate over a list of words, maintaining two counters -- `total` (all words) and `count_e` (words containing 'e'). This demonstrates how the accumulator pattern scales to solve real problems. The percentage calculation shows that about two-thirds of English words contain the letter "e", which explains why it's so difficult to write a book without using it.

## Debugging

When you are debugging a loop, the most common errors are:

- **Off-by-one errors**: The loop runs one time too many or one time too few. This is often caused by confusion about whether the upper bound of a range is inclusive or exclusive.

- **Infinite loops**: If the loop condition is never false, the loop runs forever. In Auto, `for` loops with ranges always terminate, but `for cond {}` loops (which behave like `while` loops) can loop forever if the condition never becomes false.

- **Wrong initialization**: Forgetting to initialize a counter or accumulator before the loop, or initializing it to the wrong value.

- **Scope errors**: Trying to use a loop variable outside the loop, or forgetting that variables created inside a loop don't persist after the loop ends.

## Glossary

**loop variable:**
A variable defined in the header of a `for` loop.

**file object:**
An object that represents an open file and keeps track of which parts of the file have been read or written.

**method:**
A function that is associated with an object and called using the dot operator.

**update:**
An assignment statement that gives a new value to a variable that already exists.

**initialize:**
Create a new variable and give it a value.

**increment:**
Increase the value of a variable.

**decrement:**
Decrease the value of a variable.

**counter:**
A variable used to count something, usually initialized to zero and then incremented.

**accumulator:**
A variable used to accumulate a result, such as a sum or a count.

**linear search:**
A computational pattern that searches through a sequence of elements and stops when it finds what it is looking for.

**pass:**
If a test runs and the result is as expected, the test passes.

**fail:**
If a test runs and the result is not as expected, the test fails.

## Exercises

### Exercise

Write a function named `uses_none` that takes a word and a string of forbidden letters, and returns `true` if the word does not use any of the forbidden letters.

```
uses_none('banana', 'xyz')   // should be true
uses_none('apple', 'efg')    // should be false
```

### Exercise

Write a function called `uses_only` that takes a word and a string of letters, and that returns `true` if the word contains only letters in the string.

```
uses_only('banana', 'ban')   // should be true
uses_only('apple', 'apl')    // should be false
```

### Exercise

Write a function called `uses_all` that takes a word and a string of letters, and that returns `true` if the word contains all of the letters in the string at least once.

```
uses_all('banana', 'ban')   // should be true
uses_all('apple', 'api')    // should be false
```

### Exercise

*The New York Times* publishes a daily puzzle called "Spelling Bee" that challenges readers to spell as many words as possible using only seven letters, where one of the letters is required. The words must have at least four letters.

Write a function called `check_word` that checks whether a given word is acceptable. It should take as parameters the word to check, a string of seven available letters, and a string containing the single required letter. You can use the functions you wrote in previous exercises.

```
check_word('color', 'ACDLORT', 'R')    // should be true
check_word('ratatat', 'ACDLORT', 'R')  // should be true
check_word('rat', 'ACDLORT', 'R')      // should be false (too short)
check_word('told', 'ACDLORT', 'R')     // should be false (missing R)
```
