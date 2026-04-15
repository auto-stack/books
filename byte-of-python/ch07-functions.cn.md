# 函数

函数是可重用的程序片段。它们允许你给一组语句命名，使你可以在程序中任何位置、以任意次数通过指定的名称来运行这组语句。这被称为_调用_函数。我们已经使用过许多内置函数，如 `print` 和 `range`。

函数概念可能是任何非平凡软件（在任何编程语言中）_最_重要的构建块，因此我们将在本章中探索函数的各个方面。

函数使用 `fn` 关键字来定义。在这个关键字之后是函数的_标识符_名称，接着是一对圆括号，其中可以包含一些带类型的参数名，最后是返回类型。函数体用大括号 `{}` 包围。一个例子会展示这其实非常简单：

## 定义函数

以下是 Auto 中一个最小的函数定义：

```auto
fn greet() {
    print("Hello, World!")
}
```

与之对比的 Python 等价写法：

```python
def greet():
    print("Hello, World!")
```

在 Auto 中，你使用 `fn` 而不是 Python 的 `def`，函数体用大括号 `{}` 包围而不是使用缩进。带有返回类型的函数使用 `->` 语法：

```auto
fn add(a: int, b: int) -> int {
    return a + b
}
```

这在 Python 中变成：

```python
def add(a, b):
    return a + b
```

注意 `a2p` 转译器会移除类型标注——Auto 的类型提示（`int`）用于提高可读性，不会被带入 Python 输出中。

## 函数参数

函数可以接受参数，参数是你提供给函数的值，以便函数可以_利用_这些值_执行_某些操作。这些参数就像变量一样，只不过这些变量的值是在我们调用函数时定义的，并且在函数运行时已经被赋值。

参数在函数定义的圆括号内指定，用逗号分隔。当我们调用函数时，以同样的方式提供值。请注意所使用的术语——函数定义中给出的名称称为_参数_（parameters），而你在函数调用中提供的值称为_实参_（arguments）。

<Listing number="7-1" file-name="param.auto" caption="函数参数">

```auto
fn print_max(a: int, b: int) {
    if a > b {
        print(f"$a is maximum")
    } else if a < b {
        print(f"$b is maximum")
    } else {
        print("Both are equal")
    }
}

fn main() {
    // directly pass literal values
    print_max(3, 4)

    let x = 5
    let y = 7

    // pass variables as arguments
    print_max(x, y)
}
```

```python
def print_max(a, b):
    if a > b:
        print(f"{a} is maximum")
    elif a < b:
        print(f"{b} is maximum")
    else:
        print("Both are equal")


def main():
    # directly pass literal values
    print_max(3, 4)

    x = 5
    y = 7

    # pass variables as arguments
    print_max(x, y)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

在这里，我们定义了一个名为 `print_max` 的函数，它使用两个名为 `a` 和 `b` 的参数。我们使用一个简单的 `if..else if..else` 语句找出较大的数字，然后打印它。

第一次调用函数 `print_max` 时，我们直接提供数字作为实参。第二种情况下，我们使用变量作为实参来调用函数。`print_max(x, y)` 将实参 `x` 的值赋给参数 `a`，将实参 `y` 的值赋给参数 `b`。`print_max` 函数在两种情况下的工作方式相同。

输出如下：

```
4 is maximum
7 is maximum
```

> **Python 程序员注意：**
>
> 在 Auto 中，函数参数需要类型标注（如 `a: int`）。`a2p` 转译器在生成 Python 代码时会去除这些类型标注。Auto 使用 `//` 表示注释，在 Python 中会变成 `#`。

## 局部变量

当你在函数定义内部声明变量时，它们与函数外部使用的同名变量没有任何关系——也就是说，变量名对该函数是_局部的_。这被称为变量的_作用域_。所有变量的作用域都是从定义点开始的声明所在代码块。

<Listing number="7-2" file-name="local.auto" caption="使用局部变量">

```auto
fn func(x: int) {
    print(f"x is $x")
    let x = 2
    print(f"Changed local x to $x")
}

fn main() {
    let x = 50
    func(x)
    print(f"x is still $x")
}
```

```python
def func(x):
    print(f"x is {x}")
    x = 2
    print(f"Changed local x to {x}")


def main():
    x = 50
    func(x)
    print(f"x is still {x}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

第一次打印 *x* 的_值_时（函数体中的第一行），Auto 使用在主代码块中、函数定义之上声明的参数的值。

接下来，我们将值 `2` 赋给 `x`。名称 `x` 对我们的函数是局部的。因此，当我们在函数中更改 `x` 的值时，主代码块中定义的 `x` 不受影响。

通过最后一个 `print` 语句，我们显示主代码块中定义的 `x` 的值，从而确认它实际上不受之前调用的函数中局部赋值的影响。

输出如下：

```
x is 50
Changed local x to 2
x is still 50
```

> **Python 程序员注意：**
>
> 在 Auto 中，你必须使用 `let`（或 `let mut` 用于可变变量）声明局部变量。在上面的函数中，`let x = 2` 创建了一个新的局部变量 `x`，它遮蔽了参数 `x`。在 Python 中，你只需赋值 `x = 2` 而无需任何声明关键字。`a2p` 转译器在生成 Python 代码时会移除 `let` 关键字。

## `global` 语句

如果你想给程序顶层定义的名称（即不在函数或类等任何作用域内）赋值，那么你必须告诉 Auto 该名称不是局部的，而是_全局的_。我们使用 `global` 语句来实现这一点。如果没有 `global` 语句，是不可能给函数外部定义的变量赋值的。

你可以使用函数外部定义的这些变量的值（假设函数内没有同名的变量）。然而，不鼓励这样做，应该避免，因为对程序的读者来说，不清楚该变量的定义在哪里。使用 `global` 语句可以清楚地表明该变量在最外层的代码块中定义。

<Listing number="7-3" file-name="global.auto" caption="使用 global 语句">

```auto
let mut x = 50

fn func() {
    global x
    print(f"x is $x")
    x = 2
    print(f"Changed global x to $x")
}

fn main() {
    func()
    print(f"Value of x is $x")
}
```

```python
x = 50


def func():
    global x
    print(f"x is {x}")
    x = 2
    print(f"Changed global x to {x}")


def main():
    func()
    print(f"Value of x is {x}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`global` 语句用于声明 `x` 是一个全局变量——因此，当我们在函数内部给 `x` 赋值时，这个改变会反映到主代码块中使用 `x` 的值中。

你可以在同一个 `global` 语句中指定多个全局变量，例如 `global x, y, z`。

输出如下：

```
x is 50
Changed global x to 2
Value of x is 2
```

> **Python 程序员注意：**
>
> `global` 语句在 Auto 中和 Python 中的工作方式相同。但请注意，在 Auto 中，如果你打算从函数内部修改顶层变量，则必须使用 `let mut`（而不仅仅是 `let`）来声明它。`a2p` 转译器会移除 `let mut` 声明，在 Python 输出中将裸的 `x = 50` 赋值放在模块级别。

## 默认参数值

对于某些函数，你可能想让一些参数变为_可选的_，并在用户不想为它们提供值时使用默认值。这是通过默认参数值来实现的。你可以在函数定义中，在参数名后面追加赋值运算符（`=`）和默认值来指定默认参数值。

请注意，默认参数值应该是一个常量。更准确地说，默认参数值应该是不可变的——这在后面的章节中会详细解释。现在，只需记住这一点。

<Listing number="7-4" file-name="default.auto" caption="默认参数值">

```auto
fn say(message: str, times: int = 1) {
    for i in 0..times {
        print(message)
    }
}

fn main() {
    say("Hello")
    say("World", 5)
}
```

```python
def say(message, times=1):
    for i in range(0, times):
        print(message)


def main():
    say("Hello")
    say("World", 5)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

名为 `say` 的函数用于将字符串打印指定的次数。如果我们不提供值，则默认情况下，字符串只打印一次。我们通过给参数 `times` 指定默认参数值 `1` 来实现这一点。

在第一次使用 `say` 时，我们只提供了字符串，它打印了一次字符串。在第二次使用 `say` 时，我们同时提供了字符串和参数 `5`，表示我们想要_打印_该字符串消息 5 次。

输出如下：

```
Hello
World
World
World
World
World
```

> **Python 程序员注意：**
>
> 默认参数值在 Auto 中和 Python 中的工作方式相同：`fn say(message: str, times: int = 1)`。`a2p` 转译器将其转换为 `def say(message, times=1):`，去除类型标注的同时保留默认值。

> **注意**
>
> 只有参数列表末尾的参数才能被赋予默认参数值，即你不能在函数参数列表中让一个有默认值的参数位于没有默认值的参数之前。
>
> 这是因为值是按位置分配给参数的。例如，`fn func(a: int, b: int = 5)` 是有效的，但 `fn func(a: int = 5, b: int)` 是_无效的_。

## 关键字参数

如果你有一些包含许多参数的函数，并且只想指定其中的一些，那么你可以通过命名来为这些参数提供值——这被称为_关键字参数_——我们使用名称（关键字）而不是位置（我们一直在使用的方式）来指定函数的参数。

有两个优点——第一，使用函数更简单，因为我们不需要担心参数的顺序。第二，我们可以只为我们想要的参数提供值，前提是其他参数有默认参数值。

<Listing number="7-5" file-name="keyword.auto" caption="关键字参数">

```auto
fn func(a: int, b: int = 5, c: int = 10) {
    print(f"a is $a and b is $b and c is $c")
}

fn main() {
    func(3, 7)
    func(25, c = 24)
    func(c = 50, a = 100)
}
```

```python
def func(a, b=5, c=10):
    print(f"a is {a} and b is {b} and c is {c}")


def main():
    func(3, 7)
    func(25, c=24)
    func(c=50, a=100)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

名为 `func` 的函数有一个没有默认参数值的参数，后面跟着两个有默认参数值的参数。

在第一次使用中，`func(3, 7)`，参数 `a` 得到值 `3`，参数 `b` 得到值 `7`，`c` 得到默认值 `10`。

在第二次使用中 `func(25, c=24)`，变量 `a` 由于参数的位置得到值 25。然后，参数 `c` 由于命名（即关键字参数）得到值 `24`。变量 `b` 得到默认值 `5`。

在第三次使用中 `func(c=50, a=100)`，我们对所有指定的值使用关键字参数。请注意，我们即使在函数定义中 `a` 定义在 `c` 之前，也可以先为参数 `c` 指定值。

输出如下：

```
a is 3 and b is 7 and c is 10
a is 25 and b is 5 and c is 24
a is 100 and b is 5 and c is 50
```

> **Python 程序员注意：**
>
> 关键字参数在 Auto 中和 Python 中的工作方式相同。调用 `func(c=50, a=100)` 时，Auto 使用 `=` 运算符进行关键字赋值（不是 `:`），与 Python 的语法匹配。`a2p` 转译器会原样传递关键字参数。

## 可变参数

有时你可能想定义一个可以接受_任意_数量参数的函数，即**可变**数量的**参数**（varargs）。在 Python 中，这是通过星号（`*`）和双星号（`**`）运算符来实现的。

Auto 目前不支持 `*args` 或 `**kwargs` 语法。这是 Python 特有的功能。在 Auto 中，你可以使用数组或字典类型来达到类似的效果。

以下是在 Auto 中使用数组参数作为替代方案的写法：

<Listing number="7-6" file-name="varargs.auto" caption="可变参数（Auto vs Python）">

```auto
fn total(numbers: [int]) {
    let mut sum = 0
    for n in numbers {
        sum += n
    }
    print(f"The sum is $sum")
}

fn main() {
    total([1, 2])
    total([1, 2, 3, 4])
}
```

```python
def total(*numbers):
    print("a", numbers[0] if numbers else 5)

    # iterate through all the items in tuple
    for single_item in numbers[1:]:
        print("single_item", single_item)

    print("The sum is", sum(numbers))


def main():
    total(10, 1, 2, 3)
    print("---")
    total()
```

</Listing>

**工作原理**

在 Auto 版本中，我们传递一个列表 `[1, 2]` 作为类型为 `[int]`（整数数组）的单个参数。函数遍历数组并计算总和。这与 Python 的 `*args` 达到了相同的目标，而无需特殊语法。

在 Python 等价写法中，我们展示了原始的 Python `*args` 模式供参考。带星号的参数 `*numbers` 将所有位置参数收集到一个元组中。我们还看到 Python 支持可选的 `**kwargs`（双星号）参数来将关键字参数收集到字典中——这在 Auto 中没有直接的等价物。

Auto 版本的输出如下：

```
The sum is 3
The sum is 10
```

> **Python 程序员注意：**
>
> Auto 不支持 `*args` 或 `**kwargs`。相反，请显式传递数组和字典。例如，不用 `def func(*args)`，而在 Auto 中使用 `fn func(args: [int])` 并传递 `func([1, 2, 3])`。`a2p` 转译器会将 Auto 的数组类型 `[int]` 转换为 Python 列表，在迭代方面效果相似。
>
> 上面展示的 Python 等价写法演示了"Python 简明教程"中原始的 `*args`/`**kwargs` 模式供参考，但 Auto 版本使用的是显式数组参数。

## `return` 语句

`return` 语句用于从函数中_返回_，即跳出函数。我们也可以选择从函数中_返回一个值_。

<Listing number="7-7" file-name="return.auto" caption="使用 return 语句">

```auto
fn maximum(x: int, y: int) -> str {
    if x > y {
        return f"$x"
    } else if x == y {
        return "The numbers are equal"
    } else {
        return f"$y"
    }
}

fn main() {
    print(maximum(2, 3))
}
```

```python
def maximum(x, y):
    if x > y:
        return f"{x}"
    elif x == y:
        return "The numbers are equal"
    else:
        return f"{y}")


def main():
    print(maximum(2, 3))


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`maximum` 函数返回参数中的最大值，在这个例子中就是提供给函数的数字。它使用一个简单的 `if..else if..else` 语句找出较大的值，然后_返回_该值。

请注意，没有值的 `return` 语句等价于 `return None`。`None` 是 Python 中一种特殊的类型，表示"空"。例如，它用于指示一个变量没有值，如果它的值为 `None` 的话。

每个函数在末尾都隐含一个 `return None` 语句，除非你自己写了 `return` 语句。你可以通过运行 `print(some_function())` 来看到这一点，其中函数 `some_function` 没有使用 `return` 语句。

输出如下：

```
3
```

> **Python 程序员注意：**
>
> 在 Auto 中，返回值的函数必须使用 `-> type` 声明返回类型。`a2p` 转译器会从 Python 输出中去除返回类型标注。请注意，Auto 使用显式 `return` 语句（由于已知的转译器行为，`if` 块中的尾随表达式可能会丢失）。
>
> **提示：** 有一个名为 `max` 的内置函数已经实现了"查找最大值"的功能，所以请尽可能使用这个内置函数。

## 文档字符串

Python 有一个很棒的功能叫做_文档字符串_（documentation strings），通常简称为 _docstrings_。文档字符串是你应该使用的重要工具，因为它有助于更好地记录程序并使程序更容易理解。令人惊讶的是，我们甚至可以在程序实际运行时从函数中获取文档字符串！

Auto 没有像 Python 三引号字符串那样的内置文档字符串机制。相反，Auto 使用放在函数体顶部的 `//` 注释来记录函数。这是一种更简单的方法，保持了语言的轻量级。

<Listing number="7-8" file-name="docstring.auto" caption="使用注释为函数编写文档">

```auto
fn print_max(x: int, y: int) {
    // Prints the maximum of two numbers.
    // The two values must be integers.
    let a = x
    let b = y
    if a > b {
        print(f"$a is maximum")
    } else {
        print(f"$b is maximum")
    }
}

fn main() {
    print_max(3, 5)
    // In Python, you can access docstrings via print_max.__doc__
    // Auto does not support runtime docstring access.
    print("Documentation: Use // comments at the top of a function body.")
}
```

```python
def print_max(x, y):
    """Prints the maximum of two numbers.

    The two values must be integers."""
    # convert to integers, if possible
    x = int(x)
    y = int(y)

    if x > y:
        print(x, "is maximum")
    else:
        print(y, "is maximum")


def main():
    print_max(3, 5)
    print(print_max.__doc__)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

在 Auto 版本中，我们在函数体的顶部放置 `//` 注释行作为文档。这些注释描述了函数的功能以及关于其参数或行为的任何重要说明。虽然这些注释不能像 Python 文档字符串那样在运行时访问，但它们服务于为其他开发者记录代码的相同目的。

在 Python 等价写法中，我们使用传统的 Python 文档字符串——函数第一个逻辑行上的三引号字符串。Python 将此字符串视为函数的 `__doc__` 属性，使其可以通过 `print_max.__doc__` 或 `help()` 内置函数在运行时访问。

输出如下：

```
5 is maximum
Documentation: Use // comments at the top of a function body.
```

> **Python 程序员注意：**
>
> Auto 使用 `//` 注释进行文档记录，而不是 Python 的文档字符串。Auto 中没有运行时等价于 `__doc__` 或 `help()` 的功能。`a2p` 转译器会将 `//` 注释转换为 Python 输出中的 `#` 注释。如果你在 Python 中需要运行时可访问的文档，可以手动添加到转译后的代码中。
>
> Auto 中的约定是将文档注释放在函数左大括号之后的紧接行上。以大写字母开头，以句号结尾，就像 Python 文档字符串的约定一样。

## 小结

我们已经看到了函数的许多方面，但请注意我们还没有涵盖所有方面。不过，我们已经涵盖了你在日常使用 Auto 函数时所需的大部分内容。

- **`fn` 关键字** ——定义函数。Auto 使用 `fn` 代替 Python 的 `def`。
- **参数** ——传入函数的值。Auto 需要类型标注（如 `a: int`），`a2p` 会在 Python 输出中去除。
- **局部变量** ——在函数内部用 `let` 声明的变量的作用域限于该函数。
- **`global` 语句** ——允许函数修改在顶层定义的变量。顶层变量必须用 `let mut` 声明。
- **默认参数值** ——使参数变为可选的（如 `times: int = 1`）。只有末尾的参数可以有默认值。
- **关键字参数** ——通过名称而不是位置传递参数（如 `func(c=50, a=100)`）。
- **可变参数** ——Auto 不支持 `*args`/`**kwargs`。请使用显式的数组或字典参数代替。
- **`return` 语句** ——从函数返回一个值。有返回类型的函数在签名中使用 `-> type`。
- **文档字符串** ——Auto 使用 `//` 注释进行文档记录。没有运行时 `__doc__` 属性等价物。

接下来，我们将学习如何使用和创建模块。
