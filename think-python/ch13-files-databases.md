# Files and Databases

Most of the programs we have seen so far are **ephemeral** in the sense that they run for a short time and produce output, but when they end, their data disappears. Each time you run an ephemeral program, it starts with a clean slate.

Other programs are **persistent**: they run for a long time (or all the time); they keep at least some of their data in long-term storage; and if they shut down and restart, they pick up where they left off.

A simple way for programs to maintain their data is by reading and writing text files. A more versatile alternative is to store data in a database. Databases are specialized files that can be read and written more efficiently than text files, and they provide additional capabilities.

In this chapter, we'll write programs that read and write text files and work with file systems. But before you can work with a file, you have to find it, so we'll start with file names, paths, and directories.

## Filenames and paths

Files are organized into **directories**, also called "folders". Every running program has a **current working directory**, which is the default directory for most operations. For example, when you open a file, the program looks for it in the current working directory.

The `os` module provides functions for working with files and directories ("os" stands for "operating system"). It provides a function called `getcwd` that gets the name of the current working directory.

```auto
use os

let cwd = os.getcwd()
print(cwd)  // e.g., "/home/dinsdale"
```

A string like `'/home/dinsdale'` that identifies a file or directory is called a **path**.

A simple filename like `'memo.txt'` is also considered a path, but it is a **relative path** because it specifies a file name relative to the current directory. A path that begins with `/` does not depend on the current directory -- it is called an **absolute path**. To find the absolute path to a file, you can use `abspath`.

```auto
os.path.abspath("memo.txt")  // e.g., "/home/dinsdale/memo.txt"
```

The `os` module provides other functions for working with filenames and paths. `listdir` returns a list of the contents of the given directory, including files and other directories.

```auto
os.listdir("photos")  // e.g., ["notes.txt", "jan-2023", "feb-2023", "mar-2023"]
```

To check whether a file or directory exists, we can use `os.path.exists`.

```auto
os.path.exists("photos")  // true
os.path.exists("photos/apr-2023")  // false
```

To check whether a path refers to a file or directory, we can use `isdir` and `isfile`.

```auto
os.path.isdir("photos")  // true
os.path.isfile("photos/notes.txt")  // true
```

One challenge of working with paths is that they look different on different operating systems. On macOS and UNIX systems like Linux, the directory and file names in a path are separated by a forward slash, `/`. Windows uses a backward slash, `\`.

Or, to write code that works on both systems, you can use `os.path.join`, which joins directory and filenames into a path using the appropriate separator for the operating system.

```auto
os.path.join("photos", "jan-2023", "photo1.jpg")  // "photos/jan-2023/photo1.jpg"
```

> **Note for Python Programmers:**
>
> Auto uses `os`, `os.path`, `os.getcwd()`, `os.listdir()`, `os.path.join()`, `os.path.exists()`, `os.path.isdir()`, `os.path.isfile()` the same way as Python. The `a2p` transpiler converts these directly.

## Format strings

One way for programs to store data is to write it to a text file. For example, suppose you are a camel spotter, and you want to record the number of camels you have seen during a period of observation. And suppose that in one and a half years, you have spotted `23` camels.

```auto
let num_years = 1.5
let num_camels = 23
```

To write a combination of strings and other values, we can use an **f-string** in Auto, which uses the `$var` syntax to interpolate variables.

```auto
let line1 = f"I have spotted $num_camels camels"
print(line1)  // I have spotted 23 camels
```

There can be more than one variable in a format string.

```auto
let line2 = f"In $num_years years I have spotted $num_camels camels"
print(line2)  // In 1.5 years I have spotted 23 camels
```

And the expressions can contain function calls.

```auto
let months = int(num_years * 12)
let line3 = f"In $months months I have spotted $num_camels camels"
print(line3)  // In 18 months I have spotted 23 camels
```

So we could write the data to a text file like this.

```auto
let writer = open("camel-spotting-book.txt", "w")
writer.write(f"Years of observation: $num_years\n")
writer.write(f"Camels spotted: $num_camels\n")
writer.close()
```

Both format strings end with the sequence `\n`, which adds a newline character.

> **Note for Python Programmers:**
>
> Python uses `{var}` syntax in f-strings, while Auto uses `$var`. The `a2p` transpiler converts `f"$var"` to `f"{var}"` automatically.

<Listing number="13-1" file-name="file_paths.auto" caption="Reading and writing files with os and format strings">

```auto
use os

fn main() {
    // Current working directory
    let cwd = os.getcwd()
    print("Current directory:", cwd)

    // Absolute path
    let abs_path = os.path.abspath("memo.txt")
    print("Absolute path of 'memo.txt':", abs_path)

    // f-string style formatting in Auto
    let num_years = 1.5
    let num_camels = 23

    let line1 = f"Years of observation: $num_years"
    let line2 = f"Camels spotted: $num_camels"
    print(line1)
    print(line2)

    // f-string with expressions
    let months = int(num_years * 12)
    let line3 = f"In $months months I have spotted $num_camels camels"
    print(line3)

    // os.path operations
    let joined = os.path.join("photos", "jan-2023", "photo1.jpg")
    print("Joined path:", joined)

    // Check if path exists (demonstration)
    print("Does 'photos' exist?", os.path.exists("photos"))

    // isdir and isfile checks
    print("Is '.' a directory?", os.path.isdir("."))
    print("Is 'memo.txt' a file?", os.path.isfile("memo.txt"))
}
```

```python
import os


def main():
    # Current working directory
    cwd = os.getcwd()
    print(f"Current directory: {cwd}")

    # Absolute path
    abs_path = os.path.abspath("memo.txt")
    print(f"Absolute path of 'memo.txt': {abs_path}")

    # f-string style formatting in Auto
    num_years = 1.5
    num_camels = 23

    line1 = f"Years of observation: {num_years}"
    line2 = f"Camels spotted: {num_camels}"
    print(line1)
    print(line2)

    # f-string with expressions
    months = int(num_years * 12)
    line3 = f"In {months} months I have spotted {num_camels} camels"
    print(line3)

    # os.path operations
    joined = os.path.join("photos", "jan-2023", "photo1.jpg")
    print(f"Joined path: {joined}")

    # Check if path exists (demonstration)
    print(f"Does 'photos' exist? {os.path.exists('photos')}")

    # isdir and isfile checks
    print(f"Is '.' a directory? {os.path.isdir('.')}")
    print(f"Is 'memo.txt' a file? {os.path.isfile('memo.txt')}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The `os` module provides cross-platform functions for working with the file system. `os.getcwd()` returns the current working directory. `os.path.abspath()` converts a relative path to an absolute path. `os.path.join()` constructs paths using the correct separator for the operating system. `os.path.exists()`, `os.path.isdir()`, and `os.path.isfile()` check for the existence and type of paths. Auto's `f"$var"` format strings interpolate variables directly, similar to Python's `f"{var}"` syntax.

## YAML

One of the reasons programs read and write files is to store **configuration data**, which is information that specifies what the program should do and how. The `yaml` module in Python provides functions to work with YAML files, which are text files formatted to be easy for humans *and* programs to read and write.

Converting an object like a dictionary to a string is called **serialization**. Converting the string back to an object is called **deserialization**.

In Auto, configuration is typically handled through the `pac.at` project file rather than YAML. However, the concepts of serialization and deserialization apply equally when working with JSON or other text-based data formats.

## Storing data structures

In previous chapters, we've worked with data structures like lists and dictionaries. A common task is to store these structures in a text file so they persist between program runs.

One approach is to use a simple text format. For example, to store a dictionary that maps from sorted strings of letters to lists of anagram words, we could write each key-value pair on a separate line.

Another approach is to use JSON (JavaScript Object Notation), a widely-supported text format that represents data structures as strings. Most programming languages, including Auto and Python, provide built-in or library support for reading and writing JSON.

## Checking for equivalent files

Now let's get back to a practical task: searching for different files that contain the same data. One way to check is to read the contents of both files and compare.

If the files contain images, we have to open them with mode `'rb'`, where `'r'` means we want to read the contents and `'b'` indicates **binary mode**. In binary mode, the contents are not interpreted as text -- they are treated as a sequence of bytes.

```auto
let data1 = open("photo1.jpg", "rb").read()
let data2 = open("photo2.jpg", "rb").read()
print(data1 == data2)  // false
```

If we have a large number of files and we want to know whether any two of them contain the same data, it would be inefficient to compare every pair of files. An alternative is to use a **hash function**, which takes the contents of a file and computes a **digest**, which is usually a large integer. If two files contain the same data, they will have the same digest.

The `hashlib` module provides several hash functions. The `md5` function is commonly used for this purpose. The idea is to compute a digest for each file, store the file paths in a dictionary keyed by digest, and then check for any digests that map to multiple files.

## Walking directories

The following function takes as an argument the directory we want to search. It uses `listdir` to loop through the contents of the directory. When it finds a file, it prints its complete path. When it finds a directory, it calls itself recursively to search the subdirectory.

```auto
use os

fn walk(dirname: str) {
    let names = os.listdir(dirname)
    for name in names {
        let path = os.path.join(dirname, name)

        if os.path.isfile(path) {
            print(path)
        } else if os.path.isdir(path) {
            walk(path)
        }
    }
}
```

We can use it like this:

```auto
walk("photos")
```

The order of the results depends on details of the operating system.

<Listing number="13-2" file-name="walk_directory.auto" caption="Walking a directory recursively">

```auto
use os

fn walk(dirname: str) {
    let names = os.listdir(dirname)
    for name in names {
        let path = os.path.join(dirname, name)

        if os.path.isfile(path) {
            print(path)
        } else if os.path.isdir(path) {
            walk(path)
        }
    }
}

fn main() {
    // Create a small demo directory structure
    os.makedirs("demo/photos/jan-2023", exist_ok=true)
    os.makedirs("demo/photos/feb-2023", exist_ok=true)

    // Create some demo files
    let f1 = open("demo/photos/notes.txt", "w")
    f1.write("Some notes about photos\n")
    f1.close()

    let f2 = open("demo/photos/jan-2023/photo1.jpg", "w")
    f2.write("fake jpeg data\n")
    f2.close()

    let f3 = open("demo/photos/jan-2023/photo2.jpg", "w")
    f3.write("fake jpeg data 2\n")
    f3.close()

    let f4 = open("demo/photos/feb-2023/photo3.jpg", "w")
    f4.write("fake jpeg data 3\n")
    f4.close()

    // Walk the directory
    print("Walking 'demo/photos':")
    walk("demo/photos")

    // List directory contents
    print()
    print("os.listdir('demo/photos'):", os.listdir("demo/photos"))
    print("os.listdir('demo/photos/jan-2023'):", os.listdir("demo/photos/jan-2023"))

    // Check file vs directory
    print()
    print("isdir('demo/photos'):", os.path.isdir("demo/photos"))
    print("isfile('demo/photos/notes.txt'):", os.path.isfile("demo/photos/notes.txt"))
}
```

```python
import os


def walk(dirname):
    names = os.listdir(dirname)
    for name in names:
        path = os.path.join(dirname, name)

        if os.path.isfile(path):
            print(path)
        elif os.path.isdir(path):
            walk(path)


def main():
    # Create a small demo directory structure
    os.makedirs("demo/photos/jan-2023", exist_ok=True)
    os.makedirs("demo/photos/feb-2023", exist_ok=True)

    # Create some demo files
    f1 = open("demo/photos/notes.txt", "w")
    f1.write("Some notes about photos\n")
    f1.close()

    f2 = open("demo/photos/jan-2023/photo1.jpg", "w")
    f2.write("fake jpeg data\n")
    f2.close()

    f3 = open("demo/photos/jan-2023/photo2.jpg", "w")
    f3.write("fake jpeg data 2\n")
    f3.close()

    f4 = open("demo/photos/feb-2023/photo3.jpg", "w")
    f4.write("fake jpeg data 3\n")
    f4.close()

    # Walk the directory
    print("Walking 'demo/photos':")
    walk("demo/photos")

    # List directory contents
    print()
    print(f"os.listdir('demo/photos'): {os.listdir('demo/photos')}")
    print(f"os.listdir('demo/photos/jan-2023'): {os.listdir('demo/photos/jan-2023')}")

    # Check file vs directory
    print()
    print(f"isdir('demo/photos'): {os.path.isdir('demo/photos')}")
    print(f"isfile('demo/photos/notes.txt'): {os.path.isfile('demo/photos/notes.txt')}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The `walk` function is a recursive directory traverser. It starts by listing the contents of the given directory with `os.listdir()`. For each entry, it constructs the full path using `os.path.join()`. If the entry is a file (`os.path.isfile()`), it prints the path. If the entry is a directory (`os.path.isdir()`), it calls itself recursively to explore the subdirectory. This pattern -- processing files at the current level and recursing into subdirectories -- is one of the most common uses of recursion in practical programming.

<Listing number="13-3" file-name="word_list.auto" caption="Building a word list from files">

```auto
use os

fn walk(dirname: str) {
    let names = os.listdir(dirname)
    for name in names {
        let path = os.path.join(dirname, name)
        if os.path.isfile(path) {
            print(path)
        } else if os.path.isdir(path) {
            walk(path)
        }
    }
}

fn main() {
    // Build a word list by reading text files from a directory
    os.makedirs("demo_texts", exist_ok=true)

    // Create sample text files
    let f1 = open("demo_texts/story1.txt", "w")
    f1.write("The quick brown fox jumps over the lazy dog\n")
    f1.write("The fox was very quick indeed\n")
    f1.close()

    let f2 = open("demo_texts/story2.txt", "w")
    f2.write("A lazy dog slept in the sun all day\n")
    f2.write("The sun was bright and warm\n")
    f2.close()

    let f3 = open("demo_texts/story3.txt", "w")
    f3.write("Quick thinking helps in many situations\n")
    f3.write("The dog chased the fox through the field\n")
    f3.close()

    // Collect unique words from all .txt files
    let mut word_set: HashMap<str, int> = {}
    let mut total_words = 0
    let mut file_count = 0

    let names = os.listdir("demo_texts")
    for name in names {
        let path = os.path.join("demo_texts", name)
        if os.path.isfile(path) and path.endswith(".txt") {
            file_count += 1
            let content = open(path).read()
            let words = content.split()
            for word in words {
                // Clean the word: strip punctuation, lowercase
                let cleaned = word.strip(",.!?").lower()
                if cleaned != "" {
                    word_set[cleaned] = 1
                    total_words += 1
                }
            }
        }
    }

    print(f"Files read: $file_count")
    print(f"Total word tokens: $total_words")
    print(f"Unique words: ${len(word_set)}")

    // Show sorted unique words
    let sorted_words = sorted(word_set.keys())
    print()
    print("Unique words (sorted):")
    print(sorted_words)

    // Write word list to a file using f-string formatting
    let writer = open("demo_texts/word_list.txt", "w")
    writer.write(f"Total unique words: ${len(word_set)}\n")
    writer.write(f"Total word tokens: $total_words\n")
    writer.write(f"Files processed: $file_count\n")
    writer.write("\nWords:\n")
    for word in sorted_words {
        writer.write(f"$word\n")
    }
    writer.close()
    print()
    print("Word list written to demo_texts/word_list.txt")
}
```

```python
import os


def walk(dirname):
    names = os.listdir(dirname)
    for name in names:
        path = os.path.join(dirname, name)
        if os.path.isfile(path):
            print(path)
        elif os.path.isdir(path):
            walk(path)


def main():
    # Build a word list by reading text files from a directory
    os.makedirs("demo_texts", exist_ok=True)

    # Create sample text files
    f1 = open("demo_texts/story1.txt", "w")
    f1.write("The quick brown fox jumps over the lazy dog\n")
    f1.write("The fox was very quick indeed\n")
    f1.close()

    f2 = open("demo_texts/story2.txt", "w")
    f2.write("A lazy dog slept in the sun all day\n")
    f2.write("The sun was bright and warm\n")
    f2.close()

    f3 = open("demo_texts/story3.txt", "w")
    f3.write("Quick thinking helps in many situations\n")
    f3.write("The dog chased the fox through the field\n")
    f3.close()

    # Collect unique words from all .txt files
    word_set = {}
    total_words = 0
    file_count = 0

    names = os.listdir("demo_texts")
    for name in names:
        path = os.path.join("demo_texts", name)
        if os.path.isfile(path) and path.endswith(".txt"):
            file_count += 1
            content = open(path).read()
            words = content.split()
            for word in words:
                # Clean the word: strip punctuation, lowercase
                cleaned = word.strip(",.!?").lower()
                if cleaned != "":
                    word_set[cleaned] = 1
                    total_words += 1

    print(f"Files read: {file_count}")
    print(f"Total word tokens: {total_words}")
    print(f"Unique words: {len(word_set)}")

    # Show sorted unique words
    sorted_words = sorted(word_set.keys())
    print()
    print("Unique words (sorted):")
    print(sorted_words)

    # Write word list to a file using f-string formatting
    writer = open("demo_texts/word_list.txt", "w")
    writer.write(f"Total unique words: {len(word_set)}\n")
    writer.write(f"Total word tokens: {total_words}\n")
    writer.write(f"Files processed: {file_count}\n")
    writer.write("\nWords:\n")
    for word in sorted_words:
        writer.write(f"{word}\n")
    writer.close()
    print()
    print("Word list written to demo_texts/word_list.txt")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

This example combines file I/O with the word-processing techniques from Chapter 12. It creates sample text files, then reads them all to build a comprehensive word list. For each `.txt` file in the directory, it reads the contents, splits into words, cleans each word by stripping punctuation and lowercasing, and adds it to a dictionary to track unique words. Finally, it writes the results to a new file using `f"$var"` format strings to embed variables in the output. This pattern -- reading files from a directory, processing their contents, and writing results -- is extremely common in data processing pipelines.

## Debugging

When you are reading and writing files, you might run into problems with whitespace. These errors can be hard to debug because whitespace characters are normally invisible. For example, here's a string that contains spaces, a tab represented by the sequence `\t`, and a newline represented by the sequence `\n`. When we print it, we don't see the whitespace characters.

```auto
let s = "1 2\t 3\n 4"
print(s)
```

The built-in function `repr` can help. It takes any object as an argument and returns a string representation of the object. For strings, it represents whitespace characters with backslash sequences.

```auto
print(repr(s))  // '1 2\t 3\n 4'
```

This can be helpful for debugging.

One other problem you might run into is that different systems use different characters to indicate the end of a line. Some systems use a newline, represented `\n`. Others use a return character, represented `\r`. Some use both. If you move files between different systems, these inconsistencies can cause problems.

File name capitalization is another issue you might encounter if you work with different operating systems. In macOS and UNIX, file names can contain lowercase and uppercase letters, digits, and most symbols. But many Windows applications ignore the difference between lowercase and uppercase letters.

## Glossary

**ephemeral:**
An ephemeral program typically runs for a short time and, when it ends, its data are lost.

**persistent:**
A persistent program runs indefinitely and keeps at least some of its data in permanent storage.

**directory:**
A collection of files and other directories.

**current working directory:**
The default directory used by a program unless another directory is specified.

**path:**
A string that specifies a sequence of directories, often leading to a file.

**relative path:**
A path that starts from the current working directory, or some other specified directory.

**absolute path:**
A path that does not depend on the current directory.

**configuration data:**
Data, often stored in a file, that specifies what a program should do and how.

**serialization:**
Converting an object to a string.

**deserialization:**
Converting a string to an object.

**database:**
A file whose contents are organized to perform certain operations efficiently.

**binary mode:**
A way of opening a file so the contents are interpreted as a sequence of bytes rather than a sequence of characters.

**hash function:**
A function that takes an object and computes an integer, which is sometimes called a digest.

**digest:**
The result of a hash function, especially when it is used to check whether two objects are the same.

## Exercises

### Exercise

Write a function called `replace_all` that takes as arguments a pattern string, a replacement string, and two filenames. It should read the first file and write the contents into the second file (creating it if necessary). If the pattern string appears anywhere in the contents, it should be replaced with the replacement string.

### Exercise

Write a function that takes a directory name and walks through all subdirectories, collecting all files that end with a given extension (like `.txt` or `.jpg`). The function should return a list of full paths to all matching files.

### Exercise

Using the `walk` function and the `md5_digest` concept from this chapter, write a program that searches a directory for duplicate files -- files that contain exactly the same data. Your program should:

1. Walk through the directory and its subdirectories.

2. For each file, compute a hash digest of its contents.

3. Store the file paths in a dictionary keyed by digest.

4. Print any groups of files that have the same digest.

Hint: Use the `hashlib` module in Python, or implement a simple checksum in Auto.
