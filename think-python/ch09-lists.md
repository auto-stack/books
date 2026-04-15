# Lists

This chapter presents one of Python's most useful built-in types, lists. You will also learn more about objects and what can happen when multiple variables refer to the same object.

In the exercises at the end of the chapter, we'll make a word list and use it to search for special words like palindromes and anagrams.

## A list is a sequence

Like a string, a **list** is a sequence of values. In a string, the values are characters; in a list, they can be any type. The values in a list are called **elements**.

There are several ways to create a new list; the simplest is to enclose the elements in square brackets (`[` and `]`). For example, here is a list of two integers:

```auto
let numbers = [42, 123]
```

And here's a list of three strings:

```auto
let cheeses = ["Cheddar", "Edam", "Gouda"]
```

The elements of a list don't have to be the same type. The following list contains a string, a float, an integer, and even another list:

```auto
let t = ["spam", 2.0, 5, [10, 20]]
```

A list within another list is **nested**. A list that contains no elements is called an empty list; you can create one with empty brackets, `[]`:

```auto
let empty = []
```

The `len` function returns the length of a list:

```auto
print(cheeses.len())
print(empty.len())
```

> **Note for Python Programmers:**
>
> Auto uses `.len()` method instead of Python's `len()` function. The `a2p` transpiler converts `.len()` to `len()` automatically.

<Listing number="9-1" file-name="list_basics.auto" caption="Creating and indexing lists">

```auto
fn main() {
    // Creating lists
    let numbers = [42, 123]
    let cheeses = ["Cheddar", "Edam", "Gouda"]
    let mixed = ["spam", 2.0, 5, [10, 20]]
    let empty: [str; 0] = []

    // Accessing elements by index
    print("cheeses[0]:", cheeses[0])
    print("cheeses[1]:", cheeses[1])
    print("cheeses[2]:", cheeses[2])
    print("cheeses[-1]:", cheeses[-1])

    // Length
    print("len(cheeses):", cheeses.len())
    print("len(numbers):", numbers.len())
    print("len(empty):", empty.len())

    // The 'in' operator
    print("Edam in cheeses:", "Edam" in cheeses)
    print("Wensleydale in cheeses:", "Wensleydale" in cheeses)

    // Nested list: counts as one element
    print("len(mixed):", mixed.len())
    print("10 in mixed:", 10 in mixed)

    // Accessing nested element
    print("mixed[3]:", mixed[3])
    print("mixed[3][0]:", mixed[3][0])
}
```

```python
def main():
    # Creating lists
    numbers = [42, 123]
    cheeses = ["Cheddar", "Edam", "Gouda"]
    mixed = ["spam", 2.0, 5, [10, 20]]
    empty = []

    # Accessing elements by index
    print(f"cheeses[0]: {cheeses[0]}")
    print(f"cheeses[1]: {cheeses[1]}")
    print(f"cheeses[2]: {cheeses[2]}")
    print(f"cheeses[-1]: {cheeses[-1]}")

    # Length
    print(f"len(cheeses): {len(cheeses)}")
    print(f"len(numbers): {len(numbers)}")
    print(f"len(empty): {len(empty)}")

    # The 'in' operator
    print(f"Edam in cheeses: {'Edam' in cheeses}")
    print(f"Wensleydale in cheeses: {'Wensleydale' in cheeses}")

    # Nested list: counts as one element
    print(f"len(mixed): {len(mixed)}")
    print(f"10 in mixed: {10 in mixed}")

    # Accessing nested element
    print(f"mixed[3]: {mixed[3]}")
    print(f"mixed[3][0]: {mixed[3][0]}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

Lists are created with square brackets `[]`. Elements can be any type, and a list can contain a mix of types. Indexing works the same as strings -- `cheeses[0]` returns the first element, `cheeses[-1]` returns the last. The `in` operator checks whether a value appears anywhere in the list. A nested list (a list inside another list) counts as a single element, so `10 in mixed` is `false` even though `10` is an element of the nested list `mixed[3]`.

## Lists are mutable

Unlike strings, lists are mutable. When the bracket operator appears on the left side of an assignment, it identifies the element of the list that will be assigned:

```auto
let mut numbers = [42, 123]
numbers[1] = 17
print(numbers)
```

The second element of `numbers`, which used to be `123`, is now `17`.

List indices work the same way as string indices:

- Any integer expression can be used as an index.
- If you try to read or write an element that does not exist, you get an `IndexError`.
- If an index has a negative value, it counts backward from the end of the list.

## List slices

The slice operator works on lists the same way it works on strings:

```auto
let letters = ["a", "b", "c", "d"]
print(letters[1..3])   // ["b", "c"]
print(letters[..2])    // ["a", "b"]
print(letters[2..])    // ["c", "d"]
print(letters[..])     // ["a", "b", "c", "d"]
```

Another way to copy a list is to use the `list` function:

```auto
let copy = list(letters)
```

Because `list` is the name of a built-in function, you should avoid using it as a variable name.

## List operations

The `+` operator concatenates lists:

```auto
let t1 = [1, 2]
let t2 = [3, 4]
print(t1 + t2)    // [1, 2, 3, 4]
```

The `*` operator repeats a list a given number of times:

```auto
print(["spam"] * 4)    // ["spam", "spam", "spam", "spam"]
```

The built-in function `sum` adds up the elements:

```auto
print(sum(t1))    // 3
```

And `min` and `max` find the smallest and largest elements.

## List methods

Python provides methods that operate on lists. For example, `append` adds a new element to the end of a list:

```auto
let mut letters = ["a", "b", "c"]
letters.append("d")
```

`extend` takes a list as an argument and appends all of the elements:

```auto
letters.extend(["e", "f"])
```

There are two methods that remove elements from a list. If you know the index, you can use `pop`:

```auto
let mut t = ["a", "b", "c"]
let removed = t.pop(1)    // removes and returns "b"
```

If you know the element you want to remove (but not the index), you can use `remove`:

```auto
let mut t = ["a", "b", "c"]
t.remove("b")    // modifies the list, returns None
```

<Listing number="9-2" file-name="list_methods.auto" caption="List methods: append, sort, pop">

```auto
fn main() {
    // append: add one element
    let mut letters = ["a", "b", "c"]
    letters.append("d")
    print("After append:", letters)

    // extend: add multiple elements
    letters.extend(["e", "f"])
    print("After extend:", letters)

    // pop: remove by index
    let mut t = ["a", "b", "c"]
    let removed = t.pop(1)
    print("Popped:", removed)
    print("After pop:", t)

    // remove: remove by value
    let mut t2 = ["a", "b", "c"]
    t2.remove("b")
    print("After remove:", t2)

    // sort: sort in place (ascending)
    let mut nums = [3, 1, 4, 1, 5, 9]
    nums.sort()
    print("Sorted:", nums)

    // sorted: returns a new sorted list (original unchanged)
    let scramble = ["c", "a", "b"]
    let sorted_list = sorted(scramble)
    print("Original:", scramble)
    print("Sorted copy:", sorted_list)

    // reverse
    let mut items = [1, 2, 3]
    items.reverse()
    print("Reversed:", items)

    // index: find position of element
    let fruits = ["apple", "banana", "cherry"]
    print("index of banana:", fruits.index("banana"))

    // count: count occurrences
    let data = [1, 2, 2, 3, 2]
    print("count of 2:", data.count(2))
}
```

```python
def main():
    # append: add one element
    letters = ["a", "b", "c"]
    letters.append("d")
    print(f"After append: {letters}")

    # extend: add multiple elements
    letters.extend(["e", "f"])
    print(f"After extend: {letters}")

    # pop: remove by index
    t = ["a", "b", "c"]
    removed = t.pop(1)
    print(f"Popped: {removed}")
    print(f"After pop: {t}")

    # remove: remove by value
    t2 = ["a", "b", "c"]
    t2.remove("b")
    print(f"After remove: {t2}")

    # sort: sort in place (ascending)
    nums = [3, 1, 4, 1, 5, 9]
    nums.sort()
    print(f"Sorted: {nums}")

    # sorted: returns a new sorted list (original unchanged)
    scramble = ["c", "a", "b"]
    sorted_list = sorted(scramble)
    print(f"Original: {scramble}")
    print(f"Sorted copy: {sorted_list}")

    # reverse
    items = [1, 2, 3]
    items.reverse()
    print(f"Reversed: {items}")

    # index: find position of element
    fruits = ["apple", "banana", "cherry"]
    print(f"index of banana: {fruits.index('banana')}")

    # count: count occurrences
    data = [1, 2, 2, 3, 2]
    print(f"count of 2: {data.count(2)}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`append` adds a single element to the end; `extend` adds all elements from another list. `pop(index)` removes and returns the element at the given index. `remove(value)` removes the first occurrence of the given value (returns `None`). `sort()` sorts the list in place, modifying the original. `sorted()` returns a new sorted list, leaving the original unchanged. `reverse()` reverses the list in place. `index(value)` returns the index of the first occurrence. `count(value)` returns the number of occurrences.

> **Note for Python Programmers:**
>
> Auto uses `.len()` and `.sort()` methods that work similarly to Python's. The `a2p` transpiler converts these automatically. Note that `sorted()` is a built-in function in both languages that returns a new list.

## Lists and strings

A string is a sequence of characters and a list is a sequence of values, but a list of characters is not the same as a string. To convert from a string to a list of characters, you can use the `list` function:

```auto
let s = "spam"
let t = list(s)
print(t)    // ["s", "p", "a", "m"]
```

The `list` function breaks a string into individual letters. If you want to break a string into words, you can use the `split` method:

```auto
let s = "pining for the fjords"
let t = s.split(" ")
```

An optional argument called a **delimiter** specifies which characters to use as word boundaries:

```auto
let s = "ex-parrot"
let t = s.split("-")    // ["ex", "parrot"]
```

If you have a list of strings, you can concatenate them into a single string using `join`. `join` is a string method, so you have to invoke it on the delimiter and pass the list as an argument:

```auto
let delimiter = " "
let t = ["pining", "for", "the", "fjords"]
let s = delimiter.join(t)
```

## Looping through a list

You can use a `for` statement to loop through the elements of a list:

```auto
let cheeses = ["Cheddar", "Edam", "Gouda"]

for cheese in cheeses {
    print(cheese)
}
```

For example, after using `split` to make a list of words, we can use `for` to loop through them:

```auto
let s = "pining for the fjords"

for word in s.split(" ") {
    print(word)
}
```

A `for` loop over an empty list never runs the indented statements.

## Sorting lists

Python provides a built-in function called `sorted` that sorts the elements of a list. The original list is unchanged:

```auto
let scramble = ["c", "a", "b"]
let sorted_scramble = sorted(scramble)
print(scramble)         // ["c", "a", "b"] -- unchanged
print(sorted_scramble)  // ["a", "b", "c"]
```

`sorted` works with any kind of sequence, not just lists. So we can sort the letters in a string like this:

```auto
let sorted_letters = sorted("letters")
print(sorted_letters)   // ['e', 'e', 'l', 'r', 's', 't', 't']
```

The result is a list. To convert the list to a string, we can use `join`:

```auto
let result = "".join(sorted("letters"))
print(result)   // "eelrstt"
```

With an empty string as the delimiter, the elements of the list are joined with nothing between them.

<Listing number="9-3" file-name="list_operations.auto" caption="Looping and list operations">

```auto
fn main() {
    // Looping through a list
    let cheeses = ["Cheddar", "Edam", "Gouda"]
    print("Cheeses:")
    for cheese in cheeses {
        print(" ", cheese)
    }

    // Looping through words from a string
    let sentence = "pining for the fjords"
    print("\nWords:")
    for word in sentence.split(" ") {
        print(" ", word)
    }

    // List concatenation
    let t1 = [1, 2]
    let t2 = [3, 4]
    print("\nConcat:", t1 + t2)

    // List repetition
    print("Repeat:", ["spam"] * 3)

    // Sum, min, max
    print("Sum:", sum([1, 2, 3, 4]))
    print("Min:", min([5, 2, 8, 1]))
    print("Max:", max([5, 2, 8, 1]))

    // String <-> List conversions
    let s = "hello"
    let chars = list(s)
    print("list('hello'):", chars)
    print("join:", chars.join("-"))

    // Sorted string letters
    let sorted_str = "".join(sorted("letters"))
    print("Sorted letters:", sorted_str)

    // Looping with index using enumerate
    let fruits = ["apple", "banana", "cherry"]
    print("\nWith index:")
    for (i, fruit) in fruits.enumerate() {
        print(f"  $i: $fruit")
    }
}
```

```python
def main():
    # Looping through a list
    cheeses = ["Cheddar", "Edam", "Gouda"]
    print("Cheeses:")
    for cheese in cheeses:
        print(f" {cheese}")

    # Looping through words from a string
    sentence = "pining for the fjords"
    print("\nWords:")
    for word in sentence.split(" "):
        print(f" {word}")

    # List concatenation
    t1 = [1, 2]
    t2 = [3, 4]
    print(f"\nConcat: {t1 + t2}")

    # List repetition
    print(f"Repeat: {['spam'] * 3}")

    # Sum, min, max
    print(f"Sum: {sum([1, 2, 3, 4])}")
    print(f"Min: {min([5, 2, 8, 1])}")
    print(f"Max: {max([5, 2, 8, 1])}")

    # String <-> List conversions
    s = "hello"
    chars = list(s)
    print(f"list('hello'): {chars}")
    print(f"join: {'-'.join(chars)}")

    # Sorted string letters
    sorted_str = "".join(sorted("letters"))
    print(f"Sorted letters: {sorted_str}")

    # Looping with index using enumerate
    fruits = ["apple", "banana", "cherry"]
    print("\nWith index:")
    for i, fruit in enumerate(fruits):
        print(f"  {i}: {fruit}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`for item in list` iterates through each element. `split(" ")` breaks a string into a list of words. The `+` operator concatenates lists, and `*` repeats a list. Built-in functions `sum`, `min`, and `max` operate on lists. `list(string)` converts a string to a list of characters, and `delimiter.join(list)` joins a list into a string. `sorted()` returns a new sorted list from any sequence. `enumerate()` yields pairs of `(index, value)` for looping with indices.

> **Note for Python Programmers:**
>
> Auto uses `.enumerate()` method instead of Python's `enumerate()` function. The `a2p` transpiler converts this automatically. Auto uses `.split()` with an explicit delimiter argument.

## Objects and values

If we run these assignment statements:

```auto
let a = "banana"
let b = "banana"
```

We know that `a` and `b` both refer to a string, but we don't know whether they refer to the *same* string. To check whether two variables refer to the same object, you can use the `is` operator:

```auto
print(a is b)    // true (for strings, Auto may reuse the same object)
```

But when you create two lists, you get two objects:

```auto
let a = [1, 2, 3]
let b = [1, 2, 3]
print(a is b)    // false (two separate list objects)
```

In this case we would say that the two lists are **equivalent**, because they have the same elements, but not **identical**, because they are not the same object. If two objects are identical, they are also equivalent, but if they are equivalent, they are not necessarily identical.

## Aliasing

If `a` refers to an object and you assign `b = a`, then both variables refer to the same object:

```auto
let mut a = [1, 2, 3]
let b = a
print(b is a)    // true
```

The association of a variable with an object is called a **reference**. In this example, there are two references to the same object.

An object with more than one reference has more than one name, so we say the object is **aliased**. If the aliased object is mutable, changes made with one name affect the other:

```auto
b[0] = 5
print(a)    // [5, 2, 3] -- a "sees" the change
```

So we would say that `a` "sees" this change. Although this behavior can be useful, it is error-prone. In general, it is safer to avoid aliasing when you are working with mutable objects.

For immutable objects like strings, aliasing is not as much of a problem.

## List arguments

When you pass a list to a function, the function gets a reference to the list. If the function modifies the list, the caller sees the change:

```auto
fn pop_first(lst: [int]) -> int {
    return lst.pop(0)
}

let mut letters = ["a", "b", "c"]
let first = pop_first(letters)
print(first)    // "a"
print(letters)  // ["b", "c"] -- the list was modified
```

In this example, the parameter `lst` and the variable `letters` are aliases for the same object. Passing a reference to an object as an argument to a function creates a form of aliasing. If the function modifies the object, those changes persist after the function is done.

<Listing number="9-4" file-name="aliasing.auto" caption="Aliasing and references">

```auto
fn pop_first(lst: [str]) -> str {
    return lst.pop(0)
}

fn append_item(lst: [str], item: str) {
    lst.append(item)
}

fn main() {
    // Aliasing: two names, one object
    let mut a = [1, 2, 3]
    let b = a
    print("b is a:", b is a)
    print("Before change - a:", a)

    // Modifying through b affects a
    b[0] = 5
    print("After b[0] = 5 - a:", a)

    // Lists are not identical even if equivalent
    let c = [1, 2, 3]
    let d = [1, 2, 3]
    print("c == d:", c == d)
    print("c is d:", c is d)

    // Strings: aliasing is safe (immutable)
    let s1 = "banana"
    let s2 = s1
    print("s1 is s2:", s1 is s2)

    // List arguments: caller sees changes
    let mut letters = ["a", "b", "c"]
    print("\nBefore pop_first:", letters)
    let first = pop_first(letters)
    print("Popped:", first)
    print("After pop_first:", letters)

    let mut items = ["x", "y"]
    print("\nBefore append_item:", items)
    append_item(items, "z")
    print("After append_item:", items)

    // Copying a list to avoid aliasing
    let mut original = [10, 20, 30]
    let copy = original[..]  // slice copy
    copy[0] = 99
    print("\noriginal after copy modified:", original)
    print("copy:", copy)
}
```

```python
def pop_first(lst):
    return lst.pop(0)


def append_item(lst, item):
    lst.append(item)


def main():
    # Aliasing: two names, one object
    a = [1, 2, 3]
    b = a
    print(f"b is a: {b is a}")
    print(f"Before change - a: {a}")

    # Modifying through b affects a
    b[0] = 5
    print(f"After b[0] = 5 - a: {a}")

    # Lists are not identical even if equivalent
    c = [1, 2, 3]
    d = [1, 2, 3]
    print(f"c == d: {c == d}")
    print(f"c is d: {c is d}")

    # Strings: aliasing is safe (immutable)
    s1 = "banana"
    s2 = s1
    print(f"s1 is s2: {s1 is s2}")

    # List arguments: caller sees changes
    letters = ["a", "b", "c"]
    print(f"\nBefore pop_first: {letters}")
    first = pop_first(letters)
    print(f"Popped: {first}")
    print(f"After pop_first: {letters}")

    items = ["x", "y"]
    print(f"\nBefore append_item: {items}")
    append_item(items, "z")
    print(f"After append_item: {items}")

    # Copying a list to avoid aliasing
    original = [10, 20, 30]
    copy = original[:]
    copy[0] = 99
    print(f"\noriginal after copy modified: {original}")
    print(f"copy: {copy}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

When you assign `b = a` for a list, both variables point to the same object. Modifying the list through one name (`b[0] = 5`) is visible through the other (`a`). This is **aliasing**.

The `is` operator checks identity (same object), while `==` checks equivalence (same value). Two lists with the same contents are equivalent but not identical.

When you pass a list to a function, the function receives a reference (alias) to the same object. Any modifications the function makes to the list are visible to the caller.

To avoid aliasing, you can create a copy using a full slice: `original[..]` in Auto, `original[:]` in Python. This creates a new list with the same elements, so modifications to the copy don't affect the original.

## Making a word list

In the previous chapter, we read the file `words.txt` and searched for words with certain properties. But we read the entire file many times, which is not efficient. It is better to read the file once and put the words in a list:

```auto
let mut word_list: [str] = []

for line in open("words.txt") {
    let word = line.strip()
    word_list.append(word)
}

print(word_list.len())
```

Another way to do the same thing is to use `read` to read the entire file into a string, then use `split` to split it into a list of words:

```auto
let string = open("words.txt").read()
let word_list = string.split("\n")
print(word_list.len())
```

Now, to check whether a string appears in the list, we can use the `in` operator.

## Debugging

Note that most list methods modify the argument and return `None`. This is the opposite of the string methods, which return a new string and leave the original alone.

If you are used to writing string code like this:

```auto
let word = "plumage!"
let word = word.strip("!")
```

It is tempting to write list code like this:

```auto
let mut t = [1, 2, 3]
t = t.remove(3)    // WRONG!
```

`remove` modifies the list and returns `None`, so `t` becomes `None` and any subsequent operation on `t` is likely to fail. This is a common mistake for programmers who are transitioning from strings to lists.

If you see an error message like this, you should look backward through the program and see if you might have called a list method incorrectly.

## Glossary

**list:**
An object that contains a sequence of values.

**element:**
One of the values in a list or other sequence.

**nested list:**
A list that is an element of another list.

**delimiter:**
A character or string used to indicate where a string should be split.

**equivalent:**
Having the same value.

**identical:**
Being the same object (which implies equivalence).

**reference:**
The association between a variable and its value.

**aliased:**
If there is more than one variable that refers to an object, the object is aliased.

**attribute:**
One of the named values associated with an object.

## Exercises

### Exercise

Two words are anagrams if you can rearrange the letters from one to spell the other. For example, `tops` is an anagram of `stop`.

One way to check whether two words are anagrams is to sort the letters in both words. If the lists of sorted letters are the same, the words are anagrams.

Write a function called `is_anagram` that takes two strings and returns `true` if they are anagrams.

```
is_anagram("tops", "stop")     // should be true
is_anagram("skate", "takes")   // should be true
is_anagram("tops", "takes")    // should be false
```

### Exercise

A palindrome is a word that is spelled the same backward and forward, like "noon" and "rotator". Write a function called `is_palindrome` that takes a string argument and returns `true` if it is a palindrome and `false` otherwise.

```
is_palindrome("bob")      // should be true
is_palindrome("alice")    // should be false
is_palindrome("a")        // should be true
is_palindrome("")         // should be true
```

### Exercise

Write a function called `reverse_sentence` that takes as an argument a string that contains any number of words separated by spaces. It should return a new string that contains the same words in reverse order. For example, if the argument is "Reverse this sentence", the result should be "Sentence this reverse".

Hint: You can use the `capitalize` method to capitalize the first word and convert the other words to lowercase.

### Exercise

Write a function called `total_length` that takes a list of strings and returns the total length of the strings. Use a loop and the accumulator pattern.
