# Exceptions

Exceptions occur when _exceptional_ situations occur in your program. For example, what if you are going to read a file and the file does not exist? Or what if you accidentally deleted it when the program was running? Such situations are handled using **exceptions**.

Similarly, what if your program had some invalid statements? This is handled by Python which **raises** its hands and tells you there is an **error**.

## Errors

Consider a simple `print` function call. What if we misspelt `print` as `Print`? Note the capitalization. In this case, Python _raises_ a syntax error.

<Listing number="13-1" file-name="error.auto" caption="Errors">

```auto
fn main() {
    print("Hello")
    // This will cause a NameError
    print(spam)
}
```

```python
def main():
    print("Hello")
    # This will cause a NameError
    print(spam)


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run error.auto
Hello
Traceback (most recent call last):
  File "error.auto", line 4, in <module>
NameError: name 'spam' is not defined
```

**How It Works**

Observe that a `NameError` is raised and also the location where the error was detected is printed. This is what an **error handler** for this error does. In this case, the variable `spam` was never defined before it was used, so Python raises a `NameError`.

> **Note for Python Programmers:**
>
> Errors work identically in Auto and Python. Since Auto transpiles to Python via `a2p`, all syntax errors and runtime errors are ultimately Python errors. Auto's own error system uses the `!T` (error type) and `!` (throw operator) for its native error handling, but when targeting Python, the standard Python error and exception mechanism applies.

## Exceptions

We will **try** to read input from the user. Enter the first line below and hit the `Enter` key. When your computer prompts you for input, instead press `[ctrl-d]` on a Mac or `[ctrl-z]` on Windows and see what happens. (If you're using Windows and neither option works, you can try `[ctrl-c]` in the Command Prompt to generate a `KeyboardInterrupt` error instead).

```python
>>> s = input('Enter something --> ')
Enter something --> Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
EOFError
```

Python raises an error called `EOFError` which basically means it found an *end of file* symbol (which is represented by `ctrl-d`) when it did not expect to see it.

## Handling Exceptions

We can handle exceptions using the `try..except` statement. We basically put our usual statements within the try-block and put all our error handlers in the except-block.

Example (save as `handle.auto`):

<Listing number="13-2" file-name="handle.auto" caption="Handling exceptions">

```auto
fn main() {
    try {
        let text = input("Enter something: ")
    } except EOFError {
        print("\nWhy did you do an EOF on me?")
    } except KeyboardInterrupt {
        print("\nYou cancelled the operation.")
    } else {
        print(f"You entered: $text")
    }
}
```

```python
def main():
    try:
        text = input("Enter something: ")
    except EOFError:
        print("\nWhy did you do an EOF on me?")
    except KeyboardInterrupt:
        print("\nYou cancelled the operation.")
    else:
        print(f"You entered: {text}")


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
# Press ctrl + d
$ auto run handle.auto
Enter something:
Why did you do an EOF on me?

# Press ctrl + c
$ auto run handle.auto
Enter something: ^C
You cancelled the operation.

$ auto run handle.auto
Enter something: No exceptions
You entered: No exceptions
```

**How It Works**

We put all the statements that might raise exceptions/errors inside the `try` block and then put handlers for the appropriate errors/exceptions in the `except` clause/block. The `except` clause can handle a single specified error or exception, or a parenthesized list of errors/exceptions. If no names of errors or exceptions are supplied, it will handle _all_ errors and exceptions.

Note that there has to be at least one `except` clause associated with every `try` clause. Otherwise, what's the point of having a try block?

If any error or exception is not handled, then the default Python handler is called which just stops the execution of the program and prints an error message. We have already seen this in action above.

You can also have an `else` clause associated with a `try..except` block. The `else` clause is executed if no exception occurs.

In the next example, we will also see how to get the exception object so that we can retrieve additional information.

> **Note for Python Programmers:**
>
> The `try`/`except`/`else` syntax in Auto is the same as in Python. The `a2p` transpiler passes these blocks through unchanged. The only Auto-specific syntax difference is that Auto uses `{}` braces for blocks instead of Python's indentation.

## Raising Exceptions

You can _raise_ exceptions using the `raise` statement by providing the name of the error/exception and the exception object that is to be _thrown_.

The error or exception that you can raise should be a class which directly or indirectly must be a derived class of the `Exception` class.

Example (save as `raise.auto`):

<Listing number="13-3" file-name="raise.auto" caption="Raising exceptions">

```auto
type ShortInputException {
    length: int
    atleast: int

    fn init(&self, length: int, atleast: int) {
        .length = length
        .atleast = atleast
    }

    fn to_string(&self) -> str {
        f"ShortInputException: The input was ${.length} long, expected at least ${.atleast}"
    }
}

fn main() {
    try {
        let text = input("Enter something: ")
        if text.len() < 3 {
            raise ShortInputException{text.len(), 3}
        } else {
            print("No exception was raised.")
        }
    } except ShortInputException as e {
        print(e.to_string())
    } except EOFError {
        print("Why did you do an EOF on me?")
    } else {
        print("OK")
    }
}
```

```python
class ShortInputException(Exception):
    length = 0
    atleast = 0

    def __init__(self, length, atleast):
        self.length = length
        self.atleast = atleast

    def to_string(self):
        return f"ShortInputException: The input was {self.length} long, expected at least {self.atleast}"


def main():
    try:
        text = input("Enter something: ")
        if len(text) < 3:
            raise ShortInputException(len(text), 3)
        else:
            print("No exception was raised.")
    except ShortInputException as e:
        print(e.to_string())
    except EOFError:
        print("Why did you do an EOF on me?")
    else:
        print("OK")


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run raise.auto
Enter something: a
ShortInputException: The input was 1 long, expected at least 3

$ auto run raise.auto
Enter something: abc
No exception was raised.
```

**How It Works**

Here, we are creating our own exception type. This new exception type is called `ShortInputException`. It has two fields - `length` which is the length of the given input, and `atleast` which is the minimum length that the program was expecting.

In Auto, we define custom exception types using the `type` keyword with struct-like fields and an `init` constructor. The `to_string` method provides a human-readable representation of the exception. We raise the exception using `raise ShortInputException{text.len(), 3}`, which uses Auto's struct initialization syntax.

In the `except` clause, we mention the class of error which will be stored `as` the variable name to hold the corresponding error/exception object. This is analogous to parameters and arguments in a function call. Within this particular `except` clause, we use the `to_string` method of the exception object to print an appropriate message to the user.

> **Note for Python Programmers:**
>
> In Auto, custom exception classes are defined using the `type` keyword with explicit field declarations and an `init` method, rather than Python's `class` syntax. The `a2p` transpiler converts Auto's `type` blocks into Python `class` definitions that inherit from `Exception`. The `raise ShortInputException{args}` syntax in Auto is converted to `raise ShortInputException(args)` in Python. Auto's native error system also supports `!T` (error type) and `!` (throw operator), but when targeting Python, using `raise` with exception classes is the standard approach.

## Try...Finally

Suppose you are reading a file in your program. How do you ensure that the file object is closed properly whether or not an exception was raised? This can be done using the `finally` block.

Save this program as `finally.auto`:

<Listing number="13-4" file-name="finally.auto" caption="Try-finally">

```auto
use io

fn main() {
    try {
        let f = open("poem.txt")
        // File is automatically closed
        for line in f {
            print(line, end = "")
    } except IOError {
        print("Could not find file poem.txt")
    } finally {
        print("(Cleaning up: Closed the file)")
    }
}
```

```python
import io


def main():
    try:
        f = open("poem.txt")
        # File is automatically closed
        for line in f:
            print(line, end="")
    except IOError:
        print("Could not find file poem.txt")
    finally:
        print("(Cleaning up: Closed the file)")


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run finally.auto
Programming is fun
When the work is done
if you wanna make your work also fun:
    use Auto!
(Cleaning up: Closed the file)
```

**How It Works**

We do the usual file-reading stuff. We iterate over the file line by line using a `for` loop. If an `IOError` occurs (for example, if the file `poem.txt` does not exist), we print a message.

The important thing to note is the `finally` block. No matter what happens -- whether an exception occurs or not -- the `finally` block is _always_ executed. This is useful for cleanup actions like closing files, releasing resources, or restoring states.

Notice that a variable assigned a value of 0 or `None` or a variable which is an empty sequence or collection is considered `False` by Python. This is why we can use `if f:` in Python code to check if a file was successfully opened.

## The `with` Statement

Acquiring a resource in the `try` block and subsequently releasing the resource in the `finally` block is a common pattern. Hence, there is also a `with` statement that enables this to be done in a clean manner.

Save as `with_example.auto`:

<Listing number="13-5" file-name="with_example.auto" caption="Using the with statement">

```auto
use io

fn main() {
    with open("poem.txt") as f {
        for line in f {
            print(line, end = "")
    }
}
```

```python
import io


def main():
    with open("poem.txt") as f:
        for line in f:
            print(line, end="")


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run with_example.auto
Programming is fun
When the work is done
if you wanna make your work also fun:
    use Auto!
```

**How It Works**

The output should be the same as the previous example. The difference here is that we are using the `open` function with the `with` statement -- we leave the closing of the file to be done automatically by `with open`.

What happens behind the scenes is that there is a protocol used by the `with` statement. It fetches the object returned by the `open` statement, let's call it "thefile" in this case.

It _always_ calls the `thefile.__enter__` function before starting the block of code under it and _always_ calls `thefile.__exit__` after finishing the block of code.

So the code that we would have written in a `finally` block should be taken care of automatically by the `__exit__` method. This is what helps us to avoid having to use explicit `try..finally` statements repeatedly.

> **Note for Python Programmers:**
>
> The `with` statement in Auto works identically to Python's `with` statement. The `a2p` transpiler passes `with` blocks through unchanged. Auto uses `{}` braces for the block body instead of Python's indentation, but the semantics are the same -- the context manager's `__enter__` and `__exit__` methods are called at the appropriate times.

## Summary

We have discussed the usage of the `try..except` and `try..finally` statements. We have seen how to create our own exception types and how to raise exceptions as well. We have also seen the `with` statement for cleaner resource management.

Next, we will explore the Python Standard Library.
