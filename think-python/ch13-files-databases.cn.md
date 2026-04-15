# 文件与数据库

到目前为止，我们见过的大多数程序都是**短暂的**（ephemeral），因为它们运行一小段时间并产生输出，但当它们结束时，数据就消失了。每次运行短暂程序时，它都从零开始。

其他程序是**持久的**（persistent）：它们长时间运行（或一直运行）；它们至少将一些数据保存在长期存储中；如果关闭后重启，它们会从上次中断的地方继续。

程序维护数据的一种简单方法是读写文本文件。一种更通用的替代方案是将数据存储在数据库中。数据库是经过特殊组织的文件，比文本文件可以更高效地读写，并提供额外的功能。

在本章中，我们将编写读写文本文件和处理文件系统的程序。但在处理文件之前，你必须先找到它，所以我们将从文件名、路径和目录开始。

## 文件名和路径

文件被组织到**目录**（directories）中，也称为"文件夹"。每个运行的程序都有一个**当前工作目录**（current working directory），这是大多数操作的默认目录。例如，当你打开一个文件时，程序会在当前工作目录中查找它。

`os` 模块提供了处理文件和目录的函数（"os" 代表"操作系统"）。它提供了一个名为 `getcwd` 的函数来获取当前工作目录的名称。

```auto
use os

let cwd = os.getcwd()
print(cwd)  // 例如 "/home/dinsdale"
```

像 `'/home/dinsdale'` 这样标识文件或目录的字符串称为**路径**（path）。

像 `'memo.txt'` 这样的简单文件名也被视为路径，但它是一个**相对路径**（relative path），因为它指定的是相对于当前目录的文件名。以 `/` 开头的路径不依赖于当前目录 -- 它被称为**绝对路径**（absolute path）。要查找文件的绝对路径，可以使用 `abspath`。

```auto
os.path.abspath("memo.txt")  // 例如 "/home/dinsdale/memo.txt"
```

`os` 模块还提供了其他处理文件名和路径的函数。`listdir` 返回给定目录内容的列表，包括文件和其他目录。

```auto
os.listdir("photos")  // 例如 ["notes.txt", "jan-2023", "feb-2023", "mar-2023"]
```

要检查文件或目录是否存在，可以使用 `os.path.exists`。

```auto
os.path.exists("photos")  // true
os.path.exists("photos/apr-2023")  // false
```

要检查路径是文件还是目录，可以使用 `isdir` 和 `isfile`。

```auto
os.path.isdir("photos")  // true
os.path.isfile("photos/notes.txt")  // true
```

处理路径的一个挑战是它们在不同操作系统上看起来不同。在 macOS 和 Linux 等 UNIX 系统上，路径中的目录和文件名用正斜杠 `/` 分隔。Windows 使用反斜杠 `\`。

或者，要编写在两个系统上都能工作的代码，可以使用 `os.path.join`，它使用操作系统适当的分隔符将目录和文件名连接成路径。

```auto
os.path.join("photos", "jan-2023", "photo1.jpg")  // "photos/jan-2023/photo1.jpg"
```

> **Python 程序员注意：**
>
> Auto 使用 `os`、`os.path`、`os.getcwd()`、`os.listdir()`、`os.path.join()`、`os.path.exists()`、`os.path.isdir()`、`os.path.isfile()` 的方式与 Python 相同。`a2p` 转译器会直接转换这些调用。

## 格式化字符串

程序存储数据的一种方法是将其写入文本文件。例如，假设你是一个观察骆驼的人，你想记录在观察期间看到的骆驼数量。假设在一年半的时间里，你看到了 `23` 只骆驼。

```auto
let num_years = 1.5
let num_camels = 23
```

要组合字符串和其他值，我们可以在 Auto 中使用**格式化字符串**（f-string），它使用 `$var` 语法来插值变量。

```auto
let line1 = f"I have spotted $num_camels camels"
print(line1)  // I have spotted 23 camels
```

格式化字符串中可以有多个变量。

```auto
let line2 = f"In $num_years years I have spotted $num_camels camels"
print(line2)  // In 1.5 years I have spotted 23 camels
```

表达式中还可以包含函数调用。

```auto
let months = int(num_years * 12)
let line3 = f"In $months months I have spotted $num_camels camels"
print(line3)  // In 18 months I have spotted 23 camels
```

所以我们可以这样将数据写入文本文件。

```auto
let writer = open("camel-spotting-book.txt", "w")
writer.write(f"Years of observation: $num_years\n")
writer.write(f"Camels spotted: $num_camels\n")
writer.close()
```

两个格式化字符串都以 `\n` 结尾，这会添加一个换行符。

> **Python 程序员注意：**
>
> Python 在 f-string 中使用 `{var}` 语法，而 Auto 使用 `$var`。`a2p` 转译器会自动将 `f"$var"` 转换为 `f"{var}"`。

<Listing number="13-1" file-name="file_paths.auto" caption="使用 os 和格式化字符串读写文件">

```auto
use os

fn main() {
    // 当前工作目录
    let cwd = os.getcwd()
    print("Current directory:", cwd)

    // 绝对路径
    let abs_path = os.path.abspath("memo.txt")
    print("Absolute path of 'memo.txt':", abs_path)

    // Auto 中的格式化字符串
    let num_years = 1.5
    let num_camels = 23

    let line1 = f"Years of observation: $num_years"
    let line2 = f"Camels spotted: $num_camels"
    print(line1)
    print(line2)

    // 带表达式的格式化字符串
    let months = int(num_years * 12)
    let line3 = f"In $months months I have spotted $num_camels camels"
    print(line3)

    // os.path 操作
    let joined = os.path.join("photos", "jan-2023", "photo1.jpg")
    print("Joined path:", joined)

    // 检查路径是否存在
    print("Does 'photos' exist?", os.path.exists("photos"))

    // isdir 和 isfile 检查
    print("Is '.' a directory?", os.path.isdir("."))
    print("Is 'memo.txt' a file?", os.path.isfile("memo.txt"))
}
```

```python
import os


def main():
    # 当前工作目录
    cwd = os.getcwd()
    print(f"Current directory: {cwd}")

    # 绝对路径
    abs_path = os.path.abspath("memo.txt")
    print(f"Absolute path of 'memo.txt': {abs_path}")

    # Auto 中的格式化字符串
    num_years = 1.5
    num_camels = 23

    line1 = f"Years of observation: {num_years}"
    line2 = f"Camels spotted: {num_camels}"
    print(line1)
    print(line2)

    # 带表达式的格式化字符串
    months = int(num_years * 12)
    line3 = f"In {months} months I have spotted {num_camels} camels"
    print(line3)

    # os.path 操作
    joined = os.path.join("photos", "jan-2023", "photo1.jpg")
    print(f"Joined path: {joined}")

    # 检查路径是否存在
    print(f"Does 'photos' exist? {os.path.exists('photos')}")

    # isdir 和 isfile 检查
    print(f"Is '.' a directory? {os.path.isdir('.')}")
    print(f"Is 'memo.txt' a file? {os.path.isfile('memo.txt')}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`os` 模块提供了跨平台的文件系统操作函数。`os.getcwd()` 返回当前工作目录。`os.path.abspath()` 将相对路径转换为绝对路径。`os.path.join()` 使用操作系统正确的分隔符构造路径。`os.path.exists()`、`os.path.isdir()` 和 `os.path.isfile()` 检查路径的存在性和类型。Auto 的 `f"$var"` 格式化字符串直接插值变量，类似于 Python 的 `f"{var}"` 语法。

## YAML

程序读写文件的原因之一是存储**配置数据**（configuration data），即指定程序应该做什么以及如何做的信息。Python 中的 `yaml` 模块提供了处理 YAML 文件的函数，YAML 文件是格式化的文本文件，便于人类和程序读写。

将字典等对象转换为字符串的过程称为**序列化**（serialization）。将字符串转换回对象的过程称为**反序列化**（deserialization）。

在 Auto 中，配置通常通过 `pac.at` 项目文件处理，而不是 YAML。然而，序列化和反序列化的概念在使用 JSON 或其他基于文本的数据格式时同样适用。

## 存储数据结构

在前面的章节中，我们处理过列表和字典等数据结构。一个常见的任务是将这些结构存储在文本文件中，以便在程序运行之间持久化。

一种方法是使用简单的文本格式。例如，要存储一个将排序后的字母字符串映射到字谜单词列表的字典，可以将每个键值对写在单独的一行上。

另一种方法是使用 JSON（JavaScript Object Notation），一种广泛支持的文本格式，将数据结构表示为字符串。大多数编程语言，包括 Auto 和 Python，都提供内置或库支持来读写 JSON。

## 检查等效文件

现在让我们回到一个实际任务：搜索包含相同数据的不同文件。一种检查方法是读取两个文件的内容并进行比较。

如果文件包含图像，我们必须用模式 `'rb'` 打开它们，其中 `'r'` 表示我们要读取内容，`'b'` 表示**二进制模式**（binary mode）。在二进制模式下，内容不被解释为文本 -- 它们被视为字节序列。

```auto
let data1 = open("photo1.jpg", "rb").read()
let data2 = open("photo2.jpg", "rb").read()
print(data1 == data2)  // false
```

如果我们有大量文件并且想知道是否有任何两个文件包含相同的数据，比较每对文件会很低效。另一种方法是使用**哈希函数**（hash function），它接受文件内容并计算一个**摘要**（digest），通常是一个大整数。如果两个文件包含相同的数据，它们将有相同的摘要。

`hashlib` 模块提供了几个哈希函数。`md5` 函数常用于此目的。思路是为每个文件计算摘要，将文件路径存储在以摘要为键的字典中，然后检查是否有任何摘要映射到多个文件。

## 遍历目录

以下函数接受我们要搜索的目录作为参数。它使用 `listdir` 循环遍历目录的内容。当找到文件时，打印其完整路径。当找到目录时，递归调用自身来搜索子目录。

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

我们可以这样使用：

```auto
walk("photos")
```

结果的顺序取决于操作系统的细节。

<Listing number="13-2" file-name="walk_directory.auto" caption="递归遍历目录">

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
    // 创建一个小的演示目录结构
    os.makedirs("demo/photos/jan-2023", exist_ok=true)
    os.makedirs("demo/photos/feb-2023", exist_ok=true)

    // 创建一些演示文件
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

    // 遍历目录
    print("Walking 'demo/photos':")
    walk("demo/photos")

    // 列出目录内容
    print()
    print("os.listdir('demo/photos'):", os.listdir("demo/photos"))
    print("os.listdir('demo/photos/jan-2023'):", os.listdir("demo/photos/jan-2023"))

    // 检查文件与目录
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
    # 创建一个小的演示目录结构
    os.makedirs("demo/photos/jan-2023", exist_ok=True)
    os.makedirs("demo/photos/feb-2023", exist_ok=True)

    # 创建一些演示文件
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

    # 遍历目录
    print("Walking 'demo/photos':")
    walk("demo/photos")

    # 列出目录内容
    print()
    print(f"os.listdir('demo/photos'): {os.listdir('demo/photos')}")
    print(f"os.listdir('demo/photos/jan-2023'): {os.listdir('demo/photos/jan-2023')}")

    # 检查文件与目录
    print()
    print(f"isdir('demo/photos'): {os.path.isdir('demo/photos')}")
    print(f"isfile('demo/photos/notes.txt'): {os.path.isfile('demo/photos/notes.txt')}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`walk` 函数是一个递归目录遍历器。它首先使用 `os.listdir()` 列出给定目录的内容。对于每个条目，它使用 `os.path.join()` 构造完整路径。如果条目是文件（`os.path.isfile()`），它打印路径。如果条目是目录（`os.path.isdir()`），它递归调用自身来探索子目录。这种模式 -- 处理当前级别的文件并递归进入子目录 -- 是递归在实际编程中最常见的用途之一。

<Listing number="13-3" file-name="word_list.auto" caption="从文件构建单词列表">

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
    // 通过读取目录中的文本文件来构建单词列表
    os.makedirs("demo_texts", exist_ok=true)

    // 创建示例文本文件
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

    // 从所有 .txt 文件中收集唯一单词
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
                // 清理单词：去除标点，转小写
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

    // 显示排序后的唯一单词
    let sorted_words = sorted(word_set.keys())
    print()
    print("Unique words (sorted):")
    print(sorted_words)

    // 使用格式化字符串将单词列表写入文件
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
    # 通过读取目录中的文本文件来构建单词列表
    os.makedirs("demo_texts", exist_ok=True)

    # 创建示例文本文件
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

    # 从所有 .txt 文件中收集唯一单词
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
                # 清理单词：去除标点，转小写
                cleaned = word.strip(",.!?").lower()
                if cleaned != "":
                    word_set[cleaned] = 1
                    total_words += 1

    print(f"Files read: {file_count}")
    print(f"Total word tokens: {total_words}")
    print(f"Unique words: {len(word_set)}")

    # 显示排序后的唯一单词
    sorted_words = sorted(word_set.keys())
    print()
    print("Unique words (sorted):")
    print(sorted_words)

    # 使用格式化字符串将单词列表写入文件
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

**工作原理**

这个例子将文件 I/O 与第 12 章的单词处理技术结合起来。它创建示例文本文件，然后读取所有文件来构建一个全面的单词列表。对于目录中的每个 `.txt` 文件，它读取内容、分割成单词、通过去除标点和转为小写来清理每个单词，并将其添加到字典中以跟踪唯一单词。最后，它使用 `f"$var"` 格式化字符串将结果写入新文件。这种模式 -- 从目录读取文件、处理内容、写入结果 -- 在数据处理管道中极其常见。

## 调试

在读写文件时，你可能会遇到空白字符的问题。这些错误很难调试，因为空白字符通常是不可见的。例如，这里有一个字符串，包含空格、用 `\t` 表示的制表符和用 `\n` 表示的换行符。当我们打印它时，看不到空白字符。

```auto
let s = "1 2\t 3\n 4"
print(s)
```

内置函数 `repr` 可以帮助。它接受任何对象作为参数，返回对象的字符串表示。对于字符串，它用反斜杠序列表示空白字符。

```auto
print(repr(s))  // '1 2\t 3\n 4'
```

这对调试很有帮助。

你可能遇到的另一个问题是，不同系统使用不同的字符来表示行尾。有些系统使用换行符，用 `\n` 表示。其他系统使用回车符，用 `\r` 表示。有些系统两者都使用。如果你在不同系统之间移动文件，这些不一致可能会导致问题。

文件名大小写是你在不同操作系统之间工作时可能遇到的另一个问题。在 macOS 和 UNIX 中，文件名可以包含小写和大写字母、数字和大多数符号。但许多 Windows 应用程序忽略大小写之间的差异。

## 术语表

**短暂的（ephemeral）：**
短暂程序通常运行一小段时间，结束时数据丢失。

**持久的（persistent）：**
持久程序无限期运行，并至少将一些数据保存在永久存储中。

**目录（directory）：**
文件和其他目录的集合。

**当前工作目录（current working directory）：**
除非指定了其他目录，程序使用的默认目录。

**路径（path）：**
指定一系列目录的字符串，通常通向一个文件。

**相对路径（relative path）：**
从当前工作目录或某个其他指定目录开始的路径。

**绝对路径（absolute path）：**
不依赖于当前目录的路径。

**配置数据（configuration data）：**
通常存储在文件中的数据，指定程序应该做什么以及如何做。

**序列化（serialization）：**
将对象转换为字符串。

**反序列化（deserialization）：**
将字符串转换为对象。

**数据库（database）：**
其内容经过组织以高效执行某些操作的文件。

**二进制模式（binary mode）：**
一种打开文件的方式，使内容被解释为字节序列而不是字符序列。

**哈希函数（hash function）：**
接受一个对象并计算一个整数的函数，有时称为摘要。

**摘要（digest）：**
哈希函数的结果，特别是当它用于检查两个对象是否相同时。

## 练习

### 练习

编写一个名为 `replace_all` 的函数，接受一个模式字符串、一个替换字符串和两个文件名作为参数。它应该读取第一个文件并将内容写入第二个文件（必要时创建）。如果模式字符串出现在内容的任何地方，应该将其替换为替换字符串。

### 练习

编写一个函数，接受目录名作为参数，遍历所有子目录，收集所有以给定扩展名（如 `.txt` 或 `.jpg`）结尾的文件。函数应返回所有匹配文件的完整路径列表。

### 练习

使用本章中的 `walk` 函数和 `md5_digest` 概念，编写一个程序来搜索目录中的重复文件 -- 包含完全相同数据的文件。你的程序应该：

1. 遍历目录及其子目录。

2. 对于每个文件，计算其内容的哈希摘要。

3. 将文件路径存储在以摘要为键的字典中。

4. 打印任何具有相同摘要的文件组。

提示：在 Python 中使用 `hashlib` 模块，或在 Auto 中实现一个简单的校验和。
