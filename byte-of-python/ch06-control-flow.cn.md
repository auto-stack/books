# 控制流

在我们目前见过的程序中，语句总是严格按照从上到下的顺序执行的。如果你想改变程序的执行流程怎么办？例如，你希望程序根据不同的情况做出不同的决定并执行不同的操作，比如根据一天中的时间打印"早上好"或"晚上好"？

你可能已经猜到了，这是通过控制流语句来实现的。Auto 中有三种控制流语句——`if`、`for`（同时充当 `for` 循环和 `while` 循环），以及相关的 `break` 和 `continue` 语句。

## `if` 语句

`if` 语句用于检查条件：_如果_条件为真，我们运行一个语句块（称为 _if 块_），_否则_我们处理另一个语句块（称为 _else 块_）。`else` 子句是可选的。你可以使用 `else if` 链接多个条件。

让我们看一个简单的例子：

<Listing number="6-1" file-name="if.auto" caption="使用 if 语句">

```auto
fn main() {
    let number = 23

    if number < 0 {
        print("Negative")
    } else if number == 0 {
        print("Zero")
    } else {
        print("Positive")
    }
}
```

```python
def main():
    number = 23

    if number < 0:
        print("Negative")
    elif number == 0:
        print("Zero")
    else:
        print("Positive")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

在这个程序中，我们声明了一个变量 `number` 并赋值为 `23`。然后我们使用 `if` / `else if` / `else` 链来检查这个数字是负数、零还是正数。

在 Auto 中，`if` 语句不需要在条件周围加括号——你只需写 `if condition { ... }`。大括号 `{}` 定义了条件为真时运行的代码块。相比之下，Python 在条件后使用冒号 `:`，并用缩进来定义代码块。

请注意，Auto 的 `else if` 在被 `a2p` 转译时会变成 Python 的 `elif`。这是因为 Python 使用关键字 `elif`（"else if"的缩写），而 Auto 则完整拼写出来。

> **Python 程序员注意：**
>
> 在 Python 中，条件以冒号（`:`）结尾，代码块通过缩进定义。在 Auto 中，条件不使用冒号——代码块通过大括号 `{}` 定义。`a2p` 转译器会自动处理这个转换。
>
> 还要注意，Auto 使用 `else if`（两个单词），而 Python 使用 `elif`（一个单词）。

Auto 中一个最小的有效 `if` 语句如下所示：

```auto
if true {
    print("Yes, it is true")
}
```

你可以在 `if` 语句的代码块内部再嵌套一个 `if` 语句，以此类推——这被称为嵌套 `if` 语句。请记住，`else if` 和 `else` 部分是可选的。

## `while` 循环（使用 `for`）

Auto 没有 `while` 关键字。相反，当给 `for` 关键字一个布尔条件（而不是范围）时，它同时充当 while 循环。`a2p` 转译器会检测这种模式并输出 Python 的 `while` 语句。

这种设计保持了语言的简洁——一个 `for` 关键字同时处理迭代和条件循环。

<Listing number="6-2" file-name="while.auto" caption="在 Auto 中使用 while 循环模式">

```auto
fn main() {
    let mut running = true
    let mut count = 0

    for running {
        print(count)
        count += 1
        if count >= 5 {
            running = false
        }
    }
}
```

```python
def main():
    running = True
    count = 0

    while running:
        print(count)
        count += 1
        if count >= 5:
            running = False


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

在这个程序中，我们使用 `let mut` 声明了两个可变变量：`running`（一个布尔标志）和 `count`（一个计数器）。`mut` 关键字告诉 Auto 这些变量稍后会被重新赋值。

然后我们写 `for running { ... }`。由于 `running` 是一个布尔表达式（不是像 `0..10` 这样的范围），`a2p` 转译器将其识别为 while 循环并转译为 Python 的 `while running:`。

在循环体内部，我们打印 `count` 的当前值，将其加 1，然后检查是否已经达到 5。如果是，我们将 `running` 设置为 `false`，这会导致在下一次条件检查时循环停止。

输出如下：

```
0
1
2
3
4
```

> **Python 程序员注意：**
>
> Auto 没有 `while` 关键字。当你写 `for condition { ... }`，其中 `condition` 是一个布尔表达式（而不是范围）时，`a2p` 会将其转译为 Python 的 `while condition:`。这是 Auto 的设计理念——一个 `for` 关键字同时服务于两种用途。
>
> 注意 Auto 使用 `let mut` 来声明可变变量。在 Python 中，所有变量默认都是可变的，所以 `a2p` 在输出中会直接去掉 `let mut` 前缀。

## `for` 循环

带有范围的 `for` 循环用于迭代一个数字序列。语法是 `for variable in start..end { ... }`，它生成从 `start` 到 `end`（但不包括 `end`）的数字。

<Listing number="6-3" file-name="for_range.auto" caption="使用带范围的 for 循环">

```auto
fn main() {
    for i in 0..5 {
        print(i)
    }
}
```

```python
def main():
    for i in range(0, 5):
        print(i)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

我们写 `for i in 0..5 { ... }`，它让 `i` 遍历值 `0`、`1`、`2`、`3`、`4`。注意 `5` **不**包含在内——范围 `0..5` 到达但不包含上界，就像 Python 的 `range(0, 5)` 一样。

当通过 `a2p` 转译时，Auto 的范围 `0..5` 变成 Python 的 `range(0, 5)`。两者产生相同的数字序列：`[0, 1, 2, 3, 4]`。

输出如下：

```
0
1
2
3
4
```

> **Python 程序员注意：**
>
> Auto 的 `0..5` 完全等价于 Python 的 `range(0, 5)`。`..` 运算符创建一个半开范围（不包含上界）。当你需要步长不为 1 的循环时，可以使用 `for i in 0..10 { if i % 2 == 0 { ... } }` 通过条件来筛选，或者 `a2p` 在未来版本中将支持更复杂的范围表达式。

## `break` 语句

`break` 语句用于_跳出_循环语句——也就是说，停止循环语句的执行，即使循环条件还没有变为 `false` 或者序列中的项目还没有完全遍历完。

<Listing number="6-4" file-name="break_stmt.auto" caption="使用 break 语句">

```auto
fn main() {
    for i in 0..10 {
        if i == 5 {
            break
        }
        print(i)
    }
}
```

```python
def main():
    for i in range(0, 10):
        if i == 5:
            break
        print(i)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

在这个程序中，我们让 `i` 从 `0` 遍历到 `9`。然而，在循环体内部我们检查 `i` 是否等于 `5`。当等于时，我们执行 `break`，它会立即退出循环——不再执行更多的迭代，程序继续执行循环后面的代码。

所以即使范围到了 `10`，循环也只打印 `0` 到 `4` 的值，然后停止。

输出如下：

```
0
1
2
3
4
```

> **注意：** `break` 语句在 Auto 的两种 `for` 循环中都可以使用——范围循环（`for i in 0..10`）和条件循环（`for condition`）。

## `continue` 语句

`continue` 语句用于告诉 Auto 跳过当前循环块中剩余的语句，并_继续_到循环的下一次迭代。

<Listing number="6-5" file-name="continue_stmt.auto" caption="使用 continue 语句">

```auto
fn main() {
    for i in 0..10 {
        if i % 2 == 0 {
            continue
        }
        print(i)
    }
}
```

```python
def main():
    for i in range(0, 10):
        if i % 2 == 0:
            continue
        print(i)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

在这个程序中，我们让 `i` 从 `0` 遍历到 `9`。对于每个值，我们检查它是否是偶数（`i % 2 == 0`）。如果是偶数，`continue` 语句会跳过循环体的剩余部分（即 `print(i)` 调用），然后继续下一次迭代。如果是奇数，则正常执行 `print(i)`。

这实际上只打印了 0 到 9 之间的奇数。

输出如下：

```
1
3
5
7
9
```

> **注意：** `continue` 语句在 Auto 的两种 `for` 循环中都可以使用——范围循环和条件循环。

## 小结

我们学习了如何在 Auto 中使用控制流语句：

- **`if` / `else if` / `else`** ——根据条件做决定。Auto 使用 `else if`，`a2p` 会将其转译为 Python 的 `elif`。
- **`for condition { ... }`** ——Auto 的 while 循环模式。当 `for` 关键字后面跟着布尔表达式（而不是范围）时，`a2p` 会将其转译为 Python 的 `while`。
- **`for i in start..end { ... }`** ——遍历一个数字范围。范围 `0..5` 等价于 Python 的 `range(0, 5)`。
- **`break`** ——立即退出循环，不管循环条件如何。
- **`continue`** ——跳过当前迭代的剩余部分，继续下一次迭代。

请记住，Auto 使用大括号 `{}` 来定义代码块，而 Python 使用缩进。`a2p` 转译器会自动处理这个转换，因此你可以编写干净的大括号分隔的 Auto 代码，并获得正确缩进的 Python 输出。

接下来，我们将学习如何创建和使用函数。
