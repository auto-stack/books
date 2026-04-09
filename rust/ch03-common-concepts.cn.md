# 通用编程概念

本章介绍几乎每种编程语言中都会出现的概念，以及它们在 Auto 中的工作方式。许多编程语言在核心层面有很多共同之处。本章介绍的概念都不是 Auto 独有的，但我们会在 Auto 的语境下讨论它们，并解释使用它们的惯例。

具体来说，你将学习变量、基本类型、函数、注释和控制流。这些基础知识会出现在每个 Auto 程序中，尽早学习它们将为你打下坚实的基础。

> #### 关键字
>
> Auto 语言有一组 _关键字_，仅供语言自身使用，与其他语言类似。请注意，你不能用这些词作为变量或函数的名称。大多数关键字都有特殊含义，你会在 Auto 程序中使用它们来完成各种任务。你可以在附录 A 中找到关键字列表。

## 变量与可变性

正如在第 2 章"用变量存储值"一节中提到的，默认情况下变量是不可变的。这是 Auto 引导你以更安全、更易并发的方式编写代码的手段之一。不过，你仍然可以选择让变量可变。让我们探讨 Auto 为什么鼓励你优先使用不可变性，以及为什么有时你可能需要选择可变。

当变量不可变时，一旦值绑定到一个名称，你就无法再改变它。为了演示这一点，创建一个名为 _variables_ 的新项目：

```console
$ automan new variables
$ cd variables
```

然后在新创建的 _variables_ 目录中，打开 _src/main.auto_ 并将代码替换为以下内容（这段代码暂时无法编译）：

<span class="filename">文件名：src/main.auto</span>

```auto,ignore,does_not_compile
fn main() ! {
    let x = 5
    println("The value of x is: " + x.to_string())
    x = 6
    println("The value of x is: " + x.to_string())
}
```

```rust,ignore,does_not_compile
fn main() {
    let x = 5;
    println!("The value of x is: {x}");
    x = 6;
    println!("The value of x is: {x}");
}
```

保存并使用 `automan run` 运行程序。你会收到一条错误消息：

```text
error: cannot assign twice to immutable variable `x`
```

这个例子展示了编译器如何帮助你发现程序中的错误。编译器错误可能令人沮丧，但它们只意味着你的程序还没有安全地完成你想做的事——并不代表你不是一个好程序员！

你收到了 `cannot assign twice to immutable variable x` 错误消息，因为你试图给不可变的 `x` 变量赋第二个值。

当我们尝试改变被指定为不可变的值时，能够在编译时得到错误是非常重要的，因为这种情况很容易导致 bug。如果代码的一部分假设某个值永远不会改变，而另一部分代码却改变了它，那么前一部分的代码可能无法按设计工作。Auto 编译器保证：当你声明一个值不会改变时，它就真的不会改变，所以你不需要自己去追踪。

但可变性可能非常有用，能让代码更方便编写。在 Auto 中，你使用 `var` 而不是 `let` 来创建可变变量。使用 `var` 也向未来的代码读者传达了意图，表明其他部分的代码会改变这个变量的值。

例如，将 _src/main.auto_ 改为：

<span class="filename">文件名：src/main.auto</span>

```auto
fn main() ! {
    var x = 5
    println("The value of x is: " + x.to_string())
    x = 6
    println("The value of x is: " + x.to_string())
}
```

```rust
fn main() {
    let mut x = 5;
    println!("The value of x is: {x}");
    x = 6;
    println!("The value of x is: {x}");
}
```

运行程序：

```console
$ automan run
   Compiling variables v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in 0.30s
     Running `target/debug/variables`
The value of x is: 5
The value of x is: 6
```

使用 `var` 后，我们可以将 `x` 的值从 `5` 改为 `6`。最终是否使用可变性取决于你，取决于你认为在特定情况下哪种方式更清晰。

### 声明常量

与不可变变量类似，_常量_ 是绑定到名称且不允许改变的值，但常量和变量之间有一些区别。

首先，你不能对常量使用 `var`。常量不仅仅是默认不可变——它们始终不可变。你使用 `const` 关键字而不是 `let` 来声明常量，并且 _必须_ 标注值的类型。

常量可以在任何作用域中声明，包括全局作用域，这使得它们对于代码中许多部分都需要了解的值非常有用。

最后一个区别是，常量只能设置为常量表达式，不能设置为只能在运行时计算的结果。

以下是常量声明的示例：

```auto
const THREE_HOURS_IN_SECONDS: int = 60 * 60 * 3
```

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

常量名为 `THREE_HOURS_IN_SECONDS`，其值设为 60（每分钟的秒数）乘以 60（每小时的分钟数）乘以 3（小时数）的结果。Auto 中常量的命名约定是全部大写，单词之间用下划线分隔。

### 遮蔽（Shadowing）

正如你在第 2 章的猜数字游戏教程中看到的，你可以声明一个与之前变量同名的新变量。我们说第一个变量被第二个变量 _遮蔽_ 了。实际上，第二个变量覆盖了第一个，将对变量名的所有使用都转移到自身，直到它自身被遮蔽或作用域结束。

在 Auto 中，我们可以通过重复使用 `let` 关键字和相同的变量名来遮蔽变量：

<span class="filename">文件名：src/main.auto</span>

```auto
fn main() ! {
    let x = 5
    let x = x + 1
    {
        let x = x * 2
        println("The value of x in the inner scope is: " + x.to_string())
    }
    println("The value of x is: " + x.to_string())
}
```

```rust
fn main() {
    let x = 5;
    let x = x + 1;
    {
        let x = x * 2;
        println!("The value of x in the inner scope is: {x}");
    }
    println!("The value of x is: {x}");
}
```

程序首先将 `x` 绑定到值 `5`。然后通过 `let x =` 创建新变量 `x`，将原值加 `1`，所以 `x` 的值变为 `6`。然后，在内部作用域中，第三个 `let` 遮蔽了 `x`，将之前的值乘以 `2`，使 `x` 的值变为 `12`。当该作用域结束后，内部遮蔽结束，`x` 回到 `6`。

遮蔽与使用 `var` 不同，因为如果我们不小心尝试在不使用 `let` 关键字的情况下重新赋值，会得到编译时错误。通过使用 `let`，我们可以对值执行一些转换，但在转换完成后变量是不可变的。

`var` 和遮蔽的另一个区别是，由于使用 `let` 关键字实际上是在创建一个新变量，我们可以改变值的类型但复用同一个名称：

```auto
let spaces = "   "
let spaces = spaces.length()
```

```rust
let spaces = "   ";
let spaces = spaces.len();
```

第一个 `spaces` 变量是字符串类型，第二个 `spaces` 变量是数字类型。遮蔽使我们免于想出不同的名称，如 `spaces_str` 和 `spaces_num`。

## 数据类型

Auto 中的每个值都属于某种 _数据类型_，它告诉 Auto 正在指定什么类型的数据，以便它知道如何处理这些数据。我们将了解两类数据类型：标量和复合。

请记住，Auto 是一门 _静态类型_ 语言，这意味着它必须在编译时知道所有变量的类型。编译器通常可以根据值和我们的使用方式来推断我们想用的类型。在多种类型都有可能的情况下，我们必须添加类型标注：

```auto
let guess: int = "42".to_int().expect("Not a number!")
```

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

### 标量类型

_标量_ 类型表示单个值。Auto 有四种主要标量类型：整数、浮点数、布尔值和字符。

#### 整数类型

_整数_ 是没有小数部分的数字。表 3-1 展示了 Auto 中的内置整数类型。

<span class="caption">表 3-1：Auto 中的整数类型</span>

| 长度  | 有符号  | 无符号 |
| ------- | ------- | -------- |
| 8 位   | `i8`    | `u8`     |
| 16 位  | `i16`   | `u16`    |
| 32 位  | `i32`   | `u32`    |
| 64 位  | `i64`   | `u64`    |
| 128 位 | `i128`  | `u128`   |
| 取决于架构 | `isize` | `usize`  |

_有符号_ 和 _无符号_ 指的是数字是否可能为负数。有符号数使用二进制补码表示存储。

你可以用表 3-2 中所示的任何格式编写整数字面量。

<span class="caption">表 3-2：Auto 中的整数字面量</span>

| 数字字面量  | 示例       |
| ---------------- | ------------- |
| 十进制          | `98_222`      |
| 十六进制              | `0xff`        |
| 八进制            | `0o77`        |
| 二进制           | `0b1111_0000` |
| 字节（仅 `u8`） | `b'A'`        |

数字字面量可以使用 `_` 作为视觉分隔符，使数字更易读，例如 `1_000`。默认整数类型是 `i32`。

> ##### 整数溢出
>
> 如果你试图将变量更改为超出其类型范围的值，就会发生 _整数溢出_。在调试模式下，Auto 会在运行时 panic。在发布模式下，Auto 执行二进制补码回绕。要显式处理溢出，Auto 提供了 `wrapping_add`、`checked_add` 和 `saturating_add` 等方法。

#### 浮点类型

Auto 有两种 _浮点数_ 的原始类型：`f32` 和 `f64`，分别为 32 位和 64 位大小。默认类型是 `f64`，因为在现代 CPU 上它的速度与 `f32` 大致相同，但精度更高。

<span class="filename">文件名：src/main.auto</span>

```auto
fn main() ! {
    let x = 2.0      // f64
    let y: f32 = 3.0 // f32
}
```

```rust
fn main() {
    let x = 2.0; // f64
    let y: f32 = 3.0; // f32
}
```

浮点数按照 IEEE-754 标准表示。

#### 数值运算

Auto 支持所有数字类型的基本数学运算：加法、减法、乘法、除法和取余。整数除法向零截断。

<span class="filename">文件名：src/main.auto</span>

```auto
fn main() ! {
    // 加法
    let sum = 5 + 10
    // 减法
    let difference = 95.5 - 4.3
    // 乘法
    let product = 4 * 30
    // 除法
    let quotient = 56.7 / 32.2
    // 取余
    let remainder = 43 % 5
}
```

```rust
fn main() {
    // 加法
    let sum = 5 + 10;
    // 减法
    let difference = 95.5 - 4.3;
    // 乘法
    let product = 4 * 30;
    // 除法
    let quotient = 56.7 / 32.2;
    // 取余
    let remainder = 43 % 5;
}
```

#### 布尔类型

Auto 中的布尔类型有两个可能的值：`true` 和 `false`。布尔值占一个字节。布尔类型用 `bool` 指定。

```auto
fn main() ! {
    let t = true
    let f: bool = false
}
```

```rust
fn main() {
    let t = true;
    let f: bool = false;
}
```

#### 字符类型

Auto 的 `char` 类型是语言中最基本的字母类型：

```auto
fn main() ! {
    let c = 'z'
    let z: char = 'Z'
    let heart_eyed_cat = '😻'
}
```

```rust
fn main() {
    let c = 'z';
    let z: char = 'Z';
    let heart_eyed_cat = '😻';
}
```

请注意，`char` 字面量使用单引号，而字符串字面量使用双引号。Auto 的 `char` 类型占 4 个字节，表示一个 Unicode 标量值。

### 复合类型

_复合类型_ 可以将多个值组合成一种类型。Auto 有两种原始复合类型：元组和数组。

#### 元组类型

_元组_ 是将多个具有不同类型的值组合成一种复合类型的通用方式。元组有固定长度：一旦声明，就不能增大或缩小。

<span class="filename">文件名：src/main.auto</span>

```auto
fn main() ! {
    let tup: (int, f64, bool) = (500, 6.4, true)
    let (x, y, z) = tup
    println("The value of y is: " + y.to_string())
}
```

```rust
fn main() {
    let tup: (i32, f64, bool) = (500, 6.4, true);
    let (x, y, z) = tup;
    println!("The value of y is: {y}");
}
```

我们还可以通过使用句点（`.`）后跟索引直接访问元组元素：

```auto
let five_hundred = tup.0
let six_point_four = tup.1
```

```rust
let five_hundred = tup.0;
let six_point_four = tup.1;
```

没有任何值的元组有一个特殊名称 _单元（unit）_，写作 `()`。表达式如果不返回任何其他值，会隐式返回单元值。

#### 数组类型

将多个值组合在一起的另一种方式是使用 _数组_。与元组不同，数组的每个元素必须是相同类型。Auto 中的数组有固定长度。

```auto
let a = [1, 2, 3, 4, 5]
```

```rust
let a = [1, 2, 3, 4, 5];
```

当你希望数据分配在栈上而不是堆上，或者当你想确保始终拥有固定数量的元素时，数组很有用。

你可以使用方括号、元素类型、分号和元素数量来编写数组的类型：

```auto
let a: [int; 5] = [1, 2, 3, 4, 5]
```

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

你也可以初始化数组，使每个元素都包含相同的值：

```auto
let a = [3; 5]  // 等同于 [3, 3, 3, 3, 3]
```

```rust
let a = [3; 5]; // 等同于 [3, 3, 3, 3, 3]
```

#### 数组元素访问

你可以使用索引访问数组元素：

```auto
let a = [1, 2, 3, 4, 5]
let first = a[0]
let second = a[1]
```

```rust
let a = [1, 2, 3, 4, 5];
let first = a[0];
let second = a[1];
```

#### 无效的数组元素访问

如果你试图访问数组末尾之后的元素，Auto 会在运行时 panic：

```console
thread 'main' panicked at src/main.auto:19:19:
index out of bounds: the len is 5 but the index is 10
```

这是 Auto 内存安全原则的一个实例。Auto 通过立即退出而不是允许访问无效内存并继续执行来保护你。

## 函数

函数在 Auto 代码中无处不在。你已经见过了语言中最重要的函数之一：`main` 函数，它是许多程序的入口。你也见过了 `fn` 关键字，它允许你声明新函数。

Auto 代码使用 _蛇形命名法（snake case）_ 作为函数和变量名的约定风格，即所有字母小写，单词之间用下划线分隔。

<span class="filename">文件名：src/main.auto</span>

```auto
fn main() ! {
    println("Hello, world!")
    another_function()
}

fn another_function() {
    println("Another function.")
}
```

```rust
fn main() {
    println!("Hello, world!");
    another_function();
}

fn another_function() {
    println!("Another function.");
}
```

请注意，我们在源代码中将 `another_function` 定义在 `main` 函数 _之后_；我们也可以把它定义在前面。Auto 不关心你在哪里定义函数，只关心它们定义在调用者能看到的作用域中的某个地方。

### 参数

我们可以为函数定义 _参数_，即函数签名中的特殊变量：

```auto
fn main() ! {
    another_function(5)
}

fn another_function(x: int) {
    println("The value of x is: " + x.to_string())
}
```

```rust
fn main() {
    another_function(5);
}

fn another_function(x: i32) {
    println!("The value of x is: {x}");
}
```

在函数签名中，你 _必须_ 声明每个参数的类型。这是 Auto 设计中的一个深思熟虑的决定：在函数定义中要求类型标注意味着编译器几乎不需要你在代码的其他地方使用它们来判断你想要什么类型。

定义多个参数时，用逗号分隔参数声明：

```auto
fn print_labeled_measurement(value: int, unit_label: char) {
    println("The value is: " + value.to_string() + unit_label)
}
```

```rust
fn print_labeled_measurement(value: i32, unit_label: char) {
    println!("The value is: {value}{unit_label}");
}
```

### 语句和表达式

函数体由一系列语句组成，可以选择以一个表达式结尾。因为 Auto 是一门基于表达式的语言，所以这是一个需要理解的重要区别。

- _语句_ 执行某些操作但不返回值。
- _表达式_ 求值为一个结果值。

使用 `let` 创建变量并赋值是语句。函数定义也是语句。语句不返回值。因此，你不能将 `let` 语句赋给另一个变量。

表达式求值为一个值，构成了你将在 Auto 中编写的大部分代码。用花括号创建的新作用域块就是一个表达式：

```auto
fn main() ! {
    let y = {
        let x = 3
        x + 1
    }
    println("The value of y is: " + y.to_string())
}
```

```rust
fn main() {
    let y = {
        let x = 3;
        x + 1
    };
    println!("The value of y is: {y}");
}
```

该块求值为 `4`。这个值作为 `let` 语句的一部分绑定到 `y`。注意 `x + 1` 行末尾没有分号——表达式不包含结尾分号。如果在表达式末尾加分号，它就变成了语句，也就不会返回值了。

注意，在 Auto 中，大多数地方的分号是可选的。编译器通过换行和上下文来确定语句的结束位置。但是，在返回值的块表达式中，不应在最终表达式后加分号。

### 有返回值的函数

函数可以向调用它的代码返回值。我们不命名返回值，但必须在箭头（`->`）后声明其类型。在 Auto 中，函数的返回值等同于函数体块中最后一个表达式的值。你可以使用 `return` 关键字提前返回，但大多数函数隐式返回最后一个表达式。

<span class="filename">文件名：src/main.auto</span>

```auto
fn five() -> int {
    5
}

fn main() ! {
    let x = five()
    println("The value of x is: " + x.to_string())
}
```

```rust
fn five() -> i32 {
    5
}

fn main() {
    let x = five();
    println!("The value of x is: {x}");
}
```

`five` 函数中没有函数调用、宏甚至 `let` 语句——只有数字 `5` 本身。这在 Auto 中是完全有效的函数。`5` 是函数的返回值，因为它是最终表达式。

再看一个例子：

```auto
fn plus_one(x: int) -> int {
    x + 1
}
```

```rust
fn plus_one(x: i32) -> i32 {
    x + 1
}
```

## 注释

所有程序员都努力使代码易于理解，但有时需要额外的解释。在这些情况下，程序员会在源代码中留下 _注释_，编译器会忽略它们，但阅读源代码的人可能会觉得有用。

以下是一个简单的注释：

```auto
// hello, world
```

在 Auto 中，注释以两个斜杠开头，持续到行尾。对于跨多行的注释，你需要在每行都包含 `//`：

```auto
// 我们在这里做了一些复杂的事情，足够长以至于需要
// 多行注释来解释！呼！希望这些注释能解释清楚。
```

注释也可以放在包含代码的行的末尾：

```auto
let x = 5 // 这也是注释
```

Auto 还有文档注释，我们将在第 14 章讨论。

## 控制流

根据条件是否为 `true` 来运行某些代码，以及在条件为 `true` 时重复运行某些代码的能力，是大多数编程语言的基本构建块。Auto 中最常见的控制执行流的构造是 `if` 表达式和循环。

### `if` 表达式

`if` 表达式允许你根据条件分支代码：

<span class="filename">文件名：src/main.auto</span>

```auto
fn main() ! {
    let number = 3
    if number < 5 {
        println("condition was true")
    } else {
        println("condition was false")
    }
}
```

```rust
fn main() {
    let number = 3;
    if number < 5 {
        println!("condition was true");
    } else {
        println!("condition was false");
    }
}
```

所有 `if` 表达式都以关键字 `if` 开头，后跟一个条件。条件 _必须_ 是 `bool`。Auto 不会自动尝试将非布尔类型转换为布尔值。

#### 使用 `else if` 处理多个条件

你可以通过在 `else if` 表达式中组合 `if` 和 `else` 来使用多个条件：

```auto
let number = 6

if number % 4 == 0 {
    println("number is divisible by 4")
} else if number % 3 == 0 {
    println("number is divisible by 3")
} else if number % 2 == 0 {
    println("number is divisible by 2")
} else {
    println("number is not divisible by 4, 3, or 2")
}
```

```rust
let number = 6;

if number % 4 == 0 {
    println!("number is divisible by 4");
} else if number % 3 == 0 {
    println!("number is divisible by 3");
} else if number % 2 == 0 {
    println!("number is divisible by 2");
} else {
    println!("number is not divisible by 4, 3, or 2");
}
```

使用过多的 `else if` 表达式会使代码变得杂乱。第 6 章将介绍 Auto 的 `is` 关键字用于模式匹配，对于这种情况是更强大的分支构造。

#### 在 `let` 语句中使用 `if`

因为 `if` 是表达式，我们可以把它用在 `let` 语句的右侧：

```auto
let condition = true
let number = if condition { 5 } else { 6 }
```

```rust
let condition = true;
let number = if condition { 5 } else { 6 };
```

`if` 各分支可能产生的结果值必须是相同类型。

### 通过循环实现重复

多次执行代码块通常很有用。Auto 提供了几种 _循环_：`loop`、`while` 和 `for`。

#### 使用 `loop` 重复代码

`loop` 关键字让 Auto 反复执行代码块，直到你明确告诉它停止：

```auto
fn main() ! {
    loop {
        println("again!")
    }
}
```

```rust
fn main() {
    loop {
        println!("again!");
    }
}
```

你可以在循环内使用 `break` 关键字告诉程序何时停止执行。我们还使用过 `continue`，它告诉程序跳过当前迭代中剩余的代码，进入下一次迭代。

#### 从循环返回值

你可以在 `break` 表达式后添加想要返回的值：

```auto
fn main() ! {
    var counter = 0
    let result = loop {
        counter += 1
        if counter == 10 {
            break counter * 2
        }
    }
    println("The result is " + result.to_string())
}
```

```rust
fn main() {
    let mut counter = 0;
    let result = loop {
        counter += 1;
        if counter == 10 {
            break counter * 2;
        }
    };
    println!("The result is {result}");
}
```

#### 循环标签

如果你有嵌套循环，`break` 和 `continue` 默认应用于最内层循环。你可以选择指定 _循环标签_ 来消除歧义：

```auto
'counting_up: loop {
    println("count = " + count.to_string())
    var remaining = 10
    loop {
        println("remaining = " + remaining.to_string())
        if remaining == 9 {
            break
        }
        if count == 2 {
            break 'counting_up
        }
        remaining -= 1
    }
    count += 1
}
```

#### 使用 `while` 的条件循环

程序通常需要在循环中评估条件。`while` 循环是为此目的内置的构造：

```auto
var number = 3
while number != 0 {
    println(number.to_string() + "!")
    number -= 1
}
println("LIFTOFF!!!")
```

```rust
let mut number = 3;
while number != 0 {
    println!("{number}!");
    number -= 1;
}
println!("LIFTOFF!!!");
```

#### 使用 `for` 遍历集合

你可以使用 `for` 循环迭代集合中的元素：

```auto
let a = [10, 20, 30, 40, 50]
for element in a {
    println("the value is: " + element.to_string())
}
```

```rust
let a = [10, 20, 30, 40, 50];
for element in a {
    println!("the value is: {element}");
}
```

`for` 循环的安全性和简洁性使其成为 Auto 中最常用的循环构造。即使你想运行代码固定次数，大多数 Auto 开发者也会使用带范围的 `for` 循环：

```auto
for number in (1..4).rev() {
    println(number.to_string() + "!")
}
println("LIFTOFF!!!")
```

```rust
for number in (1..4).rev() {
    println!("{number}!");
}
println!("LIFTOFF!!!");
```

## 总结

恭喜！本章内容相当多：你学习了变量、标量和复合数据类型、函数、注释、`if` 表达式和循环！要练习本章讨论的概念，试着编写以下程序：

- 在华氏度和摄氏度之间转换温度。
- 生成第 *n* 个斐波那契数。
- 打印圣诞颂歌"The Twelve Days of Christmas"的歌词，利用歌曲中的重复部分。

准备好了之后，我们将讨论 Auto 中一个在其他编程语言中 _不_ 常见的概念：内存模型。
