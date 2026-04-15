# 异常

当你的程序中出现_异常_情况时，就会发生异常（Exceptions）。例如，如果你要读取一个文件，但该文件不存在怎么办？或者如果程序运行时你意外删除了它怎么办？这些情况都使用**异常**来处理。

同样，如果你的程序中包含无效的语句怎么办？这由 Python 来处理——它会**抛出**双手并告诉你有一个**错误**。

## 错误

考虑一个简单的 `print` 函数调用。如果我们把 `print` 拼写成了 `Print` 会怎样？注意大小写。在这种情况下，Python 会_引发_一个语法错误。

<Listing number="13-1" file-name="error.auto" caption="错误">

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

输出：

```
$ auto run error.auto
Hello
Traceback (most recent call last):
  File "error.auto", line 4, in <module>
NameError: name 'spam' is not defined
```

**工作原理**

观察到一个 `NameError` 被引发，同时还打印了检测到错误的位置。这就是该错误的**错误处理器**所做的事情。在这个例子中，变量 `spam` 在使用之前从未被定义，因此 Python 引发了 `NameError`。

> **Python 程序员注意：**
>
> 错误在 Auto 和 Python 中的工作方式完全相同。由于 Auto 通过 `a2p` 转译为 Python，所有的语法错误和运行时错误最终都是 Python 错误。Auto 自身的错误系统使用 `!T`（错误类型）和 `!`（抛出运算符）进行原生错误处理，但在目标为 Python 时，应用的是标准的 Python 错误和异常机制。

## 异常

我们将**尝试**从用户那里读取输入。输入下面的第一行并按下回车键。当你的电脑提示你输入时，在 Mac 上按 `[ctrl-d]` 或在 Windows 上按 `[ctrl-z]`，看看会发生什么。（如果你使用的是 Windows 并且两个选项都不起作用，你可以在命令提示符中尝试 `[ctrl-c]` 来生成 `KeyboardInterrupt` 错误。）

```python
>>> s = input('Enter something --> ')
Enter something --> Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
EOFError
```

Python 引发了一个名为 `EOFError` 的错误，这基本上意味着它在意想不到的地方找到了一个*文件结束*符号（由 `ctrl-d` 表示）。

## 处理异常

我们可以使用 `try..except` 语句来处理异常。我们基本上将常规语句放在 try 块中，并将所有错误处理器放在 except 块中。

示例（保存为 `handle.auto`）：

<Listing number="13-2" file-name="handle.auto" caption="处理异常">

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

输出：

```
# 按 ctrl + d
$ auto run handle.auto
Enter something:
Why did you do an EOF on me?

# 按 ctrl + c
$ auto run handle.auto
Enter something: ^C
You cancelled the operation.

$ auto run handle.auto
Enter something: No exceptions
You entered: No exceptions
```

**工作原理**

我们将所有可能引发异常/错误的语句放在 `try` 块中，然后在 `except` 子句/块中放置适当错误/异常的处理器。`except` 子句可以处理单个指定的错误或异常，或者一个括号括起来的错误/异常列表。如果没有提供错误或异常的名称，它将处理_所有_错误和异常。

请注意，每个 `try` 子句必须至少关联一个 `except` 子句。否则，拥有 try 块还有什么意义呢？

如果任何错误或异常未被处理，则会调用默认的 Python 处理器，它只是停止程序的执行并打印错误消息。我们在上面已经看到过这种情况。

你还可以将 `else` 子句与 `try..except` 块关联。如果没有发生异常，则执行 `else` 子句。

在下一个示例中，我们还将看到如何获取异常对象，以便我们可以检索额外的信息。

> **Python 程序员注意：**
>
> Auto 中的 `try`/`except`/`else` 语法与 Python 相同。`a2p` 转译器会原样传递这些块。唯一可见的 Auto 特定语法差异是 Auto 使用 `{}` 花括号来表示代码块，而不是 Python 的缩进。

## 引发异常

你可以使用 `raise` 语句_引发_异常，提供错误/异常的名称以及要_抛出_的异常对象。

你可以引发的错误或异常应该是一个类，该类直接或间接地必须是 `Exception` 类的派生类。

示例（保存为 `raise.auto`）：

<Listing number="13-3" file-name="raise.auto" caption="引发异常">

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

输出：

```
$ auto run raise.auto
Enter something: a
ShortInputException: The input was 1 long, expected at least 3

$ auto run raise.auto
Enter something: abc
No exception was raised.
```

**工作原理**

在这里，我们创建了自己的异常类型。这个新的异常类型叫做 `ShortInputException`。它有两个字段——`length` 表示给定输入的长度，`atleast` 表示程序期望的最小长度。

在 Auto 中，我们使用 `type` 关键字定义自定义异常类型，包含类似结构体的字段声明和一个 `init` 构造函数。`to_string` 方法提供了异常的人类可读表示。我们使用 `raise ShortInputException{text.len(), 3}` 来引发异常，这使用了 Auto 的结构体初始化语法。

在 `except` 子句中，我们提到了错误类，它将被存储 `as` 变量名以保存相应的错误/异常对象。这类似于函数调用中的参数和实参。在这个特定的 `except` 子句中，我们使用异常对象的 `to_string` 方法向用户打印适当的消息。

> **Python 程序员注意：**
>
> 在 Auto 中，自定义异常类使用 `type` 关键字定义，包含显式的字段声明和 `init` 方法，而不是 Python 的 `class` 语法。`a2p` 转译器将 Auto 的 `type` 块转换为继承自 `Exception` 的 Python `class` 定义。Auto 中的 `raise ShortInputException{args}` 语法在 Python 中会被转换为 `raise ShortInputException(args)`。Auto 的原生错误系统也支持 `!T`（错误类型）和 `!`（抛出运算符），但在目标为 Python 时，使用 `raise` 配合异常类是标准方法。

## Try...Finally

假设你正在程序中读取一个文件。你如何确保无论是否引发异常，文件对象都能正确关闭？这可以使用 `finally` 块来实现。

将此程序保存为 `finally.auto`：

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

输出：

```
$ auto run finally.auto
Programming is fun
When the work is done
if you wanna make your work also fun:
    use Auto!
(Cleaning up: Closed the file)
```

**工作原理**

我们执行常规的文件读取操作。我们使用 `for` 循环逐行遍历文件。如果发生 `IOError`（例如，如果文件 `poem.txt` 不存在），我们打印一条消息。

需要注意的重要一点是 `finally` 块。无论发生什么——是否发生异常——`finally` 块_总是_被执行。这对于清理操作（如关闭文件、释放资源或恢复状态）非常有用。

请注意，在 Python 中，赋值为 0 或 `None` 的变量，或者是空序列或集合的变量被认为是 `False`。这就是为什么我们可以在 Python 代码中使用 `if f:` 来检查文件是否成功打开。

## `with` 语句

在 `try` 块中获取资源，然后在 `finally` 块中释放资源是一种常见的模式。因此，还有一个 `with` 语句可以更简洁地实现这一点。

保存为 `with_example.auto`：

<Listing number="13-5" file-name="with_example.auto" caption="使用 with 语句">

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

输出：

```
$ auto run with_example.auto
Programming is fun
When the work is done
if you wanna make your work also fun:
    use Auto!
```

**工作原理**

输出应该与上一个示例相同。这里的区别在于我们使用 `open` 函数配合 `with` 语句——我们将关闭文件的工作交给 `with open` 自动处理。

在幕后发生的事情是，`with` 语句使用了一个协议。它获取 `open` 语句返回的对象，在这种情况下我们称之为 "thefile"。

它_总是_在开始其下方的代码块之前调用 `thefile.__enter__` 函数，并在完成代码块之后_总是_调用 `thefile.__exit__`。

因此，我们在 `finally` 块中编写的代码应该由 `__exit__` 方法自动处理。这就是帮助我们避免反复使用显式 `try..finally` 语句的原因。

> **Python 程序员注意：**
>
> Auto 中的 `with` 语句与 Python 的 `with` 语句工作方式完全相同。`a2p` 转译器会原样传递 `with` 块。Auto 使用 `{}` 花括号来表示块体，而不是 Python 的缩进，但语义是相同的——上下文管理器的 `__enter__` 和 `__exit__` 方法会在适当的时候被调用。

## 小结

我们讨论了 `try..except` 和 `try..finally` 语句的用法。我们看到了如何创建自己的异常类型以及如何引发异常。我们还看到了用于更简洁资源管理的 `with` 语句。

接下来，我们将探索 Python 标准库。
