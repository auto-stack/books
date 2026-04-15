# 输入与输出

在某些情况下，你的程序需要与用户进行交互。例如，你可能想要接收用户的输入，然后打印一些结果。我们可以分别使用 `input()` 函数和 `print` 函数来实现这一点。

对于输出，我们还可以使用 `str`（字符串）类的各种方法。例如，你可以使用 `rjust` 方法获取一个右对齐到指定宽度的字符串。详情请参阅 `help(str)`。

另一种常见的输入/输出类型是处理文件。创建、读取和写入文件的能力对于许多程序来说是必不可少的，我们将在本章中探讨这一方面。

## 从用户获取输入

将此程序保存为 `input.auto`：

<Listing number="12-1" file-name="input.auto" caption="获取用户输入">

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

输出：

```
$ auto run input.auto
What is your name? Swaroop
Hello, Swaroop!
```

**工作原理**

`input()` 函数接受一个字符串作为参数，并将其作为提示显示给用户。然后它等待用户输入内容并按下回车键。一旦用户输入并按下回车键，`input()` 函数将返回用户输入的文本。

我们将返回的值赋给变量 `name`，然后使用 [f-字符串](./ch04-basics.md#formatting) 打印一条个性化的问候语。在 Auto 中，f-字符串使用 `$var` 代替 Python 的 `{var}` 进行变量插值，但概念是完全相同的。

> **Python 程序员注意：**
>
> `input()` 函数在 Auto 和 Python 中的工作方式完全相同。`a2p` 转译器会原样传递 `input()` 调用。本示例中唯一可见的区别是 f-字符串语法：Auto 使用 `$var`，而 Python 使用 `{var}`。

## 文件输入/输出

你可以通过使用内置的 `open` 函数创建文件对象，并使用其 `read`、`readline` 或 `write` 方法来读取或写入文件。能否读取或写入文件取决于你为打开文件指定的模式。最后，当你完成文件操作后，调用 `close` 方法告诉系统我们已不再使用该文件。

示例（保存为 `file_io.auto`）：

<Listing number="12-2" file-name="file_io.auto" caption="读写文件">

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

输出：

```
$ auto run file_io.auto
Programming is fun
When the work is done
if you wanna make your work also fun:
    use Auto!
```

**工作原理**

请注意，我们可以直接使用 `open` 函数创建一个新的文件对象。我们使用内置的 `open` 函数并指定文件名和打开模式来打开文件（如果文件不存在则会创建）。模式可以是读取模式（`'r'`）、写入模式（`'w'`）或追加模式（`'a'`）。我们还可以指定是以文本模式（`'t'`）还是二进制模式（`'b'`）进行读取、写入或追加。实际上还有更多可用的模式，`help(open)` 会给你更多细节。默认情况下，`open()` 将文件视为文本文件并以读取模式打开。

在我们的示例中，我们首先以写入文本模式打开/创建文件，并使用文件对象的 `write` 方法将字符串变量 `poem` 写入文件，然后最终 `close` 文件。

接下来，我们再次打开同一个文件进行读取。我们不需要指定模式，因为"读取文本文件"是默认模式。我们使用 `read` 方法读取文件的全部内容并打印。

> **注意：**
>
> 使用完文件后，请务必记得关闭文件。另一种方法是使用 `with` 语句，它会自动为你关闭文件。在 Auto 中，`with` 语句的工作方式与 Python 相同。例如：
>
> ```auto
> with open("poem.txt") as f {
>     print(f.read())
> }
> ```

> **Python 程序员注意：**
>
> Auto 中的文件 I/O 与 Python 完全相同。`a2p` 转译器会原样传递 `open()`、`f.write()`、`f.read()` 和 `f.close()` 调用。Auto 中的 `use io` 语句在 Python 中转换为 `import io`。文件模式（`'r'`、`'w'`、`'a'`、`'b'`、`'t'`）在两种语言中是相同的。

## Pickle

Python 提供了一个名为 `pickle` 的标准模块，你可以用它将_任何_普通 Python 对象存储在文件中，并在以后将其取回。这被称为将对象*持久化*存储。

由于 Auto 转译为 Python，你可以通过 `use pickle` 使用 `pickle` 模块。

示例（保存为 `using_pickle.auto`）：

<Listing number="12-3" file-name="using_pickle.auto" caption="使用 pickle">

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

输出：

```
$ auto run using_pickle.auto
['apple', 'mango', 'carrot']
```

**工作原理**

要将对象存储在文件中，我们首先必须以__写入二进制__模式 `open` 文件，然后调用 `pickle` 模块的 `dump` 函数。这个过程被称为_序列化_（pickling）。

接下来，我们使用 `pickle` 模块的 `load` 函数检索对象，该函数返回该对象。这个过程被称为_反序列化_（unpickling）。

> **注意：**
>
> `pickle` 模块是 Python 特有的。由于 Auto 转译为 Python，pickle 在 Auto 代码中可以无缝使用。但是，生成的 `.data` 文件不能被非 Python 程序读取。如果你需要跨语言的序列化格式，请考虑使用 JSON。

## Unicode

到目前为止，当我们编写和使用字符串，或者读写文件时，我们只使用了简单的英文字符。英语和非英语字符都可以用 Unicode 表示（详情请参阅本节末尾的文章），Python 3 默认将字符串变量（想想我们用单引号、双引号或三引号写的所有文本）存储为 Unicode。

当数据通过互联网发送时，我们需要以字节的形式发送——这是计算机容易理解的形式。将 Unicode（即 Python 存储字符串时使用的格式）转换为字节的规则称为_编码_。一种流行的编码是 UTF-8。我们可以通过在 `open` 函数中使用一个简单的关键字参数来以 UTF-8 进行读写。

示例（保存为 `unicode.auto`）：

<Listing number="12-4" file-name="unicode.auto" caption="Unicode 文本">

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

输出：

```
$ auto run unicode.auto
Imagine non-English language here
```

**工作原理**

我们使用 `open` 函数，然后在第一个 open 语句中使用 `encoding` 参数来编码消息，在第二个 open 语句中再次使用 `encoding` 参数来解码消息。请注意，我们只应在文本模式下在 `open` 语句中使用编码。

在 Auto 中（与 Python 3 一样），字符串默认就是 Unicode，因此你可以在源代码中自由混合英语和非英语字符。`encoding = "utf-8"` 参数确保文件使用 UTF-8 编码进行写入和读取，该编码支持几乎所有语言的字符。

> **Python 程序员注意：**
>
> Auto 中的 Unicode 处理与 Python 3 相同。`a2p` 转译器会原样传递带有 `encoding` 参数的 `open()` 调用。Auto 字符串默认就是 Unicode，就像 Python 3 字符串一样。不需要 Python 2 中要求的 `# encoding=utf-8` 注释。

你可以通过阅读以下文章来了解更多关于这个主题的信息：

- ["每个软件开发者绝对、肯定必须知道的关于 Unicode 和字符集的最少知识"](http://www.joelonsoftware.com/articles/Unicode.html)
- [Python Unicode Howto](http://docs.python.org/3/howto/unicode.html)
- [Pragmatic Unicode talk by Nat Batchelder](http://nedbatchelder.com/text/unipain.html)

## 小结

我们讨论了各种类型的输入/输出、文件处理、pickle 模块以及 Unicode。

接下来，我们将探讨异常的概念。
