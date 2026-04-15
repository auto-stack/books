# 函数

在上一章中，我们使用了标准库提供的几个函数，如 `int` 和 `float`，以及 `math` 模块提供的几个函数，如 `sqrt` 和 `pow`。在本章中，你将学习如何创建自己的函数并运行它们。我们将看到一个函数如何调用另一个函数。我们还将介绍 `for` 循环，它用于重复执行计算。

## 定义新函数

**函数定义**指定了新函数的名称以及调用该函数时要执行的语句序列。下面是一个例子：

```auto
fn print_lyrics() {
    print("I'm a lumberjack, and I'm okay.")
    print("I sleep all night and I work all day.")
}
```

`fn` 是一个关键字，表示这是一个函数定义。函数的名称是 `print_lyrics`。任何合法的变量名也是合法的函数名。

名称后面的空括号表示这个函数不接受任何参数。

函数定义的第一行称为**函数头**（header）——其余部分称为**函数体**（body）。函数头以冒号结束，函数体用大括号 `{}` 包围。这个函数的函数体包含两个 print 语句；一般来说，函数体可以包含任意数量的任意类型的语句。

定义函数会创建一个**函数对象**。既然我们已经定义了一个函数，就可以像调用内置函数一样调用它：

```auto
print_lyrics()
```

当函数运行时，它执行函数体中的语句，显示"伐木工之歌"的前两行。

> **Python 程序员注意：**
>
> Auto 使用 `fn` 代替 Python 的 `def`，函数体用 `{}` 包围而不是缩进。`a2p` 转译器会将 `fn` 转换为 `def` 并生成正确缩进的 Python 代码。

<Listing number="3-1" file-name="define_call.auto" caption="定义和调用函数">

```auto
fn print_lyrics() {
    print("I'm a lumberjack, and I'm okay.")
    print("I sleep all night and I work all day.")
}

fn main() {
    // 调用函数
    print_lyrics()
    print()
    print_lyrics()
}
```

```python
def print_lyrics():
    print("I'm a lumberjack, and I'm okay.")
    print("I sleep all night and I work all day.")


def main():
    # 调用函数
    print_lyrics()
    print()
    print_lyrics()


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

我们使用 `fn` 关键字后跟函数名和括号来定义 `print_lyrics`。用 `{}` 包围的函数体包含两个 `print` 语句。在 `main()` 中，我们调用了两次 `print_lyrics()`，中间有一个空行。每次调用都会从上到下执行函数体。

## 参数

我们见过的一些函数需要参数；例如，调用 `abs` 时需要传递一个数字。有些函数接受多个参数；例如，`math.pow` 接受两个参数：底数和指数。

下面是一个接受参数的函数定义：

```auto
fn print_twice(string: str) {
    print(string)
    print(string)
}
```

括号中的变量名是一个**参数**（parameter）。当函数被调用时，参数的值被赋给参数名。例如，我们可以这样调用 `print_twice`：

```auto
print_twice("Dennis Moore, ")
```

你也可以使用变量作为参数：

```auto
let line = "Dennis Moore, "
print_twice(line)
```

在这个例子中，`line` 的值被赋给了参数 `string`。

> **Python 程序员注意：**
>
> Auto 使用 `string: str` 来声明带类型的参数。`a2p` 转译器会去掉类型注解，在 Python 输出中生成 `string`。如果你愿意，也可以在 Auto 中省略类型注解。

<Listing number="3-2" file-name="parameters.auto" caption="带参数的函数">

```auto
fn print_twice(string: str) {
    print(string)
    print(string)
}

fn repeat(word: str, n: int) {
    let result = word * n
    print(result)
}

fn main() {
    // 用字面量参数调用
    print_twice("Dennis Moore, ")

    // 用变量参数调用
    let line = "Dennis Moore, "
    print_twice(line)

    // 调用有两个参数的函数
    let spam = "Spam, "
    repeat(spam, 4)
}
```

```python
def print_twice(string):
    print(string)
    print(string)


def repeat(word, n):
    result = word * n
    print(result)


def main():
    # 用字面量参数调用
    print_twice("Dennis Moore, ")

    # 用变量参数调用
    line = "Dennis Moore, "
    print_twice(line)

    # 调用有两个参数的函数
    spam = "Spam, "
    repeat(spam, 4)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`print_twice` 接受一个参数 `string`，并将其打印两次。`repeat` 接受两个参数 `word` 和 `n`，使用字符串的 `*` 运算符将单词重复 `n` 次后打印。

在 `main()` 中，我们分别用字面量字符串和变量调用 `print_twice`。我们还用一个字符串变量和一个整数调用 `repeat`。注意函数内部的参数名（`string`、`word`、`n`）与调用者的变量名（`line`、`spam`）是分开的。

## 调用函数

一旦定义了一个函数，就可以在另一个函数中使用它。为了演示，我们将编写打印"Spam Song"歌词的函数：

> Spam, Spam, Spam, Spam,
> Spam, Spam, Spam, Spam,
> Spam, Spam,
> (Lovely Spam, Wonderful Spam!)
> Spam, Spam,

我们从上一节的 `repeat` 函数开始。然后可以定义基于它构建的更高层函数：

```auto
fn first_two_lines() {
    repeat("Spam, ", 4)
    repeat("Spam, ", 4)
}

fn last_three_lines() {
    repeat("Spam, ", 2)
    print("(Lovely Spam, Wonderful Spam!)")
    repeat("Spam, ", 2)
}

fn print_verse() {
    first_two_lines()
    last_three_lines()
}
```

当我们运行 `print_verse` 时，它调用 `first_two_lines`，后者又调用 `repeat`，后者又调用 `print`。这是很多层函数调用。当然，我们可以用更少的函数完成同样的功能，但这个例子的目的是展示函数如何协同工作。

## 重复

如果我们想显示多段歌词，可以使用 `for` 语句。下面是一个简单的例子：

```auto
for i in 0..2 {
    print(i)
}
```

`for` 语句的头部以关键字 `for` 开始，后跟一个新的变量名 `i`、关键字 `in`，以及一个**范围表达式** `0..2`，它产生值 `0` 和 `1`。在 Auto 中，和许多编程语言一样，计数从 `0` 开始。

当 `for` 语句运行时，它将范围中的第一个值赋给 `i`，然后运行函数体，显示 `0`。当到达函数体末尾时，它循环回到头部——因此这个语句被称为**循环**（loop）。第二次循环时，它将下一个值赋给 `i` 并显示它。然后，因为那是范围中的最后一个值，循环结束。

下面是我们如何使用 `for` 循环打印歌曲的两段歌词：

```auto
for i in 0..2 {
    print("Verse", i)
    print_verse()
    print()
}
```

你可以将 `for` 循环放在函数内部。例如，`print_n_verses` 接受一个名为 `n` 的参数，并显示指定数量的歌词段落：

```auto
fn print_n_verses(n: int) {
    for i in 0..n {
        print_verse()
        print()
    }
}
```

在这个例子中，我们没有在循环体中使用 `i`，但头部仍然需要一个变量名。

> **Python 程序员注意：**
>
> Auto 使用 `0..n` 表示范围，而不是 Python 的 `range(n)`。`a2p` 转译器会自动将 `0..n` 转换为 `range(n)`。Auto 没有 `while` 语句；请使用 `for` 配合范围或条件中断来代替。

<Listing number="3-3" file-name="repetition.auto" caption="使用 for 循环进行重复">

```auto
fn repeat(word: str, n: int) {
    print(word * n)
}

fn first_two_lines() {
    repeat("Spam, ", 4)
    repeat("Spam, ", 4)
}

fn last_three_lines() {
    repeat("Spam, ", 2)
    print("(Lovely Spam, Wonderful Spam!)")
    repeat("Spam, ", 2)
}

fn print_verse() {
    first_two_lines()
    last_three_lines()
}

fn main() {
    // 简单的 for 循环
    print("Counting:")
    for i in 0..3 {
        print(i)
    }

    // 使用 for 循环重复歌词段落
    print("Two verses:")
    for i in 0..2 {
        print("Verse", i)
        print_verse()
    }
}
```

```python
def repeat(word, n):
    print(word * n)


def first_two_lines():
    repeat("Spam, ", 4)
    repeat("Spam, ", 4)


def last_three_lines():
    repeat("Spam, ", 2)
    print("(Lovely Spam, Wonderful Spam!)")
    repeat("Spam, ", 2)


def print_verse():
    first_two_lines()
    last_three_lines()


def main():
    # 简单的 for 循环
    print("Counting:")
    for i in range(3):
        print(i)

    # 使用 for 循环重复歌词段落
    print("Two verses:")
    for i in range(2):
        print("Verse", i)
        print_verse()


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

首先，一个简单的 `for` 循环使用 `0..3` 从 `0` 计数到 `2`。范围表达式 `0..3` 产生值 `0`、`1` 和 `2`——上界是排他的，就像 Python 的 `range(3)` 一样。

然后，第二个 `for` 循环使用 `0..2` 打印 Spam Song 的两段歌词。每次迭代调用 `print_verse()`，后者又调用 `first_two_lines()` 和 `last_three_lines()`，展示了函数如何组合起来，从更简单的部分构建更复杂的行为。

## 变量和参数是局部的

当你在函数内部创建一个变量时，它是**局部的**（local），这意味着它只存在于函数内部。例如，以下函数接受两个参数，将它们连接起来，并打印两次结果：

```auto
fn cat_twice(part1: str, part2: str) {
    let cat = part1 + part2
    print_twice(cat)
}
```

下面是一个使用它的例子：

```auto
let line1 = "Always look on the "
let line2 = "bright side of life."
cat_twice(line1, line2)
```

当 `cat_twice` 运行时，它创建一个名为 `cat` 的局部变量，该变量在函数结束时被销毁。如果我们尝试在函数外部显示它，会得到一个错误——`cat` 在那里未定义。

参数也是局部的。例如，在 `cat_twice` 外部，不存在 `part1` 或 `part2`。

<Listing number="3-4" file-name="local_scope.auto" caption="局部变量与作用域">

```auto
fn print_twice(string: str) {
    print(string)
    print(string)
}

fn cat_twice(part1: str, part2: str) {
    // cat 是局部变量
    let cat = part1 + part2
    print_twice(cat)
    // cat 在此函数结束时被销毁
}

fn main() {
    let line1 = "Always look on the "
    let line2 = "bright side of life."
    cat_twice(line1, line2)

    // 这会出错——cat 是 cat_twice 的局部变量：
    // print(cat)

    // 这些也会出错——参数也是局部的：
    // print(part1)
    // print(part2)
}
```

```python
def print_twice(string):
    print(string)
    print(string)


def cat_twice(part1, part2):
    # cat 是局部变量
    cat = part1 + part2
    print_twice(cat)
    # cat 在此函数结束时被销毁


def main():
    line1 = "Always look on the "
    line2 = "bright side of life."
    cat_twice(line1, line2)

    # 这会出错——cat 是 cat_twice 的局部变量：
    # print(cat)

    # 这些也会出错——参数也是局部的：
    # print(part1)
    # print(part2)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`cat_twice` 接收两个参数 `part1` 和 `part2`，它们是该函数的局部变量。它通过连接两个参数创建了另一个局部变量 `cat`。当 `cat_twice` 执行完毕后，它的所有局部变量（`cat`、`part1`、`part2`）都被销毁。

在 `main()` 中，我们用 `line1` 和 `line2` 调用 `cat_twice`。调用返回后，我们无法从 `main()` 访问 `cat`、`part1` 或 `part2`——它们只存在于 `cat_twice` 内部。被注释掉的行展示了如果我们尝试访问会发生什么：在 Python 中会得到 `NameError`。

## 栈图

为了追踪哪些变量可以在哪里使用，有时画一个**栈图**（stack diagram）是很有用的。和状态图一样，栈图显示每个变量的值，但它还显示每个变量属于哪个函数。

每个函数由一个**帧**（frame）表示。帧是一个方框，外面是函数名，里面是函数的参数和局部变量。

以下是 `cat_twice` 示例在运行并调用 `print_twice` 时栈图的文本表示：

```
+------------------+
| __main__         |
| line1  -> "..."  |
| line2  -> "..."  |
+------------------+
| cat_twice        |
| part1  -> "..."  |
| part2  -> "..."  |
| cat    -> "..."  |
+------------------+
| print_twice      |
| string -> "..."  |
+------------------+
```

帧按栈的方式排列，指示哪个函数调用了哪个函数。从底部向上读，`print_twice` 被 `cat_twice` 调用，而 `cat_twice` 被 `__main__` 调用——`__main__` 是最顶层帧的特殊名称。当你在任何函数之外创建变量时，它属于 `__main__`。

## 回溯

当函数中发生运行时错误时，程序会显示正在运行的函数名、调用它的函数名，依此类推，沿栈向上。这个函数列表被称为**回溯**（traceback）。

例如，如果 `print_twice` 尝试访问另一个函数的局部变量，你会得到一个错误。回溯显示 `cat_twice` 调用了 `print_twice`，错误发生在 `print_twice` 中。

回溯中函数的顺序与栈图中帧的顺序相同。发生错误时正在运行的函数位于最底部。

## 为什么使用函数？

将程序划分为函数的好处可能还不太明显。有以下几个原因：

- **可读性**：创建一个新函数让你有机会为一组语句命名，使程序更容易阅读和调试。

- **消除重复**：函数可以通过消除重复代码来减小程序的体积。以后如果需要修改，只需要在一个地方修改即可。

- **调试**：将长程序划分为函数可以让你逐个部分进行调试，然后将它们组装成一个完整的工作程序。

- **可重用性**：设计良好的函数通常对许多程序都有用。一旦你编写并调试好一个函数，就可以重复使用它。

## 调试

调试可能令人沮丧，但它也充满挑战、有趣，有时甚至很有成就感。它也是你能学到的最重要的技能之一。

在某些方面，调试就像侦探工作。你得到一些线索，必须推断出导致你所见结果的事件。

调试也像实验科学。一旦你对出了什么问题有了想法，就修改程序并重试。如果你的假设是正确的，你可以预测修改的结果，并向一个可工作的程序迈进一步。如果你的假设是错误的，你必须想出一个新的假设。

对某些人来说，编程和调试是一回事——也就是说，编程是逐步调试程序直到它满足你需求的过程。其理念是，你应该从一个可工作的程序开始，进行小步修改，并在过程中不断调试。

如果你发现自己花了很多时间调试，这通常意味着你在开始测试之前写了太多代码。如果采取更小的步骤，你可能会发现自己能进展得更快。

## 术语表

**函数定义 (function definition):**
使用 `fn` 关键字创建函数的语句。

**函数头 (header):**
函数定义的第一行，从 `fn` 到开头的 `{`。

**函数体 (body):**
函数定义内部的语句序列，用 `{}` 包围。

**函数对象 (function object):**
由函数定义创建的值。函数名是一个指向函数对象的变量。

**参数 (parameter):**
函数内部使用的名称，用于引用作为参数传递的值。

**循环 (loop):**
重复执行一个或多个语句的语句。

**局部变量 (local variable):**
在函数内部定义的变量，只能在函数内部访问。

**栈图 (stack diagram):**
函数栈、其变量及其指向值的图形表示。

**帧 (frame):**
栈图中代表函数调用的方框。它包含函数的局部变量和参数。

**回溯 (traceback):**
发生异常时打印的正在执行的函数列表。

## 练习

### 练习

编写一个名为 `print_right` 的函数，接受一个名为 `text` 的字符串参数，并打印该字符串，使字符串的最后一个字母位于显示的第 40 列。

提示：使用 `len` 函数、字符串连接运算符（`+`）和字符串重复运算符（`*`）。

### 练习

编写一个名为 `triangle` 的函数，接受一个字符串和一个整数，绘制一个使用该字符串副本组成的给定高度的三角形。以下是使用字符串 `'L'` 的 `5` 层三角形示例：

```
    L
   LLL
  LLLLL
 LLLLLLL
LLLLLLLLL
```

### 练习

编写一个名为 `rectangle` 的函数，接受一个字符串和两个整数，绘制一个使用该字符串副本组成的给定宽度和高度的矩形。例如，`rectangle("H", 5, 4)` 应该产生：

```
HHHHH
HHHHH
HHHHH
HHHHH
```

### 练习

歌曲"99 Bottles of Beer"以这段歌词开始：

> 99 bottles of beer on the wall
> 99 bottles of beer
> Take one down, pass it around
> 98 bottles of beer on the wall

第二段歌词是一样的，只是从 98 瓶开始，以 97 瓶结束。歌曲一直继续，直到 0 瓶啤酒。

编写一个名为 `bottle_verse` 的函数，接受一个数字作为参数，显示以给定瓶数开始的那段歌词。

提示：考虑先编写一个可以打印歌词第一行、第二行或最后一行的函数，然后用它来编写 `bottle_verse`。
