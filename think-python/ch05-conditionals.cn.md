# 条件与递归

本章的主要主题是 `if` 语句，它根据程序的状态执行不同的代码。通过 `if` 语句，我们将能够探索计算中最强大的思想之一——**递归**（recursion）。

但我们将从三个新特性开始：取模运算符、布尔表达式和逻辑运算符。

## 整数除法和取模

回想一下，整数除法运算符 `/` 将两个数相除并向下取整。例如，假设一部电影的播放时间是 105 分钟。你可能想知道这是几小时。整数除法返回整数小时数：

```auto
let minutes = 105
let hours = minutes / 60
print(hours)   // 输出: 1
```

要得到余数，你可以减去一小时的分钟数。或者你可以使用**取模运算符**（modulus operator）`%`，它将两个数相除并返回余数：

```auto
let remainder = minutes % 60
print(remainder)   // 输出: 45
```

<Listing number="5-1" file-name="modulus.auto" caption="取模运算符：整数除法和余数">

```auto
fn main() {
    // 整数除法和取模
    let minutes = 105
    let hours = minutes / 60
    print("Minutes: $minutes")
    print("Hours: $hours")
    print()

    // 通过减法得到余数
    let remainder = minutes - hours * 60
    print("Remainder (subtraction): $remainder")

    // 通过取模运算符得到余数
    let remainder2 = minutes % 60
    print("Remainder (modulus): $remainder2")
    print()

    // 提取最右边的数字
    let x = 123
    print("x = $x")
    print("x % 10 = ${x % 10}")
    print("x % 100 = ${x % 100}")
    print()

    // 时钟算术
    let start = 11
    let duration = 3
    let end = (start + duration) % 12
    print("Start: ${start} AM")
    print("Duration: $duration hours")
    print("End: ${if end == 0 { 12 } else { end }} PM")

    // 整除检查
    let y = 15
    print()
    print("Is $y divisible by 3? ${y % 3 == 0}")
    print("Is $y divisible by 4? ${y % 4 == 0}")
}
```

```python
def main():
    # 整数除法和取模
    minutes = 105
    hours = minutes // 60
    print(f"Minutes: {minutes}")
    print(f"Hours: {hours}")
    print()

    # 通过减法得到余数
    remainder = minutes - hours * 60
    print(f"Remainder (subtraction): {remainder}")

    # 通过取模运算符得到余数
    remainder2 = minutes % 60
    print(f"Remainder (modulus): {remainder2}")
    print()

    # 提取最右边的数字
    x = 123
    print(f"x = {x}")
    print(f"x % 10 = {x % 10}")
    print(f"x % 100 = {x % 100}")
    print()

    # 时钟算术
    start = 11
    duration = 3
    end = (start + duration) % 12
    print(f"Start: {start} AM")
    print(f"Duration: {duration} hours")
    print(f"End: {12 if end == 0 else end} PM")

    # 整除检查
    y = 15
    print()
    print(f"Is {y} divisible by 3? {y % 3 == 0}")
    print(f"Is {y} divisible by 4? {y % 4 == 0}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

我们用 `/`（Auto 中的整数除法）将 `105` 分钟除以 `60`，得到 `1` 小时。取模运算符 `%` 给出余数 `45`。我们还演示了提取最右边的数字（`123 % 10` 是 `3`，`123 % 100` 是 `23`）、时钟算术（上午 11 点 + 3 小时循环到下午 2 点）以及整除检查（15 能被 3 整除但不能被 4 整除）。

> **Python 程序员注意：**
>
> Auto 使用 `/` 进行整数除法（当两个操作数都是整数时）。`a2p` 转译器会自动将其转换为 Python 的 `//` 运算符。Auto 的 `%` 运算符与 Python 的用法相同。

## 布尔表达式

**布尔表达式**（boolean expression）是一个值为真或假的表达式。例如，以下表达式使用等于运算符 `==`，它比较两个值，如果相等则产生 `true`，否则产生 `false`：

```auto
5 == 5    // true
5 == 7    // false
```

`true` 和 `false` 是属于 `bool` 类型的特殊值；它们不是字符串。

一个常见的错误是使用单个等号（`=`）而不是双等号（`==`）。记住 `=` 给变量赋值，而 `==` 比较两个值。

`==` 运算符是**关系运算符**（relational operator）之一；其他的关系运算符有：

| 运算符 | 含义 |
|--------|------|
| `!=` | 不等于 |
| `>` | 大于 |
| `<` | 小于 |
| `>=` | 大于或等于 |
| `<=` | 小于或等于 |

> **Python 程序员注意：**
>
> Auto 使用 `true` 和 `false`（小写）。`a2p` 转译器会自动将它们转换为 Python 的 `True` 和 `False`。

## 逻辑运算符

要将布尔值组合成表达式，我们可以使用**逻辑运算符**（logical operator）。在 Auto 中，它们是 `&&`（与）、`||`（或）和 `!`（非）。

<Listing number="5-2" file-name="boolean_logical.auto" caption="布尔运算符和逻辑运算符">

```auto
fn main() {
    // 布尔表达式
    let x = 5
    let y = 7

    print("x = $x, y = $y")
    print("x == y: ${x == y}")
    print("x != y: ${x != y}")
    print("x > y: ${x > y}")
    print("x < y: ${x < y}")
    print("x >= y: ${x >= y}")
    print("x <= y: ${x <= y}")
    print()

    // 逻辑运算符
    print("x > 0 && x < 10: ${x > 0 && x < 10}")
    print("x % 2 == 0 || x % 3 == 0: ${x % 2 == 0 || x % 3 == 0}")
    print("!(x > y): ${!(x > y)}")
    print()

    // 组合条件
    let age = 25
    let has_ticket = true
    print("age = $age, has_ticket = $has_ticket")
    print("Can enter: ${age >= 18 && has_ticket}")

    // 取反
    let is_raining = false
    print("is_raining = $is_raining")
    print("Should go outside: ${!is_raining}")
}
```

```python
def main():
    # 布尔表达式
    x = 5
    y = 7

    print(f"x = {x}, y = {y}")
    print(f"x == y: {x == y}")
    print(f"x != y: {x != y}")
    print(f"x > y: {x > y}")
    print(f"x < y: {x < y}")
    print(f"x >= y: {x >= y}")
    print(f"x <= y: {x <= y}")
    print()

    # 逻辑运算符
    print(f"x > 0 and x < 10: {x > 0 and x < 10}")
    print(f"x % 2 == 0 or x % 3 == 0: {x % 2 == 0 or x % 3 == 0}")
    print(f"not (x > y): {not (x > y)}")
    print()

    # 组合条件
    age = 25
    has_ticket = True
    print(f"age = {age}, has_ticket = {has_ticket}")
    print(f"Can enter: {age >= 18 and has_ticket}")

    # 取反
    is_raining = False
    print(f"is_raining = {is_raining}")
    print(f"Should go outside: {not is_raining}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

我们对 `x` 和 `y` 测试了所有六个关系运算符。然后我们用逻辑运算符组合条件：`&&` 要求两个条件都为真，`||` 要求至少一个为真，`!` 取反一个布尔值。最后几个例子展示了实际应用：检查入场资格（年龄 >= 18 且有票）以及是否应该出门（不下雨）。

> **Python 程序员注意：**
>
> Auto 使用 `&&` 代替 Python 的 `and`，`||` 代替 `or`，`!` 代替 `not`。`a2p` 转译器会自动进行转换。

## if 语句

为了编写有用的程序，我们几乎总是需要检查条件并相应地改变程序的行为。**条件语句**（conditional statement）给了我们这种能力。最简单的形式是 `if` 语句：

```auto
if x > 0 {
    print("x is positive")
}
```

`if` 后面的布尔表达式称为**条件**（condition）。如果它为真，则执行块中的语句。如果不是，则不执行。

## 链式条件

有时有超过两种可能性，我们需要超过两个分支。表达这种计算的一种方式是**链式条件**（chained conditional），它使用 `else if`：

```auto
if x < y {
    print("x is less than y")
} else if x > y {
    print("x is greater than y")
} else {
    print("x and y are equal")
}
```

`else if` 子句的数量没有限制。如果有 `else` 子句，它必须在最后，但也可以没有。每个条件按顺序检查。如果第一个为假，则检查下一个，以此类推。如果其中有一个为真，则运行相应的分支，`if` 语句结束。即使有多个条件为真，也只有第一个为真的分支会运行。

> **Python 程序员注意：**
>
> Auto 使用 `else if` 代替 Python 的 `elif`。`a2p` 转译器会自动将 `else if` 转换为 `elif`。

## 嵌套条件

一个条件也可以嵌套在另一个条件中。我们可以这样写比较的例子：

```auto
if x == y {
    print("x and y are equal")
} else {
    if x < y {
        print("x is less than y")
    } else {
        print("x is greater than y")
    }
}
```

外层 `if` 语句包含两个分支。第一个分支包含一个简单语句。第二个分支包含另一个 `if` 语句。虽然缩进使结构很明显，但**嵌套条件**（nested conditional）可能难以阅读。一般来说，你应该尽可能避免使用它们。

逻辑运算符通常提供一种简化嵌套条件语句的方法。例如，这个嵌套条件：

```auto
if 0 < x {
    if x < 10 {
        print("x is a positive single-digit number.")
    }
}
```

可以简化为：

```auto
if 0 < x && x < 10 {
    print("x is a positive single-digit number.")
}
```

## if / else if / else

<Listing number="5-3" file-name="conditionals.auto" caption="if / else if / else 语句">

```auto
fn classify_number(x: int) {
    if x > 0 {
        print("$x is positive")
    } else if x < 0 {
        print("$x is negative")
    } else {
        print("$x is zero")
    }
}

fn classify_even_odd(x: int) {
    if x % 2 == 0 {
        print("$x is even")
    } else {
        print("$x is odd")
    }
}

fn classify_temperature(temp: int) {
    if temp >= 30 {
        print("$temp C is hot")
    } else if temp >= 20 {
        print("$temp C is warm")
    } else if temp >= 10 {
        print("$temp C is cool")
    } else {
        print("$temp C is cold")
    }
}

fn compare(x: int, y: int) {
    if x < y {
        print("$x is less than $y")
    } else if x > y {
        print("$x is greater than $y")
    } else {
        print("$x and $y are equal")
    }
}

fn main() {
    // if / else
    print("=== Positive / Negative / Zero ===")
    classify_number(5)
    classify_number(-3)
    classify_number(0)
    print()

    // if / else (奇偶)
    print("=== Even / Odd ===")
    classify_even_odd(4)
    classify_even_odd(7)
    print()

    // 链式条件 (else if)
    print("=== Temperature ===")
    classify_temperature(35)
    classify_temperature(25)
    classify_temperature(15)
    classify_temperature(5)
    print()

    // 链式条件 (三路比较)
    print("=== Comparison ===")
    compare(3, 5)
    compare(7, 2)
    compare(4, 4)
}
```

```python
def classify_number(x):
    if x > 0:
        print(f"{x} is positive")
    elif x < 0:
        print(f"{x} is negative")
    else:
        print(f"{x} is zero")


def classify_even_odd(x):
    if x % 2 == 0:
        print(f"{x} is even")
    else:
        print(f"{x} is odd")


def classify_temperature(temp):
    if temp >= 30:
        print(f"{temp} C is hot")
    elif temp >= 20:
        print(f"{temp} C is warm")
    elif temp >= 10:
        print(f"{temp} C is cool")
    else:
        print(f"{temp} C is cold")


def compare(x, y):
    if x < y:
        print(f"{x} is less than {y}")
    elif x > y:
        print(f"{x} is greater than {y}")
    else:
        print(f"{x} and {y} are equal")


def main():
    # if / else
    print("=== Positive / Negative / Zero ===")
    classify_number(5)
    classify_number(-3)
    classify_number(0)
    print()

    # if / else (奇偶)
    print("=== Even / Odd ===")
    classify_even_odd(4)
    classify_even_odd(7)
    print()

    # 链式条件 (elif)
    print("=== Temperature ===")
    classify_temperature(35)
    classify_temperature(25)
    classify_temperature(15)
    classify_temperature(5)
    print()

    # 链式条件 (三路比较)
    print("=== Comparison ===")
    compare(3, 5)
    compare(7, 2)
    compare(4, 4)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`classify_number` 使用三路 `if`/`else if`/`else` 将数字分类为正数、负数或零。`classify_even_odd` 使用取模运算符检查数字是偶数还是奇数。`classify_temperature` 演示了一个更长的 `else if` 链，有四个分支，检查从热到冷的温度范围。`compare` 使用链式条件比较两个数字。

注意 `classify_temperature` 的工作方式：条件按顺序检查，所以先检查 `temp >= 30`。如果 `temp` 是 `25`，第一个条件为假，所以检查下一个（`temp >= 20`）并发现为真——剩余的分支被跳过。

## 递归

函数调用自身是合法的。这为什么是好事可能不太明显，但它结果是程序能做的最神奇的事情之一。下面是一个例子：

<Listing number="5-4" file-name="recursion.auto" caption="简单递归：倒计时">

```auto
fn countdown(n: int) {
    if n <= 0 {
        print("Blastoff!")
    } else {
        print(n)
        countdown(n - 1)
    }
}

fn print_n(string: str, n: int) {
    if n > 0 {
        print(string)
        print_n(string, n - 1)
    }
}

fn main() {
    // 从 3 开始倒计时
    print("Countdown from 3:")
    countdown(3)
    print()

    // 从 1 开始倒计时
    print("Countdown from 1:")
    countdown(1)
    print()

    // 将字符串打印 n 次
    print("Print 'Spam' 4 times:")
    print_n("Spam", 4)
    print()

    // n = 0（基本情况，不打印）
    print("Print 'Hello' 0 times:")
    print_n("Hello", 0)
}
```

```python
def countdown(n):
    if n <= 0:
        print("Blastoff!")
    else:
        print(n)
        countdown(n - 1)


def print_n(string, n):
    if n > 0:
        print(string)
        print_n(string, n - 1)


def main():
    # 从 3 开始倒计时
    print("Countdown from 3:")
    countdown(3)
    print()

    # 从 1 开始倒计时
    print("Countdown from 1:")
    countdown(1)
    print()

    # 将字符串打印 n 次
    print("Print 'Spam' 4 times:")
    print_n("Spam", 4)
    print()

    # n = 0（基本情况，不打印）
    print("Print 'Hello' 0 times:")
    print_n("Hello", 0)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`countdown` 检查 `n` 是否小于或等于 `0`。如果是，它打印 "Blastoff!"——这称为**基本情况**（base case）。否则，它打印 `n` 然后用 `n - 1` 调用自身。

当我们调用 `countdown(3)` 时，执行从 `n=3` 开始。因为 `n > 0`，它显示 `3` 并调用 `countdown(2)`：

> `countdown` 的执行从 `n=2` 开始。因为 `n > 0`，它显示 `2` 并调用 `countdown(1)`：
>
> > `countdown` 的执行从 `n=1` 开始。因为 `n > 0`，它显示 `1` 并调用 `countdown(0)`：
> >
> > > `countdown` 的执行从 `n=0` 开始。因为 `n <= 0`，它显示 "Blastoff!" 并返回。
> >
> > 得到 `n=1` 的 `countdown` 返回。
>
> 得到 `n=2` 的 `countdown` 返回。

得到 `n=3` 的 `countdown` 返回。

`print_n` 的工作方式类似：如果 `n > 0`，它打印字符串并用 `n - 1` 调用自身。如果 `n` 是 `0`，条件为假，函数什么也不做——这就是基本情况。

调用自身的函数是**递归的**（recursive）。对于像这样的简单例子，使用 `for` 循环可能更容易。但我们稍后会看到一些用 `for` 循环很难写但用递归很容易写的例子，所以早点开始学习是好的。

## 无限递归

如果递归永远不达到基本情况，它就会一直进行递归调用，程序永远不会终止。这被称为**无限递归**（infinite recursion），通常不是一个好主意。下面是一个最小的无限递归函数：

```auto
fn recurse() {
    recurse()
}
```

每次调用 `recurse` 时，它调用自身，创建另一个帧。同时存在于栈上的帧数是有限制的。如果程序超过这个限制，就会导致运行时错误。

如果你不小心遇到了无限递归，检查你的函数，确认是否存在一个不进行递归调用的基本情况。如果有基本情况，检查是否保证能达到它。

## 键盘输入

到目前为止我们编写的程序不接受用户输入。它们每次都做同样的事情。

Auto 提供了一个名为 `input` 的内置函数，它会暂停程序并等待用户输入。当用户按下回车键时，程序恢复执行，`input` 返回用户输入的内容作为字符串。

```auto
let text = input()
print("You typed: $text")
```

在获取用户输入之前，你可能想显示一个提示，告诉用户该输入什么。`input` 可以接受一个提示作为参数：

```auto
let name = input("What is your name?\n")
print("Hello, $name!")
```

如果你期望用户输入一个整数，可以使用 `int` 函数来转换返回值：

```auto
let speed = int(input("Enter speed: "))
print("Speed is $speed")
```

但如果用户输入的不是整数，你会得到一个运行时错误。我们稍后会看到如何处理这种错误。

## 递归函数的栈图

以下是调用 `countdown` 且 `n = 3` 时创建的帧的栈图：

```
+------------------+
| countdown        |
| n -> 3           |
+------------------+
| countdown        |
| n -> 2           |
+------------------+
| countdown        |
| n -> 1           |
+------------------+
| countdown        |
| n -> 0           |
+------------------+
```

四个 `countdown` 帧对参数 `n` 有不同的值。栈的底部，`n=0` 的位置，称为**基本情况**。它不进行递归调用，所以下面没有更多的帧。

## 调试

当发生语法或运行时错误时，错误消息包含大量信息，但可能令人不知所措。最有用的部分通常是：

- 错误是什么类型，以及
- 错误发生在哪里。

语法错误通常很容易找到，但有一些陷阱。与空格和制表符相关的错误可能很棘手，因为它们是不可见的，而且我们习惯于忽略它们。

错误消息指示了发现问题的地方，但实际错误可能在代码的更前面。运行时错误也是如此。

一般来说，你应该花时间仔细阅读错误消息，但不要假设它们说的每件事都是正确的。

## 术语表

**递归 (recursion):**
调用当前正在执行的函数的过程。

**取模运算符 (modulus operator):**
运算符 `%`，用于整数，返回一个数除以另一个数的余数。

**布尔表达式 (boolean expression):**
值为 `true` 或 `false` 的表达式。

**关系运算符 (relational operator):**
比较其操作数的运算符之一：`==`、`!=`、`>`、`<`、`>=` 和 `<=`。

**逻辑运算符 (logical operator):**
组合布尔表达式的运算符之一，包括 `&&`（与）、`||`（或）和 `!`（非）。

**条件语句 (conditional statement):**
根据某些条件控制执行流的语句。

**条件 (condition):**
条件语句中确定哪个分支运行的布尔表达式。

**块 (block):**
用 `{}` 包围的一个或多个语句，表示它们是另一个语句的一部分。

**分支 (branch):**
条件语句中备选的语句序列之一。

**链式条件 (chained conditional):**
使用 `else if` 的一系列备选分支的条件语句。

**嵌套条件 (nested conditional):**
出现在另一个条件语句的某个分支中的条件语句。

**递归的 (recursive):**
调用自身的函数是递归的。

**基本情况 (base case):**
递归函数中不进行递归调用的条件分支。

**无限递归 (infinite recursion):**
没有基本情况或永远达不到基本情况的递归。最终，无限递归会导致运行时错误。

**换行符 (newline):**
在字符串的两部分之间创建换行的字符。

## 练习

### 练习

使用整数除法和取模运算符编写一个函数，接受秒数并打印小时、分钟和秒。例如，`print_time(3661)` 应该显示 `1 hour, 1 minute, 1 second`。

### 练习

如果你有三根木棍，你可能能够也可能无法将它们排列成三角形。对于任意三个长度，有一个测试可以判断是否能形成三角形：

> 如果三个长度中有一个大于其他两个之和，那么你不能形成三角形。否则，可以。

编写一个名为 `is_triangle` 的函数，接受三个整数作为参数，根据给定的长度是否能组成三角形来打印 "Yes" 或 "No"。提示：使用链式条件。

用以下情况测试你的函数：

```auto
is_triangle(4, 5, 6)    // 应该是 Yes
is_triangle(1, 2, 3)    // 应该是 Yes（退化的）
is_triangle(6, 2, 3)    // 应该是 No
is_triangle(1, 1, 12)   // 应该是 No
```

### 练习

以下程序的输出是什么？画一个栈图，显示程序打印结果时的状态。

```auto
fn recurse(n: int, s: int) {
    if n == 0 {
        print(s)
    } else {
        recurse(n - 1, n + s)
    }
}

fn main() {
    recurse(3, 0)
}
```

### 练习

编写一个名为 `fibonacci` 的递归函数，接受一个整数 `n` 并返回第 n 个斐波那契数。斐波那契数列定义为：`fib(0) = 0`，`fib(1) = 1`，对于 `n > 1`，`fib(n) = fib(n-1) + fib(n-2)`。打印前 10 个斐波那契数。

提示：你需要一个返回值的函数，我们将在下一章介绍。目前，你可以使用 `print` 来显示每个值。
