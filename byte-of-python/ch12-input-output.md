# Input and Output

There will be situations where your program has to interact with the user. For example, you would want to take input from the user and then print some results back. We can achieve this using the `input()` function and `print` function respectively.

For output, we can also use the various methods of the `str` (string) class. For example, you can use the `rjust` method to get a string which is right justified to a specified width. See `help(str)` for more details.

Another common type of input/output is dealing with files. The ability to create, read and write files is essential to many programs and we will explore this aspect in this chapter.

## Input from the User

Save this program as `input.auto`:

<Listing number="12-1" file-name="input.auto" caption="Getting user input">

```auto
fn main() {
    let name = input("What is your name? ")
    print(f"Hello, $name!")
}
```

```python
def main():
    name = input("What is your name? ")
    print(f"Hello, {name}!")


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run input.auto
What is your name? Swaroop
Hello, Swaroop!
```

**How It Works**

The `input()` function takes a string as argument and displays it to the user as a prompt. Then it waits for the user to type something and press the return key. Once the user has entered and pressed the return key, the `input()` function will return that text the user has entered.

We assign the returned value to the variable `name` and then use an [f-string](./ch04-basics.md#formatting) to print a personalized greeting. In Auto, f-strings use `$var` instead of Python's `{var}` for variable interpolation, but the concept is identical.

> **Note for Python Programmers:**
>
> The `input()` function works identically in both Auto and Python. The `a2p` transpiler passes `input()` calls through unchanged. The only difference visible in this example is the f-string syntax: Auto uses `$var` while Python uses `{var}`.

## File I/O

You can open and use files for reading or writing by creating a file object using the built-in `open` function and using its `read`, `readline` or `write` methods appropriately to read from or write to the file. The ability to read or write to the file depends on the mode you have specified for opening the file. Then finally, when you are finished with the file, you call the `close` method to tell the system that we are done using the file.

Example (save as `file_io.auto`):

<Listing number="12-2" file-name="file_io.auto" caption="Reading and writing files">

```auto
use io

fn main() {
    let poem = """\
Programming is fun
When the work is done
if you wanna make your work also fun:
    use Auto!"""

    // Open for 'w'riting
    let f = open("poem.txt", "w")
    // Write text to file
    f.write(poem)
    // Close the file
    f.close()

    // If no mode is specified,
    // 'r'ead mode is assumed by default
    let f = open("poem.txt")
    if f {
        print(f.read())
        f.close()
    }
}
```

```python
import io


def main():
    poem = """\
Programming is fun
When the work is done
if you wanna make your work also fun:
    use Auto!"""

    # Open for 'w'riting
    f = open("poem.txt", "w")
    # Write text to file
    f.write(poem)
    # Close the file
    f.close()

    # If no mode is specified,
    # 'r'ead mode is assumed by default
    f = open("poem.txt")
    if f:
        print(f.read())
        f.close()


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run file_io.auto
Programming is fun
When the work is done
if you wanna make your work also fun:
    use Auto!
```

**How It Works**

Note that we can create a new file object simply by using the `open` function. We open (or create it if it doesn't already exist) this file by using the built-in `open` function and specifying the name of the file and the mode in which we want to open the file. The mode can be a read mode (`'r'`), write mode (`'w'`) or append mode (`'a'`). We can also specify whether we are reading, writing, or appending in text mode (`'t'`) or binary mode (`'b'`). There are actually many more modes available and `help(open)` will give you more details about them. By default, `open()` considers the file to be a 't'ext file and opens it in 'r'ead mode.

In our example, we first open/create the file in write text mode and use the `write` method of the file object to write our string variable `poem` to the file and then we finally `close` the file.

Next, we open the same file again for reading. We don't need to specify a mode because 'read text file' is the default mode. We read the entire content of the file using the `read` method and print it.

> **Note:**
>
> Always remember to close your files after you are done with them. An alternative approach is to use the `with` statement which automatically closes the file for you. In Auto, the `with` statement works the same way as in Python. For example:
>
> ```auto
> with open("poem.txt") as f {
>     print(f.read())
> }
> ```

> **Note for Python Programmers:**
>
> File I/O in Auto works identically to Python. The `a2p` transpiler passes `open()`, `f.write()`, `f.read()`, and `f.close()` calls through unchanged. The `use io` statement in Auto translates to `import io` in Python. File modes (`'r'`, `'w'`, `'a'`, `'b'`, `'t'`) are the same in both languages.

## Pickle

Python provides a standard module called `pickle` which you can use to store _any_ plain Python object in a file and then get it back later. This is called storing the object *persistently*.

Since Auto transpiles to Python, you can use the `pickle` module via `use pickle`.

Example (save as `using_pickle.auto`):

<Listing number="12-3" file-name="using_pickle.auto" caption="Using pickle">

```auto
use pickle

fn main() {
    let shoplist = ["apple", "mango", "carrot"]

    // Write to file
    let f = open("shoplist.data", "wb")
    pickle.dump(shoplist, f)
    f.close()

    // Read back from the storage
    let f = open("shoplist.data", "rb")
    let storedlist = pickle.load(f)
    print(storedlist)
    f.close()
}
```

```python
import pickle


def main():
    shoplist = ["apple", "mango", "carrot"]

    # Write to file
    f = open("shoplist.data", "wb")
    pickle.dump(shoplist, f)
    f.close()

    # Read back from the storage
    f = open("shoplist.data", "rb")
    storedlist = pickle.load(f)
    print(storedlist)
    f.close()


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run using_pickle.auto
['apple', 'mango', 'carrot']
```

**How It Works**

To store an object in a file, we have to first `open` the file in __w__rite __b__inary mode and then call the `dump` function of the `pickle` module. This process is called _pickling_.

Next, we retrieve the object using the `load` function of the `pickle` module which returns the object. This process is called _unpickling_.

> **Note:**
>
> The `pickle` module is Python-specific. Since Auto transpiles to Python, pickle works seamlessly in Auto code. However, the resulting `.data` files cannot be read by non-Python programs. If you need a cross-language serialization format, consider using JSON instead.

## Unicode

So far, when we have been writing and using strings, or reading and writing to a file, we have used simple English characters only. Both English and non-English characters can be represented in Unicode (please see the articles at the end of this section for more info), and Python 3 by default stores string variables (think of all that text we wrote using single or double or triple quotes) in Unicode.

When data is sent over the Internet, we need to send it in bytes -- something your computer easily understands. The rules for translating Unicode (which is what Python uses when it stores a string) to bytes is called _encoding_. A popular encoding to use is UTF-8. We can read and write in UTF-8 by using a simple keyword argument in our `open` function.

Example (save as `unicode.auto`):

<Listing number="12-4" file-name="unicode.auto" caption="Unicode text">

```auto
use io

fn main() {
    // Write Unicode content
    let f = open("unicode.txt", "w", encoding = "utf-8")
    f.write("Imagine non-English language here")
    f.close()

    // Read Unicode content
    let f = open("unicode.txt", encoding = "utf-8")
    print(f.read())
    f.close()
}
```

```python
import io


def main():
    # Write Unicode content
    f = open("unicode.txt", "w", encoding="utf-8")
    f.write("Imagine non-English language here")
    f.close()

    # Read Unicode content
    f = open("unicode.txt", encoding="utf-8")
    print(f.read())
    f.close()


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run unicode.auto
Imagine non-English language here
```

**How It Works**

We use `open` and then use the `encoding` argument in the first open statement to encode the message, and then again in the second open statement when decoding the message. Note that we should only use encoding in the `open` statement when in text mode.

In Auto (as in Python 3), strings are Unicode by default, so you can freely mix English and non-English characters in your source code. The `encoding = "utf-8"` parameter ensures that the file is written and read using the UTF-8 encoding, which supports virtually all characters from all languages.

> **Note for Python Programmers:**
>
> Unicode handling in Auto is the same as in Python 3. The `a2p` transpiler passes `open()` calls with `encoding` arguments through unchanged. Auto strings are Unicode by default, just like Python 3 strings. There is no need for the `# encoding=utf-8` comment that was required in Python 2.

You should learn more about this topic by reading:

- ["The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets"](http://www.joelonsoftware.com/articles/Unicode.html)
- [Python Unicode Howto](http://docs.python.org/3/howto/unicode.html)
- [Pragmatic Unicode talk by Nat Batchelder](http://nedbatchelder.com/text/unipain.html)

## Summary

We have discussed various types of input/output, about file handling, about the pickle module and about Unicode.

Next, we will explore the concept of exceptions.
