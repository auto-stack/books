# Strings and Regular Expressions

Strings are not like integers, floats, and booleans. A string is a **sequence**, which means it contains multiple values in a particular order. In this chapter we'll see how to access the values that make up a string, and we'll use functions that process strings.

We'll also use regular expressions, which are a powerful tool for finding patterns in a string and performing operations like search and replace.

## A string is a sequence

A string is a sequence of characters. A **character** can be a letter (in almost any alphabet), a digit, a punctuation mark, or white space.

You can select a character from a string with the bracket operator. This example statement selects character number 1 from `fruit` and assigns it to `letter`:

```auto
let fruit = "banana"
let letter = fruit[1]
```

The expression in brackets is an **index**, so called because it *indicates* which character in the sequence to select. But the result might not be what you expect. The letter with index `1` is actually the second letter of the string. An index is an offset from the beginning of the string, so the offset of the first letter is `0`:

```auto
print(fruit[0])
```

You can think of `'b'` as the 0th letter of `'banana'` -- pronounced "zero-eth".

The index in brackets can be a variable:

```auto
let mut i = 1
print(fruit[i])
```

Or an expression that contains variables and operators:

```auto
print(fruit[i + 1])
```

As we saw in Chapter 1, we can use the built-in function `len` to get the length of a string:

```auto
let n = fruit.len()
print(n)
```

To get the last letter of a string, you might be tempted to use index `n`, but that causes an error because there is no letter in `'banana'` with the index 6. Because we started counting at `0`, the six letters are numbered `0` to `5`. To get the last character, you have to subtract `1` from `n`:

```auto
print(fruit[n - 1])
```

But there's an easier way. To get the last letter in a string, you can use a negative index, which counts backward from the end:

```auto
print(fruit[-1])
```

The index `-1` selects the last letter, `-2` selects the second to last, and so on.

> **Note for Python Programmers:**
>
> Auto uses `.len()` method to get string length instead of Python's `len()` function. The `a2p` transpiler converts `.len()` to `len()` automatically.

## String slices

A segment of a string is called a **slice**. Selecting a slice is similar to selecting a character.

```auto
let fruit = "banana"
print(fruit[0..3])
```

The operator `[n..m]` returns the part of the string from the `n`th character to the `m`th character, including the first but excluding the second. This behavior is counterintuitive, but it might help to imagine the indices pointing *between* the characters.

If you omit the first index, the slice starts at the beginning of the string:

```auto
print(fruit[..3])
```

If you omit the second index, the slice goes to the end of the string:

```auto
print(fruit[3..])
```

If the first index is greater than or equal to the second, the result is an **empty string**, represented by two quotation marks:

```auto
print(fruit[3..3])
```

An empty string contains no characters and has length 0. And if you omit both indices, the slice is a copy of the whole string:

```auto
print(fruit[..])
```

> **Note for Python Programmers:**
>
> Auto uses `s[n..m]` for slices instead of Python's `s[n:m]`. The `a2p` transpiler converts `..` to `:` automatically.

<Listing number="8-1" file-name="string_slicing.auto" caption="String slicing and indexing">

```auto
fn main() {
    let fruit = "banana"

    // Indexing: accessing individual characters
    print("fruit[0]:", fruit[0])
    print("fruit[1]:", fruit[1])
    print("fruit[-1]:", fruit[-1])
    print("fruit[-2]:", fruit[-2])

    // Slicing: accessing substrings
    print("fruit[0..3]:", fruit[0..3])
    print("fruit[2..5]:", fruit[2..5])
    print("fruit[..3]:", fruit[..3])
    print("fruit[3..]:", fruit[3..])
    print("fruit[..]:", fruit[..])

    // Empty slice
    print("fruit[3..3]:", fruit[3..3])

    // Length
    print("len(fruit):", fruit.len())
}
```

```python
def main():
    fruit = "banana"

    # Indexing: accessing individual characters
    print(f"fruit[0]: {fruit[0]}")
    print(f"fruit[1]: {fruit[1]}")
    print(f"fruit[-1]: {fruit[-1]}")
    print(f"fruit[-2]: {fruit[-2]}")

    # Slicing: accessing substrings
    print(f"fruit[0:3]: {fruit[0:3]}")
    print(f"fruit[2:5]: {fruit[2:5]}")
    print(f"fruit[:3]: {fruit[:3]}")
    print(f"fruit[3:]: {fruit[3:]}")
    print(f"fruit[:]: {fruit[:]}")

    # Empty slice
    print(f"fruit[3:3]: {fruit[3:3]}")

    # Length
    print(f"len(fruit): {len(fruit)}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

Indexing with `fruit[0]` returns the first character, `fruit[-1]` returns the last. Slicing with `fruit[0..3]` returns characters at indices 0, 1, and 2 (the upper bound is exclusive). Omitting the start (`..3`) means "from the beginning"; omitting the end (`3..`) means "to the end". An empty slice `fruit[3..3]` returns an empty string since the start equals the end.

## Strings are immutable

It is tempting to use the `[]` operator on the left side of an assignment, with the intention of changing a character in a string, like this:

```auto
let mut greeting = "Hello, world!"
greeting[0] = "J"  // ERROR!
```

This causes an error because strings are **immutable**, which means you can't change an existing string. The best you can do is create a new string that is a variation of the original:

```auto
let greeting = "Hello, world!"
let new_greeting = "J" + greeting[1..]
print(new_greeting)
```

This example concatenates a new first letter onto a slice of `greeting`. It has no effect on the original string:

```auto
print(greeting)
```

## String comparison

The relational operators work on strings. To see if two strings are equal, we can use the `==` operator:

```auto
let word = "banana"

if word == "banana" {
    print("All right, banana.")
}
```

Other relational operations are useful for putting words in alphabetical order:

```auto
fn compare_word(word: str) {
    if word < "banana" {
        print(f"$word comes before banana.")
    } else if word > "banana" {
        print(f"$word comes after banana.")
    } else {
        print("All right, banana.")
    }
}
```

Python (and Auto) does not handle uppercase and lowercase letters the same way people do. All the uppercase letters come before all the lowercase letters. To solve this problem, we can convert strings to a standard format, such as all lowercase, before performing the comparison.

## String methods

Strings provide methods that perform a variety of useful operations. A method is similar to a function -- it takes arguments and returns a value -- but the syntax is different. For example, the method `to_uppercase` takes a string and returns a new string with all uppercase letters.

Instead of the function syntax `to_uppercase(word)`, it uses the method syntax `word.to_uppercase()`:

```auto
let word = "banana"
let new_word = word.to_uppercase()
print(new_word)
```

This use of the dot operator specifies the name of the method, `to_uppercase`, and the name of the string to apply the method to, `word`. The empty parentheses indicate that this method takes no arguments.

A method call is called an **invocation**; in this case, we would say that we are invoking `to_uppercase` on `word`.

<Listing number="8-2" file-name="string_methods.auto" caption="String methods">

```auto
fn main() {
    let word = "banana"

    // Case conversion
    print("upper:", word.to_uppercase())
    print("lower:", "BANANA".to_lowercase())

    // Searching
    print("find 'a':", word.find("a"))
    print("find 'z':", word.find("z"))
    print("contains 'ana':", word.contains("ana"))
    print("starts with 'ban':", word.starts_with("ban"))
    print("ends with 'na':", word.ends_with("na"))

    // Stripping whitespace
    let spaced = "  hello world  "
    print("strip:", spaced.strip())
    print("len before:", spaced.len())
    print("len after:", spaced.strip().len())

    // Counting occurrences
    print("count 'a':", word.matches("a").count())

    // Replacement
    let text = "I like cats and cats like me"
    print("replace:", text.replace("cats", "dogs"))

    // Splitting
    let sentence = "pining for the fjords"
    let words = sentence.split(" ")
    print("split:", words)

    // Joining
    let parts = ["hello", "world"]
    print("join:", parts.join(" "))
}
```

```python
def main():
    word = "banana"

    # Case conversion
    print(f"upper: {word.upper()}")
    print(f"lower: {'BANANA'.lower()}")

    # Searching
    print(f"find 'a': {word.find('a')}")
    print(f"find 'z': {word.find('z')}")
    print(f"contains 'ana': {'ana' in word}")
    print(f"starts with 'ban': {word.startswith('ban')}")
    print(f"ends with 'na': {word.endswith('na')}")

    # Stripping whitespace
    spaced = "  hello world  "
    print(f"strip: {spaced.strip()}")
    print(f"len before: {len(spaced)}")
    print(f"len after: {len(spaced.strip())}")

    # Counting occurrences
    print(f"count 'a': {word.count('a')}")

    # Replacement
    text = "I like cats and cats like me"
    print(f"replace: {text.replace('cats', 'dogs')}")

    # Splitting
    sentence = "pining for the fjords"
    words = sentence.split(" ")
    print(f"split: {words}")

    # Joining
    parts = ["hello", "world"]
    print(f"join: {' '.join(parts)}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`to_uppercase()` (Python: `.upper()`) and `to_lowercase()` (Python: `.lower()`) return new strings with converted case. `find()` returns the index of the first occurrence or -1 if not found. `strip()` removes leading and trailing whitespace. `replace()` returns a new string with all occurrences replaced. `split()` breaks a string into a list of substrings, and `join()` concatenates a list into a single string.

> **Note for Python Programmers:**
>
> Auto uses `to_uppercase()` / `to_lowercase()` instead of Python's `.upper()` / `.lower()`. Auto uses `starts_with()` / `ends_with()` instead of Python's `.startswith()` / `.endswith()`. The `a2p` transpiler converts all of these automatically.

## Writing files

String operators and methods are useful for reading and writing text files. As an example, we'll work with a simple text file.

Here's the basic pattern for writing strings to a file:

```auto
let writer = open("output.txt", "w")
writer.write("Hello, world!\n")
writer.close()
```

The `open` function takes an optional parameter that specifies the "mode" -- `'w'` indicates that we're opening the file for writing. If the file doesn't exist, it will be created; if it already exists, the contents will be replaced.

After writing, we close the file using the `close` method to indicate that we're done.

<Listing number="8-3" file-name="file_io.auto" caption="File I/O: writing strings to a file">

```auto
fn main() {
    // Writing lines to a file
    let writer = open("output.txt", "w")
    writer.write("First line\n")
    writer.write("Second line\n")
    writer.write("Third line\n")
    writer.close()

    // Reading lines from a file
    print("Contents of output.txt:")
    for line in open("output.txt") {
        let stripped = line.strip()
        if stripped.len() > 0 {
            print(stripped)
        }
    }

    // Find and replace in a file
    let reader = open("output.txt")
    let writer2 = open("output_replaced.txt", "w")
    for line in reader {
        let new_line = line.replace("line", "row")
        writer2.write(new_line)
    }
    reader.close()
    writer2.close()

    print("\nContents of output_replaced.txt:")
    for line in open("output_replaced.txt") {
        let stripped = line.strip()
        if stripped.len() > 0 {
            print(stripped)
        }
    }
}
```

```python
def main():
    # Writing lines to a file
    writer = open("output.txt", "w")
    writer.write("First line\n")
    writer.write("Second line\n")
    writer.write("Third line\n")
    writer.close()

    # Reading lines from a file
    print("Contents of output.txt:")
    for line in open("output.txt"):
        stripped = line.strip()
        if len(stripped) > 0:
            print(stripped)

    # Find and replace in a file
    reader = open("output.txt")
    writer2 = open("output_replaced.txt", "w")
    for line in reader:
        new_line = line.replace("line", "row")
        writer2.write(new_line)
    reader.close()
    writer2.close()

    print("\nContents of output_replaced.txt:")
    for line in open("output_replaced.txt"):
        stripped = line.strip()
        if len(stripped) > 0:
            print(stripped)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`open("output.txt", "w")` opens a file for writing. The `write` method writes a string to the file -- note that it does not add a newline automatically, so we include `\n` explicitly. After writing, `close()` flushes the buffer and releases the file handle.

The reading loop uses `for line in open("output.txt")` to iterate through the file line by line. Each line includes the trailing newline, so we use `strip()` to remove it. The second part demonstrates find-and-replace: reading from one file, replacing substrings, and writing to a new file.

## Find and replace

To check whether a string contains a particular substring, you can use the `contains` method (or the `in` operator). To get the total number of occurrences, you can use the `matches` method combined with `count`:

```auto
let text = "Jonathan went to see Jonathan"
print(text.contains("Jonathan"))
print(text.matches("Jonathan").count())
```

To replace all occurrences of a substring, you can use the `replace` method:

```auto
let new_text = text.replace("Jonathan", "Thomas")
print(new_text)
```

## Regular expressions

If we know exactly what sequence of characters we're looking for, we can use `contains` to find it and `replace` to replace it. But there is another tool, called a **regular expression**, that can also perform these operations -- and a lot more.

To demonstrate, let's start with a simple example. Suppose we want to find all lines that contain a particular word. Here's a line from *Dracula*:

```auto
let text = "I am Dracula; and I bid you welcome, Mr. Harker, to my house."
```

A module called `re` provides functions related to regular expressions. We can import it like this and use the `search` function to check whether a pattern appears in the text:

```auto
use re

let pattern = "Dracula"
let result = re.search(pattern, text)
```

If the pattern appears in the text, `search` returns a `Match` object that contains the results of the search. If the pattern doesn't appear in the text, the return value from `search` is `None`.

We can use a vertical bar character, `'|'`, to match either the sequence on the left or the sequence on the right:

```auto
let pattern = "Mina|Murray"
```

The special character `'^'` matches the beginning of a string, and `'$'` matches the end of a string:

```auto
let pattern = "^Dracula"
let pattern2 = "Harker$"
```

## String substitution

We can use the `sub` function in the `re` module, which does **string substitution**. The first argument is the pattern we want to find and replace, the second is what we want to replace it with, and the third is the string we want to search:

```auto
let pattern = "colou?r"
let result = re.sub(pattern, "color", "He liked the colour of the sky")
```

The `'?'` in the pattern means the previous character is optional, so this pattern matches either "colour" or "color".

Parentheses in a pattern group parts together, so the vertical bar only applies within the group:

```auto
let pattern = "cent(er|re)"
```

This pattern matches a sequence that starts with `'cent'` and ends with either `'er'` or `'re'`.

<Listing number="8-4" file-name="regex.auto" caption="Regular expressions: search and substitution">

```auto
use re

fn main() {
    let text = "I am Dracula; and I bid you welcome, Mr. Harker, to my house."

    // Basic search
    let pattern = "Dracula"
    let result = re.search(pattern, text)
    print("Found:", result.group())
    print("Span:", result.span())

    // Search that fails
    let result2 = re.search("Count", text)
    print("Not found:", result2)

    // Alternation: match either name
    let pattern2 = "Mina|Murray"
    let result3 = re.search(pattern2, "Mina Murray was there")
    print("Alternation:", result3.group())

    // Anchors: start and end of string
    let result4 = re.search("^Dracula", "Dracula is here")
    print("Starts with Dracula:", result4.group())

    let result5 = re.search("Harker$", "Mr. Harker")
    print("Ends with Harker:", result5.group())

    // Optional character with ?
    let pattern3 = "colou?r"
    let result6 = re.sub(pattern3, "color", "The colour of the sky")
    print("Sub colour:", result6)
    let result7 = re.sub(pattern3, "color", "The color of the sky")
    print("Sub color:", result7)

    // Grouping with parentheses
    let pattern4 = "cent(er|re)"
    let result8 = re.sub(pattern4, "center", "the centre of town")
    print("Sub centre:", result8)
    let result9 = re.sub(pattern4, "center", "the center of town")
    print("Sub center:", result9)

    // findall: find all matches
    let words = "cat bat rat cat hat"
    let result10 = re.findall("cat", words)
    print("findall cat:", result10)
}
```

```python
import re

def main():
    text = "I am Dracula; and I bid you welcome, Mr. Harker, to my house."

    # Basic search
    pattern = "Dracula"
    result = re.search(pattern, text)
    print(f"Found: {result.group()}")
    print(f"Span: {result.span()}")

    # Search that fails
    result2 = re.search("Count", text)
    print(f"Not found: {result2}")

    # Alternation: match either name
    pattern2 = "Mina|Murray"
    result3 = re.search(pattern2, "Mina Murray was there")
    print(f"Alternation: {result3.group()}")

    # Anchors: start and end of string
    result4 = re.search("^Dracula", "Dracula is here")
    print(f"Starts with Dracula: {result4.group()}")

    result5 = re.search("Harker$", "Mr. Harker")
    print(f"Ends with Harker: {result5.group()}")

    # Optional character with ?
    pattern3 = "colou?r"
    result6 = re.sub(pattern3, "color", "The colour of the sky")
    print(f"Sub colour: {result6}")
    result7 = re.sub(pattern3, "color", "The color of the sky")
    print(f"Sub color: {result7}")

    # Grouping with parentheses
    pattern4 = "cent(er|re)"
    result8 = re.sub(pattern4, "center", "the centre of town")
    print(f"Sub centre: {result8}")
    result9 = re.sub(pattern4, "center", "the center of town")
    print(f"Sub center: {result9}")

    # findall: find all matches
    words = "cat bat rat cat hat"
    result10 = re.findall("cat", words)
    print(f"findall cat: {result10}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`re.search(pattern, text)` searches for the first occurrence of `pattern` in `text` and returns a `Match` object (or `None` if not found). The `group()` method returns the matched text, and `span()` returns the start and end indices.

The `|` operator in a pattern means "or" -- `Mina|Murray` matches either string. The `^` anchor matches the beginning of a string, and `$` matches the end. The `?` makes the preceding character optional. Parentheses group parts of the pattern together. `re.sub(pattern, replacement, text)` performs search-and-replace on all occurrences. `re.findall(pattern, text)` returns a list of all non-overlapping matches.

> **Note for Python Programmers:**
>
> Auto uses `use re` instead of Python's `import re`. The `a2p` transpiler converts this automatically. The `re` module functions (`search`, `sub`, `findall`) work identically in both languages.

## Debugging

When you are reading and writing files, debugging can be tricky. A good debugging strategy is to start with just part of the file, get the program working, and then run it with the whole file.

Common string-related bugs include:

- **Off-by-one errors in slicing**: Confusion about whether the upper bound is inclusive or exclusive.
- **Forgetting to strip newlines**: When reading lines from a file, each line ends with `\n`.
- **Type errors in indexing**: Using a float or string as an index instead of an integer.
- **Case sensitivity in comparisons**: `"Banana"` and `"banana"` are not equal.

## Glossary

**sequence:**
An ordered collection of values where each value is identified by an integer index.

**character:**
An element of a string, including letters, numbers, and symbols.

**index:**
An integer value used to select an item in a sequence, such as a character in a string. Indices start from `0`.

**slice:**
A part of a string specified by a range of indices.

**empty string:**
A string that contains no characters and has length `0`.

**object:**
Something a variable can refer to. An object has a type and a value.

**immutable:**
If the elements of an object cannot be changed, the object is immutable.

**invocation:**
An expression -- or part of an expression -- that calls a method.

**regular expression:**
A sequence of characters that defines a search pattern.

**pattern:**
A rule that specifies the requirements a string has to meet to constitute a match.

**string substitution:**
Replacement of a string, or part of a string, with another string.

## Exercises

### Exercise

Write a function called `is_palindrome` that takes a string argument and returns `true` if it is a palindrome (reads the same backward and forward) and `false` otherwise. For example, `"noon"` and `"rotator"` are palindromes.

```
is_palindrome("noon")     // should be true
is_palindrome("hello")    // should be false
is_palindrome("a")        // should be true
is_palindrome("")         // should be true
```

### Exercise

Write a function called `count_vowels` that takes a string and returns the number of vowels (a, e, i, o, u) in it, ignoring case.

```
count_vowels("banana")    // should be 3
count_vowels("hello")     // should be 2
count_vowels("xyz")       // should be 0
```

### Exercise

Write a regular expression that matches any word that starts with a capital letter and ends with a period. Test it with `re.search` on strings like `"Hello."`, `"world."`, and `"Python."`.

### Exercise

Write a function called `normalize_text` that takes a string and returns a new string where:
- All letters are lowercase
- Leading and trailing whitespace is removed
- Multiple spaces between words are collapsed to a single space

```
normalize_text("  Hello,   World!  ")   // should be "hello, world!"
```
