# Modules

You have seen how you can reuse code in your program by defining functions once. What if you wanted to reuse a number of functions in other programs that you write? As you might have guessed, the answer is modules.

There are various methods of writing modules, but the simplest way is to create a file with a `.at` extension that contains functions and variables. Every Auto file is already a module in its own right.

A module can be *imported* by another program to make use of its functionality. This is how we can use the Python standard library as well -- Auto transpiles its `use` statements into Python `import` statements via `a2p`. First, we will see how to use the standard library modules.

## The `use` Statement (Importing Modules)

In Auto, you bring a module into your program using the `use` keyword. When the `a2p` transpiler processes your Auto code, it converts `use` into Python's `import` statement. This is one of the key places where Auto and Python syntax differ -- Auto says "use" while Python says "import".

Let's see an example using the `sys` module:

<Listing number="8-1" file-name="using_sys.auto" caption="Using the sys module">

```auto
use sys

fn main() {
    print("The command line arguments are:")
    for arg in sys.argv {
        print(arg)
    }
}
```

```python
import sys


def main():
    print("The command line arguments are:")
    for arg in sys.argv:
        print(arg)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

First, we *import* the `sys` module using the `use sys` statement. Basically, this tells Auto that we want to use this module. The `sys` module contains functionality related to the Python interpreter and its environment -- the **sys**tem.

When `a2p` transpiles `use sys`, it outputs `import sys` in the Python code. The `sys` module is one of the built-in modules, so Python knows where to find it.

If it was not a built-in module, the Python interpreter would search for it in the directories listed in its `sys.path` variable. If the module is found, the statements in the body of that module are run and the module is made *available* for you to use. Note that the initialization is done only the *first* time that we import a module.

The `argv` variable in the `sys` module is accessed using the dotted notation -- `sys.argv`. This clearly indicates that this name is part of the `sys` module. Another advantage of this approach is that the name does not clash with any `argv` variable you might use in your own program.

The `sys.argv` variable is a *list* of strings (lists are explained in detail in a [later chapter](./ch10-data-structures.md#data-structures)). Specifically, `sys.argv` contains the list of *command line arguments* -- the arguments passed to your program using the command line.

If you are using an IDE to write and run these programs, look for a way to specify command line arguments to the program in the menus.

When you execute the program with arguments, Python stores the command line arguments in `sys.argv` for you to use. Remember, the name of the script running is always the first element in `sys.argv`. So, if you run `a2p using_sys.auto` and then run `python using_sys.py we are arguments`, you will have `'using_sys.py'` as `sys.argv[0]`, `'we'` as `sys.argv[1]`, `'are'` as `sys.argv[2]` and `'arguments'` as `sys.argv[3]`. Notice that counting starts from 0, not 1.

The `sys.path` contains the list of directory names where modules are imported from. Observe that the first string in `sys.path` is empty -- this indicates that the current directory is also part of the search path. This means that you can directly import modules located in the current directory. Otherwise, you will have to place your module in one of the directories listed in `sys.path`.

Note that the current directory is the directory from which the program is launched.

> **Note for Python Programmers:**
>
> Auto uses `use` instead of `import`. The `a2p` transpiler converts `use module_name` to `import module_name` automatically. When writing Auto code, always use `use` -- never write `import` directly, as `a2p` expects the `use` keyword for proper transpilation.

## Byte-compiled `.pyc` Files

Importing a module is a relatively costly affair, so Python does some tricks to make it faster. One way is to create *byte-compiled* files with the extension `.pyc` which is an intermediate form that Python transforms the program into. This `.pyc` file is useful when you import the module the next time from a different program -- it will be much faster since a portion of the processing required in importing a module is already done. These byte-compiled files are platform-independent.

Note: These `.pyc` files are usually created in a `__pycache__` directory. If Python does not have permission to write to files in that directory, then the `.pyc` files will *not* be created.

> **Note for Auto Programmers:**
>
> Byte-compiled files are a Python runtime optimization. Since Auto code is transpiled to Python before execution, this optimization applies to the generated Python code, not the original `.at` files. As an Auto programmer, you generally do not need to worry about `.pyc` files.

## The `from..import` Statement

If you want to directly import a specific variable or function into your program (to avoid typing the module name every time), you can use the `from module::item` syntax in Auto. The `a2p` transpiler converts this to Python's `from module import item` statement.

> **Warning:** In general, *avoid* using the `from..import` statement and prefer the plain `use` statement instead. This is because your program will avoid name clashes and will be more readable.

Let's see an example:

<Listing number="8-3" file-name="from_import.auto" caption="Using the from..import syntax">

```auto
use sys::argv

fn main() {
    print(f"The command line arguments are: $argv")
}
```

```python
from sys import argv


def main():
    print(f"The command line arguments are: {argv}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

In Auto, `use sys::argv` tells the transpiler to import only the `argv` variable from the `sys` module. The `::` syntax is borrowed from Rust-style path notation and is Auto's way of expressing "from this module, get this specific item".

When transpiled by `a2p`, this becomes `from sys import argv` in Python. Now you can use `argv` directly without the `sys.` prefix.

> **Note for Python Programmers:**
>
> Auto uses `use sys::argv` where Python uses `from sys import argv`. The `::` double-colon is Auto's namespace separator, similar to Rust. The `a2p` transpiler handles this conversion automatically.
>
> Also note that Auto uses `$` for string interpolation (e.g., `$argv`), while Python uses `{argv}` inside f-strings. The transpiler converts between the two.

## The `__name__` Attribute

Every Python module has a `__name__` attribute. If this is `'__main__'`, it implies that the module is being run standalone by the user. This is handy for figuring out whether the module is being run standalone or being imported.

In Auto, you don't need to deal with `__name__` directly. The `a2p` transpiler automatically wraps your `fn main()` inside the `if __name__ == "__main__":` guard in the generated Python code. This means your Auto program's `main` function will only run when the file is executed directly, not when it is imported as a module.

<Listing number="8-2" file-name="module_name.auto" caption="Using __name__ via Auto's main function">

```auto
fn main() {
    print("This program is being run by itself")
}
```

```python
def main():
    print("This program is being run by itself")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

In Auto, you simply define a `fn main()` function. The `a2p` transpiler recognizes this as the entry point and wraps the call to `main()` inside the `if __name__ == "__main__":` guard.

When you run the transpiled Python file directly (e.g., `python module_name.py`), `__name__` will be `'__main__'`, so `main()` gets called and you see the output:

```
This program is being run by itself
```

When another Python program imports this file (e.g., `import module_name`), `__name__` will be `'module_name'` (not `'__main__'`), so the `main()` function will *not* be called. Only the `def main():` function definition is loaded.

> **Note for Python Programmers:**
>
> In Python, you manually write `if __name__ == "__main__":` to guard your main code. In Auto, you simply define `fn main()` and the `a2p` transpiler adds the guard automatically. This is cleaner and less error-prone -- you never forget to add the guard.

## Making Your Own Modules

Creating your own modules in Auto is straightforward. Every `.at` file you create is already a module! You just need to make sure other programs can find it -- either by placing it in the same directory or by placing it in a directory listed in `sys.path`.

Here is a simple example of a module file. Save it as `mymodule.at`:

```auto
// mymodule.at

fn say_hi() {
    print("Hi, this is mymodule speaking.")
}

__version__ = "1.0"
```

Now, you can use this module in another Auto program. Save the following as `mymodule_demo.at`:

```auto
use mymodule

fn main() {
    mymodule.say_hi()
    print(f"Version: ${mymodule.__version__}")
}
```

When transpiled and run, this produces:

```
Hi, this is mymodule speaking.
Version: 1.0
```

**How It Works**

Notice that we use the same dotted notation to access members of the module: `mymodule.say_hi()` and `mymodule.__version__`. The `a2p` transpiler converts `use mymodule` to `import mymodule`, and the dotted access works exactly the same in both languages.

Here is a version using the `from..import` syntax:

```auto
use mymodule::say_hi
use mymodule::__version__

fn main() {
    say_hi()
    print(f"Version: $__version__")
}
```

The output is the same. However, notice that if there was already a `__version__` variable in the importing module, there would be a name clash. This is why it is always recommended to prefer the plain `use` statement even though it might make your program slightly longer.

> **Warning:** Avoid using `use module::*` (which would import everything from a module). This can lead to hard-to-debug name clashes.

> **Note for Python Programmers:**
>
> Auto's module creation is essentially the same as Python's. Every `.at` file is a module, just as every `.py` file is a module in Python. The `a2p` transpiler preserves the module structure when converting to Python.

## The `dir` Function

The built-in `dir()` function returns the list of names defined by an object. If the object is a module, this list includes functions, classes and variables defined inside that module.

This function can accept arguments. If the argument is the name of a module, the function returns the list of names from that specified module. If there is no argument, the function returns the list of names from the current module.

```python
$ python
>>> import sys

# get names of attributes in sys module
>>> dir(sys)
['__displayhook__', '__doc__',
'argv', 'builtin_module_names',
'version', 'version_info']
# only a few entries shown here

# get names of attributes for current module
>>> dir()
['__builtins__', '__doc__',
'__name__', '__package__', 'sys']

# create a new variable 'a'
>>> a = 5

>>> dir()
['__builtins__', '__doc__', '__name__', '__package__', 'sys', 'a']

# delete/remove a name
>>> del a

>>> dir()
['__builtins__', '__doc__', '__name__', '__package__', 'sys']
```

**How It Works**

First, we see the usage of `dir` on the imported `sys` module. We can see the huge list of attributes that it contains.

Next, we use the `dir` function without passing parameters to it. By default, it returns the list of attributes for the current module. Notice that the list of imported modules is also part of this list.

In order to observe `dir` in action, we define a new variable `a` and assign it a value, then check `dir` and we observe that there is an additional value in the list of the same name. We remove the variable/attribute of the current module using the `del` statement and the change is reflected again in the output of `dir`.

A note on `del`: This statement is used to *delete* a variable/name and after the statement has run, in this case `del a`, you can no longer access the variable `a` -- it is as if it never existed before at all.

Note that the `dir()` function works on *any* object. For example, run `dir(str)` for the attributes of the `str` (string) class.

## Packages

By now, you must have started observing the hierarchy of organizing your programs. Variables usually go inside functions. Functions and global variables usually go inside modules. What if you wanted to organize modules? That's where packages come into the picture.

Packages are folders of modules with a special `__init__.py` file that indicates to Python that this folder is special because it contains Python modules.

Let's say you want to create a package called `world` with subpackages `asia`, `africa`, etc. and these subpackages in turn contain modules like `india`, `madagascar`, etc.

This is how you would structure the folders:

```
- <some folder present in the sys.path>/
    - world/
        - __init__.py
        - asia/
            - __init__.py
            - india/
                - __init__.py
                - foo.py
        - africa/
            - __init__.py
            - madagascar/
                - __init__.py
                - bar.py
```

Packages are just a convenience to organize modules hierarchically. You will see many instances of this in the [standard library](./ch14-stdlib.md#stdlib).

> **Note for Auto Programmers:**
>
> Auto does not yet have its own package system separate from Python's. When transpiled, Auto modules follow Python's package conventions. In future versions, Auto may introduce its own module resolution mechanism.

## Summary

Just like functions are reusable parts of programs, modules are reusable programs. Packages are another hierarchy to organize modules. The standard library that comes with Python is an example of such a set of packages and modules.

We have seen how to use these modules and create our own modules. Here are the key takeaways for Auto:

- **`use module`** -- import a module. Auto's `use` keyword becomes Python's `import` in the transpiled output.
- **`use module::item`** -- import a specific item from a module. This becomes Python's `from module import item`.
- **`fn main()`** -- Auto's entry point. The `a2p` transpiler automatically wraps it with `if __name__ == "__main__":` in the Python output.
- **Every `.at` file is a module** -- you can create reusable modules simply by writing Auto code in a file.
- **`dir()`** -- inspect the available names in a module (Python built-in function).

Next, we will learn about data structures.
