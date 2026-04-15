# 返回值

在前几章中，我们使用了内置函数（如 `abs` 和 `round`）以及 math 模块中的函数（如 `sqrt` 和 `pow`）。当你调用这些函数时，它们会返回一个值，你可以将其赋给变量或用作表达式的一部分。

到目前为止我们编写的函数有所不同。有些函数使用 `print` 来显示值，有些函数使用 turtle 函数来绘制图形。但它们不会返回我们可以赋给变量或在表达式中使用的值。

在本章中，我们将学习如何编写具有返回值的函数。

## 有些函数有返回值

当你调用像 `math.sqrt` 这样的函数时，结果被称为**返回值**（return value）。如果将返回值赋给变量，你可以稍后使用它或将其用作表达式的一部分。

下面是一个返回值的函数示例：

```auto
fn circle_area(radius: f64) -> f64 {
    let area = 3.14159 * radius * radius
    return area
}
```

`circle_area` 接受 `radius` 作为参数，计算以该值为半径的圆的面积。最后一行是 `return` 语句，返回 `area` 的值。

我们可以将返回值赋给变量：

```auto
let a = circle_area(3.66)
```

或者将其用作表达式的一部分：

```auto
circle_area(radius) + 2.0 * circle_area(radius / 2.0)
```

`area` 是函数内部的局部变量，所以我们无法从函数外部访问它。

> **Python 程序员注意：**
>
> Auto 使用 `-> f64` 来声明函数的返回类型。`a2p` 转译器会去除返回类型注解。在 Auto 中，`return` 的工作方式与 Python 相同 -- 它结束函数并将一个值返回给调用者。

<Listing number="6-1" file-name="return_values.auto" caption="返回值与纯函数">

```auto
fn circle_area(radius: f64) -> f64 {
    let area = 3.14159 * radius * radius
    return area
}

fn repeat_string(word: str, n: int) -> str {
    return word * n
}

fn main() {
    // circle_area 的返回值
    let radius = 3.66
    let a = circle_area(radius)
    print("Area of circle with radius $radius:", a)

    // 在表达式中使用返回值
    let total = circle_area(radius) + 2.0 * circle_area(radius / 2.0)
    print("Combined area:", total)

    // 纯函数：repeat_string 返回一个值
    let line = repeat_string("Spam, ", 4)
    print(line)

    // 没有返回语句的函数返回空值
    print(repeat_string("Finland, ", 3))
}
```

```python
import math

def circle_area(radius):
    area = math.pi * radius ** 2
    return area


def repeat_string(word, n):
    return word * n


def main():
    # circle_area 的返回值
    radius = 3.66
    a = circle_area(radius)
    print(f"Area of circle with radius {radius}: {a}")

    # 在表达式中使用返回值
    total = circle_area(radius) + 2.0 * circle_area(radius / 2.0)
    print(f"Combined area: {total}")

    # 纯函数：repeat_string 返回一个值
    line = repeat_string("Spam, ", 4)
    print(line)

    # 没有返回语句的函数返回空值
    print(repeat_string("Finland, ", 3))


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`circle_area` 使用公式 pi * r^2 计算圆的面积，并通过 `return area` 返回结果。`repeat_string` 接受一个单词和一个计数，然后使用字符串的 `*` 运算符返回重复 `n` 次的单词。两者都是**纯函数** -- 它们返回一个值而不打印任何内容或产生其他副作用。

在 `main()` 中，我们调用这些函数并在表达式和赋值中使用它们的返回值。注意 Auto 中的 `return` 关键字与 Python 中相同。

## 有些函数返回 None

如果一个函数没有 `return` 语句，它会返回 `None`，这是一个类似 `True` 和 `False` 的特殊值。例如，第 3 章中的 `repeat` 函数使用 `print` 来显示字符串，但没有使用 `return` 来返回值。

相比之下，`repeat_string` 使用 `return word * n` 来返回结果。使用这个版本，我们可以将结果赋给变量并在稍后使用。

这样的函数被称为**纯函数**（pure function），因为它除了返回一个值之外，不会显示任何内容或产生其他效果。

## 返回值与条件语句

如果我们没有 `abs`，可以这样编写：

```auto
fn absolute_value(x: f64) -> f64 {
    if x < 0.0 {
        return -x
    } else {
        return x
    }
}
```

如果 `x` 是负数，第一个 `return` 语句返回 `-x` 并立即结束函数。否则，第二个 `return` 语句返回 `x` 并结束函数。

但是，如果在条件语句中放置 `return` 语句，必须确保程序的每条可能路径都会遇到一个 `return` 语句。考虑这个不正确的版本：

```auto
fn absolute_value_wrong(x: f64) -> f64 {
    if x < 0.0 {
        return -x
    }
    if x > 0.0 {
        return x
    }
    // 错误：x == 0 怎么办？这个函数没有处理这种情况！
}
```

当 `x` 为 `0` 时，两个条件都不为真，函数在没有遇到 `return` 语句的情况下结束，这意味着返回值为 `None`。

永远无法执行的代码被称为**死代码**（dead code）。例如，放在另一个必定执行的 `return` 语句之后的 `return` 语句永远无法到达。

## 渐进式开发

随着你编写越来越大的函数，可能会发现调试花费的时间越来越多。为了应对日益复杂的程序，你可以尝试**渐进式开发**（incremental development），即每次只添加和测试少量代码。

举个例子，假设你想求由坐标 (x1, y1) 和 (x2, y2) 表示的两个点之间的距离。根据勾股定理，距离为：

**distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)**

第一步是考虑 `distance` 函数应该是什么样子 -- 即输入（参数）是什么，输出（返回值）是什么？

对于这个函数，输入是点的坐标。返回值是距离。你可以立即编写函数的大纲：

```auto
fn distance(x1: f64, y1: f64, x2: f64, y2: f64) -> f64 {
    return 0.0
}
```

这个版本还不计算距离 -- 它总是返回零。但它是一个完整的带有返回值的函数，这意味着你可以在使其更复杂之前先测试它。

渐进式开发的关键方面是：

1. 从一个可运行的程序开始，每次做小改动，每次改动后都进行测试。
2. 使用变量保存中间值，以便显示和检查它们。
3. 一旦程序正常工作，移除脚手架代码。

开发过程中使用但不属于最终版本的代码被称为**脚手架**（scaffolding）。

## 布尔函数

函数可以返回布尔值 `true` 和 `false`，这对于将复杂测试封装在函数中非常方便。例如，`is_divisible` 检查 `x` 是否能被 `y` 整除：

```auto
fn is_divisible(x: int, y: int) -> bool {
    return x % y == 0
}
```

`==` 运算符的结果是布尔值，所以我们可以直接返回它而不需要 `if` 语句。布尔函数通常在条件语句中使用：

```auto
if is_divisible(6, 2) {
    print("divisible")
}
```

没有必要（也不符合惯用法）将结果与 `true` 比较：

```auto
// 不要这样做：
if is_divisible(6, 2) == true { ... }

// 应该这样做：
if is_divisible(6, 2) { ... }
```

<Listing number="6-2" file-name="incremental_dev.auto" caption="渐进式开发与布尔函数">

```auto
fn is_divisible(x: int, y: int) -> bool {
    return x % y == 0
}

fn distance(x1: f64, y1: f64, x2: f64, y2: f64) -> f64 {
    let dx = x2 - x1
    let dy = y2 - y1
    let dsquared = dx * dx + dy * dy
    let result = dsquared.sqrt()
    return result
}

fn main() {
    // 第一步：从一个总是返回 0 的桩函数开始
    // 第二步：添加 dx, dy 计算
    // 第三步：添加 dsquared 计算
    // 第四步：使用 sqrt 并返回结果

    let d = distance(1.0, 2.0, 4.0, 6.0)
    print("distance(1, 2, 4, 6) =", d)

    // 在条件语句中使用布尔函数
    if is_divisible(6, 2) {
        print("6 is divisible by 2")
    }

    if is_divisible(6, 4) {
        print("6 is divisible by 4")
    } else {
        print("6 is NOT divisible by 4")
    }
}
```

```python
import math

def is_divisible(x, y):
    return x % y == 0


def distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    dsquared = dx ** 2 + dy ** 2
    result = math.sqrt(dsquared)
    return result


def main():
    # 第一步：从一个总是返回 0 的桩函数开始
    # 第二步：添加 dx, dy 计算
    # 第三步：添加 dsquared 计算
    # 第四步：使用 sqrt 并返回结果

    d = distance(1, 2, 4, 6)
    print(f"distance(1, 2, 4, 6) = {d}")

    # 在条件语句中使用布尔函数
    if is_divisible(6, 2):
        print("6 is divisible by 2")

    if is_divisible(6, 4):
        print("6 is divisible by 4")
    else:
        print("6 is NOT divisible by 4")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`distance` 函数展示了渐进式开发的最终结果。它先计算 `dx` 和 `dy`（x 和 y 坐标的差值），然后计算 `dsquared`（平方和），最后使用 `sqrt` 得到距离。在开发过程中的每一步，你都应该测试函数以确保中间值正确，然后再添加更多代码。

`is_divisible` 展示了一个简洁的布尔函数 -- 它直接返回 `x % y == 0` 的结果。在 `main()` 函数中，我们将 `is_divisible` 用作 `if` 语句中的条件，而不将其与 `true` 比较。

> **Python 程序员注意：**
>
> Auto 使用 `&&` 代替 Python 的 `and`，使用 `||` 代替 Python 的 `or`。Auto 使用 `true`/`false` 代替 Python 的 `True`/`False`。`a2p` 转译器会自动转换这些。

## 带返回值的递归

既然我们可以编写具有返回值的函数，我们也可以编写带返回值的递归函数。有了这个能力，我们已经跨过了一个重要的门槛 -- 我们目前使用的 Auto 子集现在是**图灵完备的**（Turing complete），这意味着我们可以执行任何可以用算法描述的计算。

为了演示带返回值的递归，我们将计算一个递归定义的数学函数。阶乘函数，用符号 `!` 表示，定义如下：

- 0! = 1
- n! = n * (n-1)!

这个定义说 0 的阶乘是 1，而任何其他值 n 的阶乘是 n 乘以 (n-1) 的阶乘。

按照渐进式开发的过程，最终的函数如下：

```auto
fn factorial(n: int) -> int {
    if n == 0 {
        return 1
    } else {
        let recurse = factorial(n - 1)
        return n * recurse
    }
}
```

这个程序的执行流程类似于第 5 章中 `countdown` 的流程。如果我们用值 `3` 调用 `factorial`：

因为 3 不是 0，我们走第二个分支并计算 n-1 的阶乘...

> 因为 2 不是 0，我们走第二个分支并计算 n-1 的阶乘...
>
> > 因为 1 不是 0，我们走第二个分支并计算 n-1 的阶乘...
> >
> > > 因为 0 等于 0，我们走第一个分支并返回 1，不再进行递归调用。
> >
> > 返回值 1 乘以 n（即 1），结果被返回。
>
> 返回值 1 乘以 n（即 2），结果被返回。

返回值 2 乘以 n（即 3），结果 6 成为启动整个过程的函数调用的返回值。

## 信念之跃

跟踪执行流程是阅读程序的一种方式，但它可能很快变得令人困惑。另一种方式是我称之为"信念之跃"（leap of faith）的方法。当你遇到函数调用时，不跟踪执行流程，而是*假设*该函数工作正常并返回了正确的结果。

事实上，当你使用内置函数时，你已经在实践这种信念之跃了。当你调用 `abs` 或 `math.sqrt` 时，你不会检查这些函数的内部实现 -- 你只是假设它们能正常工作。

递归程序也是如此。当你遇到递归调用时，不跟踪执行流程，而是假设递归调用能正常工作，然后问自己："假设我能计算 n-1 的阶乘，我能计算 n 的阶乘吗？"阶乘的递归定义告诉你，通过乘以 n 就可以。

## 斐波那契

在 `factorial` 之后，最常见的递归函数例子是 `fibonacci`（斐波那契），其定义如下：

- fibonacci(0) = 0
- fibonacci(1) = 1
- fibonacci(n) = fibonacci(n-1) + fibonacci(n-2)

翻译成 Auto 如下：

```auto
fn fibonacci(n: int) -> int {
    if n == 0 {
        return 0
    } else if n == 1 {
        return 1
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2)
    }
}
```

如果你尝试在这里跟踪执行流程，即使对于很小的 n 值，你的头脑也会爆炸。但根据信念之跃，如果你假设两个递归调用都能正常工作，你就可以确信最后一个 `return` 语句是正确的。

顺便说一下，这种计算斐波那契数的方法效率非常低。我们将在后面的章节中探讨原因并提出改进方案。

<Listing number="6-4" file-name="recursion.auto" caption="递归阶乘与斐波那契">

```auto
fn factorial(n: int) -> int {
    if n == 0 {
        return 1
    } else {
        let recurse = factorial(n - 1)
        return n * recurse
    }
}

fn fibonacci(n: int) -> int {
    if n == 0 {
        return 0
    } else if n == 1 {
        return 1
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2)
    }
}

fn main() {
    // 阶乘
    print("factorial(0):", factorial(0))
    print("factorial(1):", factorial(1))
    print("factorial(3):", factorial(3))
    print("factorial(5):", factorial(5))

    // 斐波那契
    print("fibonacci(0):", fibonacci(0))
    print("fibonacci(1):", fibonacci(1))
    print("fibonacci(5):", fibonacci(5))
    print("fibonacci(10):", fibonacci(10))
}
```

```python
def factorial(n):
    if n == 0:
        return 1
    else:
        recurse = factorial(n - 1)
        return n * recurse


def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def main():
    # 阶乘
    print(f"factorial(0): {factorial(0)}")
    print(f"factorial(1): {factorial(1)}")
    print(f"factorial(3): {factorial(3)}")
    print(f"factorial(5): {factorial(5)}")

    # 斐波那契
    print(f"fibonacci(0): {fibonacci(0)}")
    print(f"fibonacci(1): {fibonacci(1)}")
    print(f"fibonacci(5): {fibonacci(5)}")
    print(f"fibonacci(10): {fibonacci(10)}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`factorial` 使用递归定义：基本情况是 `n == 0`（返回 1），递归情况将 `n` 乘以 `factorial(n-1)`。局部变量 `recurse` 在乘以 `n` 之前存储递归调用的结果。

`fibonacci` 有两个基本情况（`n == 0` 返回 0，`n == 1` 返回 1），并在 else 分支中进行两次递归调用。这种"树形递归"结构意味着函数对每个非基本情况调用自身两次，呈指数级增长。

## 类型检查

如果我们在调用 `factorial` 时传入 `1.5` 作为参数会发生什么？看起来像是无限递归。怎么可能呢？函数在 `n == 1` 或 `n == 0` 时有基本情况。但如果 `n` 不是整数，我们可能*错过*基本情况而永远递归下去。

为了避免无限递归，我们可以检查参数的类型。在 Auto 中，类型系统帮助在编译时捕获许多此类错误。当你声明 `fn factorial(n: int)` 时，传入浮点数将是一个类型错误。

为了额外的安全性，我们可以添加**输入验证**（input validation） -- 检查函数的参数以确保它们具有正确的类型和值。

## 调试

将大型程序分解为较小的函数会创建自然的调试检查点。如果一个函数不能正常工作，有三种可能性需要考虑：

- 函数接收到的参数有问题 -- 即前置条件被违反。
- 函数本身有问题 -- 即后置条件被违反。
- 调用者对返回值的使用有问题。

要排除第一种可能性，可以在函数开头添加 `print` 语句来显示参数的值。如果参数看起来没问题，可以在每个 `return` 语句之前添加 `print` 语句来显示返回值。如果函数似乎正常工作，检查函数调用以确保返回值被正确使用 -- 或者是否被使用了！

在函数的开头和结尾添加 `print` 语句可以帮助使执行流程更加可见。

## 术语表

**返回值（return value）：**
函数的结果。如果函数调用被用作表达式，返回值就是该表达式的值。

**纯函数（pure function）：**
除了返回值之外，不显示任何内容或产生任何其他效果的函数。

**死代码（dead code）：**
程序中永远无法执行的部分，通常因为它出现在 `return` 语句之后。

**渐进式开发（incremental development）：**
一种程序开发计划，通过每次只添加和测试少量代码来避免调试。

**脚手架（scaffolding）：**
程序开发期间使用但不是最终版本一部分的代码。

**图灵完备（Turing complete）：**
如果一种语言或语言的子集可以执行任何可以用算法描述的计算，则它是图灵完备的。

**输入验证（input validation）：**
检查函数的参数以确保它们具有正确的类型和值。

## 练习

### 练习

使用渐进式开发编写一个名为 `hypot` 的函数，给定直角三角形的两条直角边长度，返回斜边的长度。

注意：math 模块中有一个名为 `hypot` 的函数可以做同样的事情，但在这个练习中你不应该使用它！

即使你第一次就能正确编写这个函数，也要从一个总是返回 `0` 的函数开始，练习做小改动并逐步测试。完成后，函数应该只返回一个值 -- 它不应该显示任何内容。

### 练习

编写一个布尔函数 `is_between(x, y, z)`，如果 x < y < z 或 z < y < x，则返回 `true`，否则返回 `false`。

你可以用以下示例来测试你的函数：

```
is_between(1, 2, 3)  // 应该返回 true
is_between(3, 2, 1)  // 应该返回 true
is_between(1, 3, 2)  // 应该返回 false
is_between(2, 3, 1)  // 应该返回 false
```

<Listing number="6-3" file-name="boolean_funcs.auto" caption="布尔函数：is_between 和 is_power">

```auto
fn is_between(x: f64, y: f64, z: f64) -> bool {
    return (x < y && y < z) || (z < y && y < x)
}

fn is_power(a: int, b: int) -> bool {
    if a == 1 {
        return true
    }
    if a % b == 0 {
        return is_power(a / b, b)
    }
    return false
}

fn main() {
    // 测试 is_between
    print("is_between(1, 2, 3):", is_between(1.0, 2.0, 3.0))
    print("is_between(3, 2, 1):", is_between(3.0, 2.0, 1.0))
    print("is_between(1, 3, 2):", is_between(1.0, 3.0, 2.0))
    print("is_between(2, 3, 1):", is_between(2.0, 3.0, 1.0))

    // 测试 is_power
    print("is_power(65536, 2):", is_power(65536, 2))
    print("is_power(27, 3):", is_power(27, 3))
    print("is_power(24, 2):", is_power(24, 2))
    print("is_power(1, 17):", is_power(1, 17))
}
```

```python
def is_between(x, y, z):
    return (x < y and y < z) or (z < y and y < x)


def is_power(a, b):
    if a == 1:
        return True
    if a % b == 0:
        return is_power(a // b, b)
    return False


def main():
    # 测试 is_between
    print(f"is_between(1, 2, 3): {is_between(1, 2, 3)}")
    print(f"is_between(3, 2, 1): {is_between(3, 2, 1)}")
    print(f"is_between(1, 3, 2): {is_between(1, 3, 2)}")
    print(f"is_between(2, 3, 1): {is_between(2, 3, 1)}")

    # 测试 is_power
    print(f"is_power(65536, 2): {is_power(65536, 2)}")
    print(f"is_power(27, 3): {is_power(27, 3)}")
    print(f"is_power(24, 2): {is_power(24, 2)}")
    print(f"is_power(1, 17): {is_power(1, 17)}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`is_between` 在 `y` 位于 `x` 和 `z` 之间时（升序或降序）返回 `true`。它使用 `&&`（与）和 `||`（或）来组合两种可能的顺序。

`is_power` 使用递归检查 `a` 是否是 `b` 的幂。基本情况是 `a == 1`（因为对于任何 b，b^0 = 1）。如果 `a` 能被 `b` 整除，它递归检查 `a / b` 是否是 `b` 的幂。否则，`a` 不是 `b` 的幂。

### 练习

阿克曼函数 A(m, n) 定义如下：

- A(m, n) = n+1，如果 m = 0
- A(m, n) = A(m-1, 1)，如果 m > 0 且 n = 0
- A(m, n) = A(m-1, A(m, n-1))，如果 m > 0 且 n > 0

编写一个名为 `ackermann` 的函数来计算阿克曼函数。如果你调用 `ackermann(5, 5)` 会发生什么？

你可以用以下示例来测试你的函数：

```
ackermann(3, 2)  // 应该返回 29
ackermann(3, 3)  // 应该返回 61
ackermann(3, 4)  // 应该返回 125
```

### 练习

一个数 a 是 b 的幂，如果它能被 b 整除且 a/b 是 b 的幂。编写一个名为 `is_power` 的函数，接受参数 `a` 和 `b`，如果 `a` 是 `b` 的幂则返回 `true`。

你可以用以下示例来测试你的函数：

```
is_power(65536, 2)   // 应该返回 true
is_power(27, 3)      // 应该返回 true
is_power(24, 2)      // 应该返回 false
is_power(1, 17)      // 应该返回 true
```

### 练习

a 和 b 的最大公约数（GCD）是能同时整除两者的最大数。求两个数的 GCD 的一种方法基于以下观察：如果 r 是 a 除以 b 的余数，那么 gcd(a, b) = gcd(b, r)。作为基本情况，我们可以使用 gcd(a, 0) = a。

编写一个名为 `gcd` 的函数，接受参数 `a` 和 `b`，返回它们的最大公约数。

你可以用以下示例来测试你的函数：

```
gcd(12, 8)    // 应该返回 4
gcd(13, 17)   // 应该返回 1
```
