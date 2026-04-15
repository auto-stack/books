# 变量与语句

在上一章中，我们使用运算符编写了执行算术运算的表达式。

在本章中，你将学习变量和语句、`use` 语句（Auto 中相当于 Python 的 `import`）以及 `print` 函数。我们还将介绍更多用于讨论程序的术语，包括"参数"和"模块"。

## 变量

**变量**是一个指向值的名称。要创建变量，我们使用 `let` 关键字编写**赋值语句**：

```auto
let n = 17
```

赋值语句包含三个部分：`let` 关键字、变量名和要赋值的表达式。在这个例子中，表达式是一个整数。

在下面的例子中，表达式是一个浮点数：

```auto
let pi = 3.141592653589793
```

在这个例子中，表达式是一个字符串：

```auto
let message = "And now for something completely different"
```

当你运行赋值语句时，不会产生任何输出。Auto 创建变量并给它赋值，但赋值语句本身没有可见的效果。然而，创建变量后，你可以在表达式和函数调用中使用它：

```auto
let n = 17
print(n + 25)       // 输出 42
print(2 * pi)       // 输出 6.283185307179586
```

在 Auto 中，变量使用 `let` 声明。如果你需要一个值可以稍后更改的变量，可以使用 `let mut`（"mut" 是 "mutable" 的缩写，意为可变的）：

```auto
let mut x = 5
x = 10              // 因为有 mut，允许重新赋值
```

没有 `mut` 的话，重新赋值是不允许的，这有助于防止意外更改应该保持不变的值。

> **Python 程序员注意：**
>
> Python 没有 `let` 或 `mut` 关键字——你只需写 `n = 17`。在 Auto 中，所有变量声明都必须使用 `let`。`a2p` 转译器在生成 Python 代码时会去掉 `let` 和 `let mut`，因为 Python 中所有变量默认都是可变的。

<Listing number="2-1" file-name="variables.auto" caption="变量赋值与重新赋值">

```auto
fn main() {
    // 使用 let 创建变量
    let n = 17
    let pi = 3.141592653589793
    let message = "And now for something completely different"

    // 在表达式中使用变量
    print(n + 25)
    print(2 * pi)

    // 在函数调用中使用变量
    print(round(pi))
    print(len(message))

    // 使用 let mut 声明可变变量
    let mut x = 5
    print(x)
    x = 10
    print(x)
}
```

```python
def main():
    # 创建变量
    n = 17
    pi = 3.141592653589793
    message = "And now for something completely different"

    # 在表达式中使用变量
    print(n + 25)
    print(2 * pi)

    # 在函数调用中使用变量
    print(round(pi))
    print(len(message))

    # 可变变量
    x = 5
    print(x)
    x = 10
    print(x)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

首先，我们使用 `let` 声明了三个变量：`n`（整数）、`pi`（浮点数）和 `message`（字符串）。然后在算术表达式（`n + 25`、`2 * pi`）和函数调用（`round(pi)`、`len(message)`）中使用这些变量。结果说明一旦创建了变量，就可以在任何需要其值的地方使用。

接下来，我们使用 `let mut` 将 `x` 声明为可变变量。先打印其初始值（`5`），然后重新赋值为 `10` 并再次打印。如果没有 `mut`，重新赋值 `x = 10` 是不被允许的。在 Python 翻译中，所有变量默认都是可变的，因此 `let mut` 的区别消失了。

## 状态图

在纸上表示变量的一种常见方法是写出变量名并用箭头指向它的值。例如，执行以下赋值后：

```auto
let message = "And now for something completely different"
let n = 17
let pi = 3.141592653589793
```

状态图看起来像这样：

```
message --> "And now for something completely different"
n        --> 17
pi       --> 3.141592653589793
```

这种图被称为**状态图**，因为它展示了每个变量处于什么状态（可以把它想象成变量的"心理状态"）。我们将在整本书中使用状态图来表示变量和值是如何存储的模型。

## 变量名

变量名可以任意长。它们可以包含字母和数字，但不能以数字开头。使用大写字母是合法的，但惯例上变量名只使用小写字母。

变量名中唯一可以出现的标点符号是下划线字符 `_`。它常用于由多个单词组成的名称中，例如 `your_name` 或 `airspeed_of_unladen_swallow`。

如果你给变量一个非法的名称，就会得到语法错误。名称 `million!` 是非法的，因为它包含标点符号：

```auto
// 错误：变量名中出现意外的 '!'
let million! = 1000000
```

`76trombones` 是非法的，因为它以数字开头：

```auto
// 错误：变量名不能以数字开头
let 76trombones = "big parade"
```

`class` 也是非法的，但原因可能不太明显：

```auto
// 错误：应为标识符，但找到的是关键字
let class = "Self-Defence Against Fresh Fruit"
```

原来 `class` 是一个**关键字**，是用于指定程序结构的特殊词汇。关键字不能用作变量名。

以下是 Auto 的完整关键字列表：

```
fn        let       mut       if        else
for       in        return    true      false
use       as        type      struct    impl
break     continue  while     match     with
```

你不需要记住这个列表。在大多数开发环境中，关键字会以不同的颜色显示；如果你尝试将关键字用作变量名，你就会知道。

> **Python 程序员注意：**
>
> Auto 的关键字比 Python 少。Python 的许多关键字（如 `def`、`class`、`import`、`try`、`except`、`yield` 等）在 Auto 中以不同的方式处理。例如，Auto 使用 `fn` 代替 `def`，使用 `use` 代替 `import`，使用 `type` 代替 `class` 来定义自定义类型。

<Listing number="2-3" file-name="keywords.auto" caption="关键字与非法变量名">

```auto
fn main() {
    // 合法的变量名
    let my_name = "Alice"
    let _private = 42
    let item_count = 100
    let speed2 = 60

    print(my_name)
    print(_private)
    print(item_count)
    print(speed2)

    // 这些会导致语法错误：
    // let 76trombones = "big parade"   // 以数字开头
    // let million! = 1000000           // 包含标点符号
    // let fn = "keyword"               // fn 是关键字
}
```

```python
def main():
    # 合法的变量名
    my_name = "Alice"
    _private = 42
    item_count = 100
    speed2 = 60

    print(my_name)
    print(_private)
    print(item_count)
    print(speed2)

    # 这些会导致语法错误：
    # 76trombones = "big parade"   # 以数字开头
    # million! = 1000000           # 包含标点符号
    # fn = "keyword"               # fn 是关键字（在 Auto 中）


if __name__ == "__main__":
    main()
```

</Listing>

## use 语句

为了使用某些功能，你需要**导入**它们。在 Auto 中，这通过 `use` 关键字完成。例如，以下语句导入了 `math` 模块：

```auto
use math
```

**模块**是变量和函数的集合。`math` 模块提供了一个名为 `pi` 的变量，其中包含数学常数 pi 的值。我们可以这样显示它的值：

```auto
use math
print(math.pi)
```

要使用模块中的变量，你必须在模块名和变量名之间使用**点运算符**（`.`）。

`math` 模块还包含函数。例如，`sqrt` 计算平方根，`pow` 将一个数提升到另一个数的幂：

```auto
use math
print(math.sqrt(25))    // 输出 5.0
print(math.pow(5, 2))   // 输出 25.0
```

> **Python 程序员注意：**
>
> Auto 使用 `use math` 而不是 Python 的 `import math`。`a2p` 转译器会自动将 `use` 转换为 `import`。点运算符在两种语言中的工作方式相同。

<Listing number="2-2" file-name="use_print.auto" caption="使用模块和 print 函数">

```auto
use math

fn main() {
    // 使用模块变量
    print("The value of pi is approximately")
    print(math.pi)

    // 使用模块函数
    print(math.sqrt(25))
    print(math.pow(5, 2))

    // print 可以显示任意数量的值
    print("Any", "number", "of", "arguments")

    // print 用空格分隔值
    print("The value of pi is approximately", math.pi)
}
```

```python
import math


def main():
    # 使用模块变量
    print("The value of pi is approximately")
    print(math.pi)

    # 使用模块函数
    print(math.sqrt(25))
    print(math.pow(5, 2))

    # print 可以显示任意数量的值
    print("Any", "number", "of", "arguments")

    # print 用空格分隔值
    print("The value of pi is approximately", math.pi)


if __name__ == "__main__":
    main()
```

</Listing>

## 表达式与语句

到目前为止，我们已经看到了几种表达式。表达式可以是单个值，如整数、浮点数或字符串。它也可以是值和运算符的组合。它还可以包含变量名和函数调用。以下是一个包含其中几种元素的表达式：

```auto
use math
19 + n + round(math.pi) * 2
```

我们也看到了几种语句。**语句**是一段有作用但没有值的代码单元。例如，赋值语句创建一个变量并给它赋值，但语句本身没有值：

```auto
let n = 17
```

类似地，`use` 语句有作用——它导入一个模块以便我们可以使用其中包含的变量和函数——但它没有可见的效果：

```auto
use math
```

计算表达式的值称为**求值**（evaluation）。运行语句称为**执行**（execution）。

## print 函数

当你在交互式环境中求值一个表达式时，结果会被显示出来。但如果你求值多个表达式，只有最后一个表达式的值会被显示。

要显示多个值，你可以使用 `print` 函数：

```auto
print(n + 2)
print(n + 3)
```

它也可以处理浮点数和字符串：

```auto
print("The value of pi is approximately")
print(math.pi)
```

你还可以传递用逗号分隔的一系列表达式：

```auto
print("The value of pi is approximately", math.pi)
```

注意 `print` 会在值之间加一个空格。

## 参数

当你调用函数时，括号中的表达式被称为**参数**（arguments）。

我们目前见过的一些函数只接受一个参数，比如 `int`：

```auto
int("101")       // 将字符串转换为整数：101
```

有些接受两个参数，比如 `math.pow`：

```auto
math.pow(5, 2)   // 将 5 的 2 次方：25.0
```

有些可以接受额外的可选参数。例如，`int` 可以接受第二个参数来指定数字的进制：

```auto
int("101", 2)    // 将 "101" 解释为二进制：5
```

`round` 也接受一个可选的第二个参数，即四舍五入到的小数位数：

```auto
round(math.pi, 3)    // 将 pi 四舍五入到 3 位小数：3.142
```

有些函数可以接受任意数量的参数，比如 `print`：

```auto
print("Any", "number", "of", "arguments")
```

如果你调用函数时提供了太多参数，那是一个 `TypeError`。如果提供的参数太少，也是 `TypeError`。如果你提供的参数类型不对，同样也是 `TypeError`。这种检查在刚开始时可能会让人感到烦恼，但它能帮助你检测和纠正错误。

## 注释

随着程序变得越来越大、越来越复杂，阅读起来也会越来越困难。形式化语言很密集，仅仅看一段代码往往很难弄清楚它在做什么以及为什么这样做。

因此，在程序中添加注释来用自然语言解释程序在做什么是个好主意。这些注释被称为**注释**（comments）。

在 Auto 中，注释以 `//` 符号开头：

```auto
// 42 分 42 秒对应的总秒数
let seconds = 42 * 60 + 42
```

在这种情况下，注释单独占一行。你也可以把注释放在一行的末尾：

```auto
let miles = 10 / 1.61     // 10 公里换算为英里
```

从 `//` 到行末的所有内容都会被忽略——它对程序的执行没有任何影响。

注释在记录代码中不明显的特性时最有用。可以合理地假设读者能弄清楚代码做了*什么*；解释*为什么*才更有用。

这段注释与代码重复，是没用的：

```auto
let v = 8     // 将 8 赋值给 v
```

这段注释包含了代码中没有的有用信息：

```auto
let v = 8     // 速度，单位为英里/小时
```

好的变量名可以减少对注释的需求，但过长的变量名会使复杂表达式难以阅读，所以需要权衡。

> **Python 程序员注意：**
>
> Auto 使用 `//` 表示注释，而 Python 使用 `#`。`a2p` 转译器会自动将 `//` 转换为 `#`。

## 调试

程序中可能出现三种错误：语法错误、运行时错误和语义错误。区分它们对于更快地追踪和修复错误很有帮助。

* **语法错误**："语法"指的是程序的结构以及关于该结构的规则。如果程序中存在语法错误，编译器不会运行程序，而是立即显示错误消息。

* **运行时错误**：如果程序中没有语法错误，它可以开始运行。但如果运行过程中出了问题，程序会显示错误消息并停止。这种类型的错误也被称为**异常**（exception），因为它表示发生了异常情况。

* **语义错误**：第三种错误是"语义"错误，即与含义相关的错误。如果程序中存在语义错误，它运行时不会产生错误消息，但不会执行你预期的操作。识别语义错误可能比较困难，因为它需要你通过查看程序的输出进行反向推理，弄清楚程序实际在做什么。

正如我们看到的，非法的变量名是语法错误。如果你对不支持的类型使用运算符，那是运行时错误。如果你因为逻辑错误（比如忘记了运算优先级）写了一个产生错误结果的表达式，那是语义错误。

## 术语表

**变量 (variable):**
指向一个值的名称。

**赋值语句 (assignment statement):**
使用 `let` 将值赋给变量的语句。

**状态图 (state diagram):**
一组变量及其指向值的图形表示。

**关键字 (keyword):**
用于指定程序结构的特殊词汇。关键字不能用作变量名。

**use 语句 (use statement):**
读取模块文件以便使用其中包含的变量和函数的语句。相当于 Python 的 `import`。

**模块 (module):**
包含 Auto 代码的文件，包括函数定义和其他语句。

**点运算符 (dot operator):**
运算符 `.`，用于通过指定模块名后跟一个点和函数名/变量名来访问另一个模块中的函数或变量。

**求值 (evaluate):**
按顺序执行表达式中的运算以计算出一个值。

**语句 (statement):**
有作用但没有值的代码单元。

**执行 (execute):**
运行一个语句并执行它所描述的操作。

**参数 (argument):**
调用函数时提供给函数的值。

**注释 (comment):**
包含在程序中的文本，提供有关程序的信息，但对程序的执行没有影响。

**运行时错误 (runtime error):**
导致程序显示错误消息并退出的错误。

**异常 (exception):**
程序运行期间检测到的错误。

**语义错误 (semantic error):**
导致程序执行错误操作但不会显示错误消息的错误。

## 练习

### 练习

每当你学习一个新功能时，应该故意犯一些错误，看看会发生什么。

- 我们已经看到 `let n = 17` 是合法的。那么 `17 = n` 呢？
- 那么 `let x = 1` 后面跟着 `let x = 2` 呢？
- 如果拼错了模块名称，尝试 `use maath` 会怎样？

### 练习

练习使用 Auto 作为计算器：

**第 1 部分。** 半径为 $r$ 的球体体积为 $\frac{4}{3} \pi r^3$。半径为 5 的球体体积是多少？从名为 `radius` 的变量开始，然后将结果赋给名为 `volume` 的变量。显示结果。添加注释说明 `radius` 的单位是厘米，`volume` 的单位是立方厘米。

**第 2 部分。** 三角学的一个规则是，对于任何 $x$ 值，$(\cos x)^2 + (\sin x)^2 = 1$。让我们看看它对于 $x = 42$ 是否成立。创建一个名为 `x` 的变量并赋值为 42。然后使用 `math.cos` 和 `math.sin` 计算正弦和余弦，以及它们平方的和。结果应该接近 1。

**第 3 部分。** 除了 `pi` 之外，`math` 模块中定义的另一个变量是 `e`，它代表自然对数的底数。用三种方式计算 $e^2$：使用 `math.e` 和幂运算符（`**`）、使用 `math.pow`，以及使用 `math.exp`。
