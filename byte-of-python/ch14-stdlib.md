# Standard Library

The Python Standard Library contains a huge number of useful modules and is part of every standard Python installation. It is important to become familiar with the Python Standard Library since many problems can be solved quickly if you are familiar with the range of things that these libraries can do.

Since Auto transpiles to Python, you can import any module from Python's standard library using the `use` statement. This means the entire Python standard library is available to your Auto programs.

We will explore some of the commonly used modules in this library. You can find complete details for all of the modules in the Python Standard Library in the ['Library Reference' section](http://docs.python.org/3/library/) of the documentation that comes with your Python installation.

> **Note:**
>
> If you find the topics in this chapter too advanced, you may skip this chapter. However, it is highly recommended to come back to this chapter when you are more comfortable with programming.

## The `sys` Module

The `sys` module contains system-specific functionality. We have already seen that the `sys.argv` list contains the command-line arguments.

Suppose we want to check the version of the Python software being used to run our Auto program -- the `sys` module gives us that information.

Save as `sys_module.auto`:

<Listing number="14-1" file-name="sys_module.auto" caption="Using the sys module">

```auto
use sys

fn main() {
    print(f"Python version: $sys.version")
    print(f"Version info: $sys.version_info")

    if sys.version_info.major >= 3 {
        print("You are running Python 3 or later.")
    } else {
        print("You need to upgrade to Python 3!")
    }
}
```

```python
import sys


def main():
    print(f"Python version: {sys.version}")
    print(f"Version info: {sys.version_info}")

    if sys.version_info.major >= 3:
        print("You are running Python 3 or later.")
    else:
        print("You need to upgrade to Python 3!")


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run sys_module.auto
Python version: 3.12.0 (main, Oct  2 2024, 08:00:00)
Version info: sys.version_info(major=3, minor=12, micro=0, releaselevel='final', serial=0)
You are running Python 3 or later.
```

**How It Works**

The `sys` module has a `version_info` tuple that gives us the version information. The first entry is the major version. We can pull out this information to use it.

We use an f-string to print the full version string (`sys.version`) and the version info tuple (`sys.version_info`). Then we check whether the major version is 3 or greater using an `if` statement, and print an appropriate message.

> **Note for Python Programmers:**
>
> The `use sys` statement in Auto translates to `import sys` in Python. The `sys.version_info` attribute and `sys.version` attribute work identically in both languages since Auto transpiles to Python.

## The `logging` Module

What if you wanted to have some debugging messages or important messages to be stored somewhere so that you can check whether your program has been running as you would expect it? How do you "store somewhere" these messages? This can be achieved using the `logging` module.

Save as `logging_example.auto`:

<Listing number="14-2" file-name="logging_example.auto" caption="Using the logging module">

```auto
use os
use platform
use logging

fn main() {
    let platform_name = platform.platform()
    let user_home = os.path.expanduser("~")

    let log_file: str
    if platform_name.contains("Windows") {
        let home_drive = os.environ.get("HOMEDRIVE", "C:")
        let home_path = os.environ.get("HOMEPATH", "\\")
        log_file = os.path.join(home_drive + home_path, "test.log")
    } else {
        log_file = os.path.join(user_home, "test.log")
    }

    logging.basicConfig(
        level = logging.DEBUG,
        format = "%(asctime)s : %(levelname)s : %(message)s",
        filename = log_file
    )

    logging.debug("Start of the program")
    logging.info("Doing something")
    logging.warning("Dying now")

    print(f"Logging to: $log_file")
    print("Check the log file for details.")
}
```

```python
import os
import platform
import logging


def main():
    platform_name = platform.platform()
    user_home = os.path.expanduser("~")

    log_file: str
    if platform_name.contains("Windows"):
        home_drive = os.environ.get("HOMEDRIVE", "C:")
        home_path = os.environ.get("HOMEPATH", "\\")
        log_file = os.path.join(home_drive + home_path, "test.log")
    else:
        log_file = os.path.join(user_home, "test.log")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s : %(levelname)s : %(message)s",
        filename=log_file,
    )

    logging.debug("Start of the program")
    logging.info("Doing something")
    logging.warning("Dying now")

    print(f"Logging to: {log_file}")
    print("Check the log file for details.")


if __name__ == "__main__":
    main()
```

</Listing>

Output:

```
$ auto run logging_example.auto
Logging to: /Users/swa/test.log
Check the log file for details.

$ cat /Users/swa/test.log
2024-03-29 09:27:36,660 : DEBUG : Start of the program
2024-03-29 09:27:36,660 : INFO : Doing something
2024-03-29 09:27:36,660 : WARNING : Dying now
```

**How It Works**

We use three modules from the standard library -- the `os` module for interacting with the operating system, the `platform` module for information about the platform (i.e., the operating system), and the `logging` module to *log* information.

First, we check which operating system we are using by checking the string returned by `platform.platform()`. If it is Windows, we figure out the home drive, the home folder, and the filename where we want to store the information. Putting these parts together, we get the full location of the file. For other platforms, we need to know just the home folder of the user and we get the full location of the file.

We use the `os.path.join()` function to put these parts of the location together. The reason to use a special function rather than just adding the strings together is because this function will ensure the full location matches the format expected by the operating system.

We configure the `logging` module to write all the messages in a particular format to the file we have specified.

Finally, we can put messages that are either meant for debugging, information, warning or even critical messages. Once the program has run, we can check this file and we will know what happened in the program, even though no information was displayed to the user running the program.

> **Note for Python Programmers:**
>
> The `use os`, `use platform`, and `use logging` statements in Auto translate to `import os`, `import platform`, and `import logging` in Python respectively. All logging functions work identically since Auto transpiles to Python.

## Module of the Week

There is much more to be explored in the standard library such as [debugging](http://docs.python.org/3/library/pdb.html),
[handling command line options](http://docs.python.org/3/library/argparse.html), [regular expressions](http://docs.python.org/3/library/re.html) and so on.

The best way to further explore the standard library is to read Doug Hellmann's excellent [Python Module of the Week](http://pymotw.com/2/contents.html) series (also available as a [book](http://amzn.com/0321767349)) and reading the [Python documentation](http://docs.python.org/3/).

## Summary

We have explored some of the functionality of many modules in the Python Standard Library. It is highly recommended to browse through the [Python Standard Library documentation](http://docs.python.org/3/library/) to get an idea of all the modules that are available.

Since Auto transpiles to Python, the entire Python standard library is at your fingertips via the `use` statement. This is one of Auto's greatest strengths -- you get a clean, modern syntax while retaining full access to Python's rich ecosystem.
