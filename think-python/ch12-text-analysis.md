# Text Analysis and Generation

This chapter is a case study that uses Python's core data structures -- lists, dictionaries, and tuples -- to explore text analysis and Markov generation:

* Text analysis is a way to describe the statistical relationships between the words in a document, like the probability that one word is followed by another, and

* Markov generation is a way to generate new text with words and phrases similar to the original text.

These algorithms are similar to parts of a Large Language Model (LLM), which is the key component of a chatbot.

We'll start by counting the number of times each word appears in a book. Then we'll look at pairs of words, and make a list of the words that can follow each word. We'll make a simple version of a Markov generator, and as an exercise, you'll have a chance to make a more general version.

## Unique words

As a first step toward text analysis, let's read a book -- *The Strange Case Of Dr. Jekyll And Mr. Hyde* by Robert Louis Stevenson -- and count the number of unique words. Instructions for downloading the book are in the notebook for this chapter.

We'll use a `for` loop to read lines from the file and `split` to divide the lines into words. Then, to keep track of unique words, we'll store each word as a key in a dictionary.

```auto
let mut unique_words: HashMap<str, int> = {}
for line in open(filename) {
    let seq = line.split()
    for word in seq {
        unique_words[word] = 1
    }
}
print(len(unique_words))
```

The length of the dictionary is the number of unique words -- about 6000 by this way of counting. But if we inspect them, we'll see that some are not valid words.

For example, let's look at the longest words in `unique_words`. We can use `sorted` to sort the words, passing the `len` function as a keyword argument so the words are sorted by length.

```auto
sorted(unique_words.keys(), key=len)[-5:]
```

The slice index, `[-5:]`, selects the last `5` elements of the sorted list, which are the longest words.

The list includes some legitimately long words, like "circumscription", and some hyphenated words, like "chocolate-coloured". But some of the longest "words" are actually two words separated by a dash. And other words include punctuation like periods, exclamation points, and quotation marks.

So, before we move on, let's deal with dashes and other punctuation.

## Punctuation

To identify the words in the text, we need to deal with two issues:

* When a dash appears in a line, we should replace it with a space -- then when we use `split`, the words will be separated.

* After splitting the words, we can use `strip` to remove punctuation.

To handle the first issue, we can use the following function, which takes a string, replaces dashes with spaces, splits the string, and returns the resulting list.

```auto
fn split_line(line: str) -> List<str> {
    return line.replace("\u2014", " ").split()
}
```

Notice that `split_line` only replaces em dashes (`\u2014`), not hyphens. Here's an example.

```auto
split_line("coolness\u2014frightened")  // ["coolness", "frightened"]
```

Now, to remove punctuation from the beginning and end of each word, we can use `strip`, but we need a list of characters that are considered punctuation.

Characters in Auto strings are in Unicode, which is an international standard used to represent letters in nearly every alphabet, numbers, symbols, punctuation marks, and more. We can find punctuation marks by checking for characters with Unicode categories that begin with `'P'`.

The following loop stores the unique punctuation marks in a dictionary.

```auto
let mut punc_marks: HashMap<str, int> = {}
for line in open(filename) {
    for char in line {
        if not char.is_alphanumeric() and char != " " {
            punc_marks[char] = 1
        }
    }
}
let punctuation = "".join(punc_marks.keys())
print(punctuation)
```

Now that we know which characters in the book are punctuation, we can write a function that takes a word, strips punctuation from the beginning and end, and converts it to lower case.

```auto
fn clean_word(word: str, punctuation: str) -> str {
    return word.strip(punctuation).lower()
}
```

Here's an example.

```auto
clean_word("\u201cBehold!\u201d", punctuation)  // "behold"
```

Because `strip` removes characters from the beginning and end, it leaves hyphenated words alone.

```auto
clean_word("pocket-handkerchief", punctuation)  // "pocket-handkerchief"
```

<Listing number="12-1" file-name="unique_words.auto" caption="Counting unique words with punctuation cleaning">

```auto
fn split_line(line: str) -> List<str> {
    return line.replace("\u2014", " ").split()
}

fn clean_word(word: str, punctuation: str) -> str {
    return word.strip(punctuation).lower()
}

fn main() {
    // Simulated text from Dr. Jekyll and Mr. Hyde
    let lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?"
    ]

    // Count unique words (simple version without punctuation cleaning)
    let mut unique_words: HashMap<str, int> = {}
    for line in lines {
        let seq = line.split()
        for word in seq {
            unique_words[word] = 1
        }
    }
    print("Unique words (simple):", len(unique_words))

    // Find longest words
    let sorted_words = sorted(unique_words.keys(), key=len)
    print("Longest words:", sorted_words[-3:])

    // Build punctuation set
    let mut punc_marks: HashMap<str, int> = {}
    for line in lines {
        for char in line {
            if not char.is_alphanumeric() and char != " " {
                punc_marks[char] = 1
            }
        }
    }
    let punctuation = "".join(punc_marks.keys())
    print("Punctuation marks:", punctuation)

    // Count cleaned unique words
    let mut unique_words2: HashMap<str, int> = {}
    for line in lines {
        for word in split_line(line) {
            let cleaned = clean_word(word, punctuation)
            unique_words2[cleaned] = 1
        }
    }
    print("Unique words (cleaned):", len(unique_words2))

    // Show longest cleaned words
    let sorted2 = sorted(unique_words2.keys(), key=len)
    print("Longest cleaned words:", sorted2[-3:])
}
```

```python
def split_line(line):
    return line.replace("\u2014", " ").split()


def clean_word(word, punctuation):
    return word.strip(punctuation).lower()


def main():
    # Simulated text from Dr. Jekyll and Mr. Hyde
    lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?"
    ]

    # Count unique words (simple version without punctuation cleaning)
    unique_words = {}
    for line in lines:
        seq = line.split()
        for word in seq:
            unique_words[word] = 1
    print(f"Unique words (simple): {len(unique_words)}")

    # Find longest words
    sorted_words = sorted(unique_words.keys(), key=len)
    print(f"Longest words: {sorted_words[-3:]}")

    # Build punctuation set
    punc_marks = {}
    for line in lines:
        for char in line:
            if not char.isalnum() and char != " ":
                punc_marks[char] = 1
    punctuation = "".join(punc_marks.keys())
    print(f"Punctuation marks: {punctuation}")

    # Count cleaned unique words
    unique_words2 = {}
    for line in lines:
        for word in split_line(line):
            cleaned = clean_word(word, punctuation)
            unique_words2[cleaned] = 1
    print(f"Unique words (cleaned): {len(unique_words2)}")

    # Show longest cleaned words
    sorted2 = sorted(unique_words2.keys(), key=len)
    print(f"Longest cleaned words: {sorted2[-3:]}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The simple word-counting approach treats every whitespace-separated token as a word, including strings with attached punctuation like `"Hyde"` or `"remarkable!"`. By detecting non-alphanumeric characters and building a punctuation string, `clean_word` strips punctuation from both ends and lowercases the result. The em dash (`\u2014`) is replaced with a space before splitting, so words connected by dashes are properly separated. Hyphenated words like `"pocket-handkerchief"` are preserved because `strip` only removes characters from the ends.

## Word frequencies

Now let's see how many times each word is used. The following loop computes the frequency of each unique word.

```auto
let mut word_counter: HashMap<str, int> = {}
for line in open(filename) {
    for word in split_line(line) {
        word = clean_word(word, punctuation)
        if word not in word_counter {
            word_counter[word] = 1
        } else {
            word_counter[word] += 1
        }
    }
}
```

The first time we see a word, we initialize its frequency to `1`. If we see the same word again later, we increment its frequency.

To see which words appear most often, we can use `items` to get the key-value pairs from `word_counter`, and sort them by the second element of the pair, which is the frequency. First we'll define a function that selects the second element.

```auto
fn second_element(t: Tuple) -> int {
    return t[1]
}
```

Now we can use `sorted` with two keyword arguments:

* `key=second_element` means the items will be sorted according to the frequencies of the words.

* `reverse=true` means the items will be sorted in reverse order, with the most frequent words first.

```auto
let items = sorted(word_counter.items(), key=second_element, reverse=true)
```

Here are the five most frequent words.

```auto
for i in 0..5 {
    let (word, freq) = items[i]
    print(f"$freq\t$word")
}
```

In the next section, we'll encapsulate this loop in a function. And we'll use it to demonstrate a new feature -- optional parameters.

## Optional parameters

We've used built-in functions that take optional parameters. For example, `round` takes an optional parameter called `ndigits` that indicates how many decimal places to keep.

```auto
round(3.141592653589793, ndigits=3)  // 3.142
```

But it's not just built-in functions -- we can write functions with optional parameters, too. For example, the following function takes two parameters, `word_counter` and `num`.

```auto
fn print_most_common(word_counter: HashMap<str, int>, num: int = 5) {
    let items = sorted(word_counter.items(), key=second_element, reverse=true)
    for i in 0..num {
        let (word, freq) = items[i]
        print(f"$freq\t$word")
    }
}
```

The second parameter looks like an assignment statement, but it's not -- it's an optional parameter.

If you call this function with one argument, `num` gets the **default value**, which is `5`.

```auto
print_most_common(word_counter)
```

If you call this function with two arguments, the second argument gets assigned to `num` instead of the default value.

```auto
print_most_common(word_counter, 3)
```

In that case, we would say the optional argument **overrides** the default value.

If a function has both required and optional parameters, all of the required parameters have to come first, followed by the optional ones.

> **Note for Python Programmers:**
>
> Auto optional parameters use the same `param = value` syntax as Python. The `a2p` transpiler converts this directly.

<Listing number="12-2" file-name="word_frequencies.auto" caption="Computing and displaying word frequencies">

```auto
fn split_line(line: str) -> List<str> {
    return line.replace("\u2014", " ").split()
}

fn clean_word(word: str, punctuation: str) -> str {
    return word.strip(punctuation).lower()
}

fn second_element(t: Tuple) -> int {
    return t[1]
}

fn print_most_common(word_counter: HashMap<str, int>, num: int = 5) {
    let items = sorted(word_counter.items(), key=second_element, reverse=true)
    for i in 0..num {
        let (word, freq) = items[i]
        print(f"$freq\t$word")
    }
}

fn main() {
    let lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?",
        "Dr. Jekyll was a well-known man in the city.",
        "Mr. Hyde was a strange and violent man.",
        "The lawyer Utterson was worried about his friend Dr. Jekyll."
    ]

    // Build punctuation set
    let mut punc_marks: HashMap<str, int> = {}
    for line in lines {
        for char in line {
            if not char.is_alphanumeric() and char != " " {
                punc_marks[char] = 1
            }
        }
    }
    let punctuation = "".join(punc_marks.keys())

    // Build word frequency counter
    let mut word_counter: HashMap<str, int> = {}
    for line in lines {
        for word in split_line(line) {
            let cleaned = clean_word(word, punctuation)
            if cleaned == "" { continue }
            if cleaned not in word_counter {
                word_counter[cleaned] = 1
            } else {
                word_counter[cleaned] += 1
            }
        }
    }

    print("Word frequencies (top 10):")
    print_most_common(word_counter, 10)

    print()
    print("Default number (top 5):")
    print_most_common(word_counter)
}
```

```python
def split_line(line):
    return line.replace("\u2014", " ").split()


def clean_word(word, punctuation):
    return word.strip(punctuation).lower()


def second_element(t):
    return t[1]


def print_most_common(word_counter, num=5):
    items = sorted(word_counter.items(), key=second_element, reverse=True)
    for i in range(num):
        word, freq = items[i]
        print(f"{freq}\t{word}")


def main():
    lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?",
        "Dr. Jekyll was a well-known man in the city.",
        "Mr. Hyde was a strange and violent man.",
        "The lawyer Utterson was worried about his friend Dr. Jekyll."
    ]

    # Build punctuation set
    punc_marks = {}
    for line in lines:
        for char in line:
            if not char.isalnum() and char != " ":
                punc_marks[char] = 1
    punctuation = "".join(punc_marks.keys())

    # Build word frequency counter
    word_counter = {}
    for line in lines:
        for word in split_line(line):
            cleaned = clean_word(word, punctuation)
            if cleaned == "":
                continue
            if cleaned not in word_counter:
                word_counter[cleaned] = 1
            else:
                word_counter[cleaned] += 1

    print("Word frequencies (top 10):")
    print_most_common(word_counter, 10)

    print()
    print("Default number (top 5):")
    print_most_common(word_counter)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`word_counter` maps each cleaned word to its frequency. The `second_element` function serves as a sort key to order items by frequency. The `print_most_common` function demonstrates optional parameters: calling it with one argument uses the default `num=5`; calling it with two arguments overrides the default.

## Dictionary subtraction

Suppose we want to spell-check a book -- that is, find a list of words that might be misspelled. One way to do that is to find words in the book that don't appear in a list of valid words.

We can think of this problem as set subtraction -- that is, we want to find all the words from one set (the words in the book) that are not in the other (the words in the list).

Then we'll store the words as keys in a dictionary so we can use the `in` operator to check quickly whether a word is valid.

```auto
let mut valid_words: HashMap<str, int> = {}
for word in word_list {
    valid_words[word] = 1
}
```

Now, to identify words that appear in the book but not in the word list, we'll use `subtract`, which takes two dictionaries as parameters and returns a new dictionary that contains all the keys from one that are not in the other.

```auto
fn subtract(d1: HashMap<str, int>, d2: HashMap<str, int>) -> HashMap<str, int> {
    let mut res: HashMap<str, int> = {}
    for key in d1 {
        if key not in d2 {
            res[key] = d1[key]
        }
    }
    return res
}
```

Here's how we use it.

```auto
let diff = subtract(word_counter, valid_words)
```

To get a sample of words that might be misspelled, we can print the most common words in `diff`.

```auto
print_most_common(diff)
```

The most common "misspelled" words are mostly names and a few single-letter words.

If we select words that only appear once, they are more likely to be actual misspellings. We can do that by looping through the items and making a list of words with frequency `1`.

```auto
let mut singletons: List<str> = []
for (word, freq) in diff.items() {
    if freq == 1 {
        singletons.append(word)
    }
}
```

Most of them are valid words that are not in the word list. But some may be actual misspellings, so at least we found some legitimate errors.

<Listing number="12-3" file-name="dict_subtraction.auto" caption="Dictionary subtraction for spell-checking">

```auto
fn split_line(line: str) -> List<str> {
    return line.replace("\u2014", " ").split()
}

fn clean_word(word: str, punctuation: str) -> str {
    return word.strip(punctuation).lower()
}

fn second_element(t: Tuple) -> int {
    return t[1]
}

fn subtract(d1: HashMap<str, int>, d2: HashMap<str, int>) -> HashMap<str, int> {
    let mut res: HashMap<str, int> = {}
    for key in d1 {
        if key not in d2 {
            res[key] = d1[key]
        }
    }
    return res
}

fn print_most_common(word_counter: HashMap<str, int>, num: int = 5) {
    let items = sorted(word_counter.items(), key=second_element, reverse=true)
    for i in 0..num {
        let (word, freq) = items[i]
        print(f"$freq\t$word")
    }
}

fn main() {
    let lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?",
        "Dr. Jekyll was a well-known man in the city.",
        "Mr. Hyde was a strange and violent man.",
        "The lawyer Utterson was worried about his friend Dr. Jekyll."
    ]

    let mut punc_marks: HashMap<str, int> = {}
    for line in lines {
        for char in line {
            if not char.is_alphanumeric() and char != " " {
                punc_marks[char] = 1
            }
        }
    }
    let punctuation = "".join(punc_marks.keys())

    let mut word_counter: HashMap<str, int> = {}
    for line in lines {
        for word in split_line(line) {
            let cleaned = clean_word(word, punctuation)
            if cleaned == "" { continue }
            if cleaned not in word_counter {
                word_counter[cleaned] = 1
            } else {
                word_counter[cleaned] += 1
            }
        }
    }

    // A small valid word list for demonstration
    let valid_word_list = [
        "the", "a", "was", "and", "of", "not", "but", "it",
        "strange", "case", "door", "man", "city", "two",
        "friend", "worried", "violent", "his", "about"
    ]
    let mut valid_words: HashMap<str, int> = {}
    for word in valid_word_list {
        valid_words[word] = 1
    }

    // Dictionary subtraction
    let diff = subtract(word_counter, valid_words)
    print("Words possibly misspelled (most common):")
    print_most_common(diff, 8)

    // Find singletons
    let mut singletons: List<str> = []
    for (word, freq) in diff.items() {
        if freq == 1 {
            singletons.append(word)
        }
    }
    print()
    print(f"Singletons: ${len(singletons)} words")
    print("Sample:", singletons[-5:])
}
```

```python
def split_line(line):
    return line.replace("\u2014", " ").split()


def clean_word(word, punctuation):
    return word.strip(punctuation).lower()


def second_element(t):
    return t[1]


def subtract(d1, d2):
    res = {}
    for key in d1:
        if key not in d2:
            res[key] = d1[key]
    return res


def print_most_common(word_counter, num=5):
    items = sorted(word_counter.items(), key=second_element, reverse=True)
    for i in range(num):
        word, freq = items[i]
        print(f"{freq}\t{word}")


def main():
    lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?",
        "Dr. Jekyll was a well-known man in the city.",
        "Mr. Hyde was a strange and violent man.",
        "The lawyer Utterson was worried about his friend Dr. Jekyll."
    ]

    punc_marks = {}
    for line in lines:
        for char in line:
            if not char.isalnum() and char != " ":
                punc_marks[char] = 1
    punctuation = "".join(punc_marks.keys())

    word_counter = {}
    for line in lines:
        for word in split_line(line):
            cleaned = clean_word(word, punctuation)
            if cleaned == "":
                continue
            if cleaned not in word_counter:
                word_counter[cleaned] = 1
            else:
                word_counter[cleaned] += 1

    valid_word_list = [
        "the", "a", "was", "and", "of", "not", "but", "it",
        "strange", "case", "door", "man", "city", "two",
        "friend", "worried", "violent", "his", "about"
    ]
    valid_words = {}
    for word in valid_word_list:
        valid_words[word] = 1

    diff = subtract(word_counter, valid_words)
    print("Words possibly misspelled (most common):")
    print_most_common(diff, 8)

    singletons = []
    for word, freq in diff.items():
        if freq == 1:
            singletons.append(word)
    print()
    print(f"Singletons: {len(singletons)} words")
    print(f"Sample: {singletons[-5:]}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The `subtract` function performs set-like subtraction on dictionaries: it returns a new dictionary containing keys from `d1` that are not in `d2`, preserving the values from `d1`. By subtracting `valid_words` from `word_counter`, we get the words that appear in the text but not in our reference list -- candidates for misspellings. Singletons (words appearing only once) are especially likely to be actual errors rather than proper nouns or domain-specific terms.

## Random numbers

As a step toward Markov text generation, next we'll choose a random sequence of words from `word_counter`. But first let's talk about randomness.

Given the same inputs, most computer programs are **deterministic**, which means they generate the same outputs every time. Determinism is usually a good thing, since we expect the same calculation to yield the same result. For some applications, though, we want the computer to be unpredictable.

The `random` module provides functions that generate pseudorandom numbers. We can import it like this.

```auto
use random
```

The `random` module provides a function called `choice` that chooses an element from a list at random, with every element having the same probability of being chosen.

```auto
let t = [1, 2, 3]
random.choice(t)  // e.g., 2
```

If you call the function again, you might get the same element again, or a different one.

The `random` module provides another function called `choices` that takes weights as an optional argument.

```auto
random.choices(words, weights=weights)
```

And it takes another optional argument, `k`, that specifies the number of words to select.

```auto
let random_words = random.choices(words, weights=weights, k=6)
random_words
```

If you choose words from the book at random, you get a sense of the vocabulary, but a series of random words seldom makes sense because there is no relationship between successive words.

## Bigrams

Instead of looking at one word at a time, now we'll look at sequences of two words, which are called **bigrams**. A sequence of three words is called a **trigram**, and a sequence with some unspecified number of words is called an **n-gram**.

Let's write a program that finds all of the bigrams in the book and the number of times each one appears. To store the results, we'll use a dictionary where the keys are tuples of strings that represent bigrams, and the values are integers that represent frequencies.

As we go through the book, we have to keep track of each pair of consecutive words. We'll use a list called `window`, because it is like a window that slides over the text, showing only two words at a time.

```auto
let mut window: List<str> = []

fn process_word(word: str) {
    window.append(word)
    if len(window) == 2 {
        count_bigram(window)
        window.pop(0)
    }
}
```

The first time this function is called, it appends the given word to `window`. Since there is only one word, we don't have a bigram yet. The second time it's called, it appends a second word and calls `count_bigram`. Then it uses `pop` to remove the first word from the window, making room for the next.

## Markov analysis

We can do better with Markov chain text analysis, which computes, for each word in a text, the list of words that come next. As an example, we'll analyze these lyrics from the Monty Python song *Eric, the Half a Bee*:

```auto
let song = [
    "Half", "a", "bee", "philosophically,",
    "Must", "ipso", "facto,", "half", "not", "be.",
    "But", "half", "the", "bee", "has", "got", "to", "be",
    "Vis", "a", "vis,", "its", "entity.", "D'you", "see?"
]
```

To store the results, we'll use a dictionary that maps from each word to the list of words that follow it.

```auto
let mut successor_map: HashMap<str, List<str>> = {}
```

The following function encapsulates the logic of adding bigrams to the successor map.

```auto
fn add_bigram(successor_map: HashMap<str, List<str>>, bigram: List<str>) {
    let first = bigram[0]
    let second = bigram[1]

    if first not in successor_map:
        successor_map[first] = [second]
    else:
        successor_map[first].append(second)
}
```

If the same bigram appears more than once, the second word is added to the list more than once. In this way, `successor_map` keeps track of how many times each successor appears.

## Generating text

We can use the results from the previous section to generate new text with the same relationships between consecutive words as in the original. Here's how it works:

* Starting with any word that appears in the text, we look up its possible successors and choose one at random.

* Then, using the chosen word, we look up its possible successors, and choose one at random.

We can repeat this process to generate as many words as we want.

<Listing number="12-4" file-name="markov_text.auto" caption="Simple Markov text generation">

```auto
use random

fn split_line(line: str) -> List<str> {
    return line.replace("\u2014", " ").split()
}

fn clean_word(word: str, punctuation: str) -> str {
    return word.strip(punctuation).lower()
}

fn add_bigram(successor_map: HashMap<str, List<str>>, bigram: List<str>) {
    let first = bigram[0]
    let second = bigram[1]

    if first not in successor_map {
        successor_map[first] = [second]
    } else {
        successor_map[first].append(second)
    }
}

fn main() {
    let song = [
        "Half", "a", "bee", "philosophically,",
        "Must", "ipso", "facto,", "half", "not", "be.",
        "But", "half", "the", "bee", "has", "got", "to", "be",
        "Vis", "a", "vis,", "its", "entity.", "D'you", "see?"
    ]

    let mut punctuation: HashMap<str, int> = {}
    let punc_chars = ",.'"
    for c in punc_chars {
        punctuation[c] = 1
    }
    let punc = "".join(punctuation.keys())

    // Build successor map from the song
    let mut successor_map: HashMap<str, List<str>> = {}
    let mut window: List<str> = []

    for string in song {
        let word = clean_word(string, punc)
        if word == "" { continue }
        window.append(word)

        if len(window) == 2 {
            add_bigram(successor_map, window)
            window.pop(0)
        }
    }

    print("Successor map from song:")
    for (key, value) in successor_map.items() {
        print(f"  '$key' -> $value")
    }

    // Markov text generation
    random.seed(42)
    let start_word = "half"
    print()
    print(f"Starting word: '$start_word'")
    print("Generated text:")

    let mut word = start_word
    let mut result: List<str> = [start_word]

    for i in 0..15 {
        if word not in successor_map {
            break
        }
        let successors = successor_map[word]
        word = random.choice(successors)
        result.append(word)
    }

    print(" ".join(result))
}
```

```python
import random


def split_line(line):
    return line.replace("\u2014", " ").split()


def clean_word(word, punctuation):
    return word.strip(punctuation).lower()


def add_bigram(successor_map, bigram):
    first = bigram[0]
    second = bigram[1]

    if first not in successor_map:
        successor_map[first] = [second]
    else:
        successor_map[first].append(second)


def main():
    song = [
        "Half", "a", "bee", "philosophically,",
        "Must", "ipso", "facto,", "half", "not", "be.",
        "But", "half", "the", "bee", "has", "got", "to", "be",
        "Vis", "a", "vis,", "its", "entity.", "D'you", "see?"
    ]

    punctuation = {}
    punc_chars = ",.'"
    for c in punc_chars:
        punctuation[c] = 1
    punc = "".join(punctuation.keys())

    # Build successor map from the song
    successor_map = {}
    window = []

    for string in song:
        word = clean_word(string, punc)
        if word == "":
            continue
        window.append(word)

        if len(window) == 2:
            add_bigram(successor_map, window)
            window.pop(0)

    print("Successor map from song:")
    for key, value in successor_map.items():
        print(f"  '{key}' -> {value}")

    # Markov text generation
    random.seed(42)
    start_word = "half"
    print()
    print(f"Starting word: '{start_word}'")
    print("Generated text:")

    word = start_word
    result = [start_word]

    for i in range(16):
        if word not in successor_map:
            break
        successors = successor_map[word]
        word = random.choice(successors)
        result.append(word)

    print(" ".join(result))


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The Markov chain generator works in two phases. First, it builds a **successor map** (also called a transition table) by scanning the text with a sliding window of size 2. Each pair of consecutive words becomes a bigram; the first word is stored as a key and the second word is appended to its list of possible successors. If the same bigram appears multiple times, the successor appears multiple times in the list, which naturally weights the selection toward more frequent transitions.

In the generation phase, the algorithm starts with a given word, looks up its successors in the map, and chooses one at random using `random.choice`. The chosen word becomes the new current word, and the process repeats. Because the successor lists encode the statistical relationships between consecutive words, the generated text preserves some of the structure and style of the original.

We can do better using more than one word as a key in `successor_map`. For example, we can make a dictionary that maps from each bigram -- or trigram -- to the list of words that come next. As an exercise, you'll have a chance to implement this analysis and see what the results look like.

## Debugging

At this point we are writing more substantial programs, and you might find that you are spending more time debugging. If you are stuck on a difficult bug, here are a few things to try:

* **Reading**: Examine your code, read it back to yourself, and check that it says what you meant to say.

* **Running**: Experiment by making changes and running different versions. Often if you display the right thing at the right place in the program, the problem becomes obvious, but sometimes you have to build scaffolding.

* **Ruminating**: Take some time to think! What kind of error is it: syntax, runtime, or semantic? What information can you get from the error messages, or from the output of the program?

* **Rubberducking**: If you explain the problem to someone else, you sometimes find the answer before you finish asking the question. Often you don't need the other person; you could just talk to a rubber duck. And that's the origin of the well-known strategy called **rubber duck debugging**.

* **Retreating**: At some point, the best thing to do is back up -- undoing recent changes -- until you get to a program that works. Then you can start rebuilding.

* **Resting**: If you give your brain a break, sometime it will find the problem for you.

Beginning programmers sometimes get stuck on one of these activities and forget the others. Each activity comes with its own failure mode. For example, reading your code works if the problem is a typographical error, but not if the problem is a conceptual misunderstanding.

You have to take time to think. Debugging is like an experimental science. You should have at least one hypothesis about what the problem is. If there are two or more possibilities, try to think of a test that would eliminate one of them.

Finding a hard bug requires reading, running, ruminating, retreating, and sometimes resting. If you get stuck on one of these activities, try the others.

## Glossary

**default value:**
The value assigned to a parameter if no argument is provided.

**override:**
To replace a default value with an argument.

**deterministic:**
A deterministic program does the same thing each time it runs, given the same inputs.

**pseudorandom:**
A pseudorandom sequence of numbers appears to be random, but is generated by a deterministic program.

**bigram:**
A sequence of two elements, often words.

**trigram:**
A sequence of three elements.

**n-gram:**
A sequence of an unspecified number of elements.

**Markov analysis:**
An analysis that computes, for each element in a sequence, the set of elements that can follow it.

**successor map:**
A dictionary that maps from each element to a list of possible successors.

**rubber duck debugging:**
A way of debugging by explaining a problem aloud to an inanimate object.

## Exercises

### Exercise

Write a function that counts the number of times each trigram (sequence of three words) appears. If you test your function with the text of *Dr. Jekyll and Mr. Hyde*, you should find that the most common trigram is "said the lawyer".

Hint: Write a function called `count_trigram` that is similar to `count_bigram`. Then write a function called `process_word_trigram` that is similar to `process_word_bigram`, but uses a window of size 3.

### Exercise

Now let's implement Markov chain text analysis with a mapping from each bigram to a list of possible successors.

Starting with `add_bigram`, write a function called `add_trigram` that takes a list of three words and either adds or updates an item in `successor_map`, using the first two words as the key and the third word as a possible successor.

Then write a function `process_word_trigram` that uses a window of size 3 and calls `add_trigram`.

### Exercise

Using the `successor_map` from the previous exercise (which maps from bigrams to lists of successors), write a loop that generates 50 words of text:

1. Choose a random key from `successor_map`.

2. Look up the list of words that can follow the bigram.

3. Choose one of them at random and print it.

4. Make a new bigram from the second word of the current bigram and the chosen successor.

5. Repeat.

If everything is working, you should find that the generated text is recognizably similar in style to the original, and some phrases make sense, but the text might wander from one topic to another.
