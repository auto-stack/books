# 基础

仅仅打印 `hello world` 是不够的，对吧？你想做更多的事情——你想接收一些输入，对它进行处理，然后输出结果。我们可以通过 Auto 中的常量和变量来实现这一点，在本章中我们还将学习一些其他概念。

## 注释

_注释_是 `//` 符号右侧的任何文本，主要用作程序读者的笔记。

例如：

```auto
print("Hello, World!") // 这是一个行内注释
```

或者：

```auto
// 这是代码前面的注释
print("Hello, World!")
```

在程序中尽可能多地使用有用的注释来：

- 解释假设条件
- 解释重要的决定
- 解释重要的细节
- 解释你正在尝试解决的问题
- 解释你在程序中试图克服的困难，等等。

[*代码告诉你怎么做，注释应该告诉你为什么*](http://www.codinghorror.com/blog/2006/12/code-tells-you-how-comments-tell-you-why.html)。

这对程序的读者很有帮助，使他们能轻松理解程序在做什么。记住，那个人也可能是六个月后的你自己！

> **Python 程序员注意：**
>
> Auto 使用 `//` 表示注释，而 Python 使用 `#`。当通过 `a2p` 转译时，`//` 注释会自动转换为输出 Python 代码中的 `#` 注释。

让我们通过一个小程序来实践注释的用法：

<Listing number="4-1" file-name="comments.auto" caption="在 Auto 中使用注释">

```auto
// 这是一个注释
// 这也是一个注释

fn main() {
    print("Hello, World!") // 这也是一个注释
}
```

```python
# 这是一个注释
# 这也是一个注释


def main():
    print("Hello, World!")  # 这也是一个注释


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

前两行是整行注释——它们都以 `//` 开头，编译器会忽略整行。在 `main()` 中，`// 这也是一个注释` 部分是行内注释。编译器会忽略从 `//` 到行末的所有内容，因此 `print("Hello, World!")` 正常执行，而注释只是供人类阅读的。

## 字面常量

字面常量的例子有数字 `5`、`1.23`，或字符串 `"This is a string"` 和 `"It's a string!"`。

之所以称为字面量，是因为它是_字面意义上的_——你直接使用它的值。数字 `2` 始终代表它自己，别无其他——它是一个_常量_，因为它的值不能被改变。因此，这些都被称为字面常量。

## 数字

数字主要有两种类型——整数和浮点数。

整数的一个例子是 `2`，它就是一个整数。

浮点数（简称_浮点数_）的例子有 `3.23` 和 `52.3E-4`。`E` 表示法表示 10 的幂。在这种情况下，`52.3E-4` 表示 `52.3 * 10^-4`。

> **有经验的程序员注意：**
>
> 没有单独的 `long` 类型。`int` 类型可以是任意大小的整数。为了提高可读性，你可以在数字字面量中使用下划线，如 `2_000_000`。

<Listing number="4-2" file-name="numbers.auto" caption="在 Auto 中使用数字">

```auto
fn main() {
    // 整数
    let a = 5
    let b = -3
    let c = 2_000_000  // 下划线用于提高可读性

    // 浮点数
    let pi = 3.14159
    let small = 1.5e-4

    // 算术运算
    print(a + b)
    print(a * b)
    print(a / b)
    print(pi * c)
}
```

```python
def main():
    # 整数
    a = 5
    b = -3
    c = 2_000_000  # 下划线用于提高可读性

    # 浮点数
    pi = 3.14159
    small = 1.5e-4

    # 算术运算
    print(a + b)
    print(a * b)
    print(a / b)
    print(pi * c)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

我们使用 `let` 声明了整数变量 `a`、`b` 和 `c`。注意 `c` 使用下划线分隔数字组——这是从 Python 借鉴的可读性特性，使大数字一目了然。我们还声明了浮点数变量 `pi` 和 `small`。`1.5e-4` 是科学计数法，表示 `1.5 * 10^-4`，等于 `0.00015`。然后我们执行基本算术运算：加法（`+`）、乘法（`*`）和除法（`/`）。请注意，在 Auto 中（转译为 Python 后）两个整数相除会产生一个浮点数，就像 Python 3 一样。

## 字符串

字符串是_字符_的_序列_。字符串基本上就是一堆文字。

在你编写的几乎每一个 Auto 程序中都会用到字符串，所以请注意以下内容。

### 双引号

你可以使用双引号来指定字符串，如 `"Hello, World!"`。双引号是 Auto 中推荐的字符串风格。

引号内的所有空白字符，即空格和制表符，都会原样保留。

### 单引号

单引号中的字符串与双引号中的字符串工作方式完全相同。例如 `'What\'s your name?'`。

### 多行字符串

你可以使用三个双引号 `"""` 来指定多行字符串。你可以在三引号内自由使用单引号和双引号。例如：

```auto
"""This is a multi-line string. This is the first line.
This is the second line.
"What's your name?," I asked.
He said "Bond, James Bond."
"""
```

### 字符串是不可变的

这意味着一旦你创建了一个字符串，就不能再改变它。虽然这看起来像是一件坏事，但实际上并不是。我们将在后面的各种程序中看到为什么这不是一个限制。

> **C/C++ 程序员注意：**
>
> Auto 中没有单独的 `char` 数据类型。实际上并不需要它，我确信你不会想念它的。

### 字符串格式化

有时候我们可能想从其他信息中构造字符串。Auto 支持_f-string_（格式化字符串）来实现这一目的。语法使用 `$` 前缀放在变量名之前：

```auto
let name = "Swaroop"
let age = 20
print(f"$name was $age years old when he wrote this book")
```

> **Python 程序员注意：**
>
> 在 Python 中，f-string 使用 `{name}` 语法。在 Auto 中，相同的功能使用 `$name` 语法。`a2p` 转译器会自动将 `f"$name"` 转换为 `f"{name}"`。

<Listing number="4-3" file-name="strings.auto" caption="在 Auto 中使用字符串">

```auto
fn main() {
    // 单引号和双引号
    let name = "Swaroop"
    let greeting = 'Hello'

    // 多行字符串
    let story = """This is a multi-line string.
This is the second line.
"What's your name?" I asked.
He said "Bond, James Bond."
"""

    // 使用 $ 插值的 f-string
    let age = 20
    print(f"$name was $age years old when he wrote this book")
    print(f"Why is $name playing with that python?")

    // 字符串拼接
    print(name + " is " + "awesome")

    print(story)
}
```

```python
def main():
    # 单引号和双引号
    name = "Swaroop"
    greeting = "Hello"

    # 多行字符串
    story = """This is a multi-line string.
This is the second line.
"What's your name?" I asked.
He said "Bond, James Bond."
"""

    # 使用 {var} 插值的 f-string
    age = 20
    print(f"{name} was {age} years old when he wrote this book")
    print(f"Why is {name} playing with that python?")

    # 字符串拼接
    print(name + " is " + "awesome")

    print(story)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

我们使用双引号（`"Swaroop"`）和单引号（`'Hello'`）声明字符串变量。多行字符串使用三个双引号（`"""`）并保留所有格式，包括换行符和嵌入的引号。f-string 使用 `$name` 和 `$age` 将变量直接插入字符串中——当转译为 Python 时，这些会变成 `{name}` 和 `{age}`。最后，我们演示了使用 `+` 运算符进行字符串拼接。

### 转义序列

假设你想要一个包含双引号（`"`）的字符串，你该如何指定这个字符串？例如，字符串是 `"He said, "Hi.""`。你不能写成 `"He said, "Hi.""`，因为 Auto 会搞不清楚字符串从哪里开始、到哪里结束。因此，你需要指定这个双引号不表示字符串的结尾。这可以通过_转义序列_来实现。你将双引号写为 `\"`——注意反斜杠。

类似地，你需要使用转义序列 `\\` 来表示反斜杠本身。

如果你想指定一个两行的字符串怎么办？一种方法是使用前面展示的三引号字符串，或者你可以使用转义序列 `\n` 来表示新行的开始。另一个有用的转义序列是制表符：`\t`。

## 变量

仅仅使用字面常量很快就会变得无聊——我们需要某种方式来存储任何信息并对其进行操作。这就是_变量_发挥作用的地方。变量正如其名——它们的值可以变化，即你可以用变量来存储任何东西。变量只是你计算机内存中存储某些信息的部分。与字面常量不同，你需要某种方法来访问这些变量，因此你给它们起名字。

在 Auto 中，你使用 `let` 关键字来声明变量：

```auto
let i = 5
```

这会创建一个名为 `i` 的变量并赋值为 `5`。

> **Python 程序员注意：**
>
> Python 不需要 `let` 关键字——你只需写 `i = 5`。在 Auto 中，变量声明必须使用 `let`。`a2p` 转译器在生成 Python 代码时会去掉 `let` 关键字。

### 标识符命名

变量是标识符的一个例子。_标识符_是用来标识_某物_的名称。命名标识符时需要遵循一些规则：

- 标识符的第一个字符必须是字母（大写 ASCII 或小写 ASCII 或 Unicode 字符）或下划线（`_`）。
- 标识符名称的其余部分可以由字母（大写 ASCII 或小写 ASCII 或 Unicode 字符）、下划线（`_`）或数字（0-9）组成。
- 标识符名称区分大小写。例如，`myname` 和 `myName` 是_不_相同的。注意前者中的小写 `n` 和后者中的大写 `N`。
- _有效_标识符名称的例子有 `i`、`name_2_3`。_无效_标识符名称的例子有 `2things`、`this is spaced out`、`my-name` 和 `>a1b2_c3`。

<Listing number="4-4" file-name="variables.auto" caption="在 Auto 中使用变量">

```auto
fn main() {
    // 使用 let 声明变量
    let i = 5
    print(i)

    i = i + 1
    print(i)

    // 变量可以保存不同类型
    let name = "Alice"
    let score = 98.5
    let is_passing = true

    // 多行字符串变量
    let s = """This is a multi-line string.
This is the second line."""

    print(name)
    print(score)
    print(is_passing)
    print(s)
}
```

```python
def main():
    # 变量声明
    i = 5
    print(i)

    i = i + 1
    print(i)

    # 变量可以保存不同类型
    name = "Alice"
    score = 98.5
    is_passing = True

    # 多行字符串变量
    s = """This is a multi-line string.
This is the second line."""

    print(name)
    print(score)
    print(is_passing)
    print(s)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

首先，我们使用 `let` 创建变量 `i` 并赋值为 `5`。打印它，然后加 `1`，再次打印——如预期得到 `6`。请注意，当我们重新赋值 `i` 时，_不再_使用 `let`——`let` 仅用于首次声明。

然后我们声明了保存不同类型数据的变量：字符串（`"Alice"`）、浮点数（`98.5`）和布尔值（`true`）。注意 Auto 使用小写的 `true` 和 `false` 表示布尔值，`a2p` 转译器会将它们转换为 Python 的 `True` 和 `False`。

最后，我们将一个多行字符串赋值给变量 `s` 并打印它。

## 数据类型

变量可以保存称为_数据类型_的不同类型的值。基本类型包括我们已经讨论过的数字和字符串。Auto 是具有类型推断的静态类型语言——编译器通常可以根据你赋的值推断出类型。你也可以显式指定类型：

```auto
let age: int = 20
let pi: float = 3.14
let name: str = "Alice"
let is_active: bool = true
```

在后面的章节中，我们将看到如何使用 `type` 关键字创建自己的类型。

> **Python 程序员注意：**
>
> Auto 是静态类型的，不像 Python 是动态类型的。当通过 `a2p` 转译为 Python 时，类型注解会保留为 Python 类型提示（例如 `age: int = 20`）。这意味着生成的 Python 代码可以受益于 `mypy` 等类型检查工具。

## 对象

请记住，Auto 将程序中使用的任何东西都称为_对象_。这是从一般意义上来说的。我们不说"那个_什么什么_"，而是说"那个_对象_"。

> **面向对象编程用户注意：**
>
> Auto 是强面向对象的，在这个意义上，一切都是对象，包括数字、字符串和函数。

## 缩进

Auto 使用大括号 `{}` 来定义代码块，而不是缩进。这与 Python 使用缩进来定义代码块有着显著的区别。

例如，在 Auto 中：

```auto
fn main() {
    let x = 5
    if x > 3 {
        print("x is greater than 3")
    }
}
```

`{` 和 `}` 清楚地标记了每个代码块的开始和结束，无论代码如何缩进。尽管如此，你仍然应该一致地缩进你的代码以提高可读性——这只是语言不强制要求而已。

> **Python 程序员注意：**
>
> Python 使用缩进来定义代码块，没有大括号。Auto 使用 `{}` 定义代码块，类似于 JavaScript、Rust 和 C 等语言。`a2p` 转译器会自动将 Auto 的大括号代码块转换为 Python 的缩进代码块。
>
> **注意：** 即使 Auto 不要求缩进来保证正确性，也要始终正确缩进你的代码。一致的缩进（惯例是每级 4 个空格）使你的代码更易读、更易维护。

## 小结

我们在本章中涵盖了不少主题：

- **注释**使用 `//`，编译器会忽略它们
- **字面常量**是 `5`、`3.14`、`"hello"` 这样的值
- **数字**包括整数和浮点数
- **字符串**可以使用单引号或双引号，多行字符串使用 `"""`，f-string 使用 `$var` 提供方便的格式化
- **变量**使用 `let` 声明，遵循标准的命名规则
- **数据类型**包括 `int`、`float`、`str`、`bool` 等
- **一切**在 Auto 中都是对象
- **代码块**使用 `{}` 定义（不像 Python 使用缩进）

现在我们已经了解了许多细节，接下来可以进入更有趣的内容，比如运算符和表达式。请确保你已熟练掌握本章的内容。
