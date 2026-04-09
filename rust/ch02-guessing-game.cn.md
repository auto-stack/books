# 编写猜数字游戏

让我们通过一个动手项目来开始学习 Auto！本章通过展示如何在实际程序中使用它们，来介绍一些常见的 Auto 概念。你将学习 `let`、`var`、`is` 关键字、方法、外部包等等！在接下来的章节中，我们会更详细地探讨这些概念。本章只是练习基础内容。

我们将实现一个经典的编程入门问题：猜数字游戏。游戏规则如下：程序生成一个 1 到 100 之间的随机整数，然后提示玩家输入猜测值。输入猜测后，程序会提示猜测值是太小还是太大。如果猜对了，游戏会打印祝贺信息并退出。

## 创建新项目

要创建新项目，进入你在第 1 章中创建的 _projects_ 目录，然后使用 automan 创建一个新项目：

```console
$ automan new guessing_game
$ cd guessing_game
```

第一条命令 `automan new` 以项目名称（`guessing_game`）作为第一个参数。第二条命令进入新项目的目录。

查看生成的 _auto.toml_ 文件：

<span class="filename">文件名：auto.toml</span>

```toml
[package]
name = "guessing_game"
version = "0.1.0"

[dependencies]
```

正如你在第 1 章中看到的，`automan new` 为你生成了一个 "Hello, world!" 程序。查看 _src/main.auto_ 文件：

<span class="filename">文件名：src/main.auto</span>

```auto
fn main() ! {
    print("Hello, world!")
}
```

```rust
fn main() {
    println!("Hello, world!");
}
```

现在让我们用 `automan run` 命令一步完成编译和运行：

```console
$ automan run
   Compiling guessing_game v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in 2.85s
     Running `target/debug/guessing_game`
Hello, world!
```

重新打开 _src/main.auto_ 文件。你将在这个文件中编写所有代码。

## 处理猜测

猜数字游戏的第一部分将要求用户输入、处理输入，并检查输入是否符合预期格式。首先，我们让玩家输入一个猜测值。将代码清单 2-1 中的代码输入 _src/main.auto_。

<Listing number="2-1" file-name="src/main.auto" caption="获取用户猜测并打印的代码">

```auto
use io

fn main() ! {
    println("Guess the number!")
    println("Please input your guess.")

    var guess = ""
    io.read_line(guess)
        .expect("Failed to read line")

    println("You guessed: " + guess)
}
```

```rust
use std::io;

fn main() {
    println!("Guess the number!");

    println!("Please input your guess.");

    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");

    println!("You guessed: {guess}");
}
```

</Listing>

这段代码包含很多信息，让我们逐行分析。为了获取用户输入并打印结果，我们需要将 `io` 输入/输出库引入作用域。`io` 库来自标准库：

```auto
use io
```

默认情况下，Auto 会将标准库中定义的一组项引入每个程序的作用域。这组项称为 _prelude_（预导入）。如果你想使用的类型不在 prelude 中，就需要用 `use` 语句显式引入。使用 `io` 库可以提供很多有用的功能，包括接受用户输入。

正如你在第 1 章中看到的，`main` 函数是程序的入口：

```auto
fn main() ! {
```

`fn` 语法声明一个新函数；括号 `()` 表示没有参数；`!` 表示错误传播；花括号 `{` 开始函数体。

### 用变量存储值

接下来，我们创建一个 _变量_ 来存储用户输入：

```auto
var guess = ""
```

程序开始变得有趣了！我们使用 `var` 创建一个可变变量。在 Auto 中，`let` 创建不可变绑定，`var` 创建可变绑定。这里需要用 `var`，因为 `read_line` 函数会通过追加用户输入来修改 `guess`。

我们将 `guess` 初始化为空字符串 `""`。Auto 中字符串字面量是 UTF-8 编码的，编译器可以据此推断出 `guess` 是 `String` 类型。

### 接收用户输入

现在我们调用 `io` 模块中的 `read_line` 函数来处理用户输入：

```auto
io.read_line(guess)
    .expect("Failed to read line")
```

我们调用 `io.read_line`，传入 `guess` 作为参数，告诉它将用户输入存储到哪个字符串中。`read_line` 的完整功能是获取用户在标准输入中输入的所有内容，并追加到字符串中（不会覆盖原有内容）。

### 用 `!T` 处理潜在失败

我们还在处理上面那行代码。`read_line` 函数会返回一个表示操作成功或失败的结果。在 Auto 中，我们用 `.expect()` 方法来处理：

```auto
.expect("Failed to read line")
```

如果 `read_line` 遇到错误，`expect` 会导致程序崩溃并显示你传入的消息。如果操作成功，`expect` 会返回结果值供你使用。

> Auto 使用 `!T` 进行错误处理的完整细节将在第 9 章介绍。现在只需知道 `expect` 是一种表示"出问题就崩溃"的方式。

### 打印值

除了右花括号，目前代码中只有一行需要讨论：

```auto
println("You guessed: " + guess)
```

这行打印现在包含用户输入的字符串。Auto 使用 `+` 运算符进行字符串拼接。你也可以使用 `{}` 进行字符串插值：

```auto
let x = 5
let y = 10
println("x = {x} and y + 2 = {y + 2}")
```

这会打印 `x = 5 and y + 2 = 12`。

### 测试第一部分

让我们测试猜数字游戏的第一部分。使用 `automan run` 运行：

```console
$ automan run
   Compiling guessing_game v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Guess the number!
Please input your guess.
6
You guessed: 6
```

至此，游戏的第一部分完成了：我们从键盘获取输入并打印出来。

## 生成秘密数字

接下来，我们需要生成一个让用户来猜的秘密数字。秘密数字每次都应该不同，这样游戏才能多次游玩。我们使用 1 到 100 之间的随机数，这样游戏不会太难。

### 使用外部包

记住，包是一组源代码文件的集合。我们一直在构建的项目是一个二进制包（可执行文件）。我们将使用一个外部库包来生成随机数。

automan 对外部包的协调管理是它真正出彩的地方。在编写使用随机数的代码之前，我们需要修改 _auto.toml_ 文件，将 `random` 包添加为依赖。打开该文件，在 `[dependencies]` 节标题下面添加以下内容：

<span class="filename">文件名：auto.toml</span>

```toml
[dependencies]
random = "0.8.5"
```

在 _auto.toml_ 文件中，标题后面的所有内容都属于该节，直到下一个节开始。在 `[dependencies]` 中，你告诉 automan 你的项目依赖哪些外部包以及需要什么版本。

现在，在不修改代码的情况下，构建项目：

```console
$ automan build
   Updating registry index
    Adding random v0.8.5
   Compiling random v0.8.5
   Compiling guessing_game v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in 2.48s
```

当我们引入外部依赖时，automan 会从包注册表中获取该依赖所需的所有内容。

#### 确保可复现的构建

automan 有一种机制确保每次都能构建出相同的产物：_auto.lock_ 文件。当你第一次构建项目时，automan 会确定所有符合条件的依赖版本，然后将它们写入 _auto.lock_ 文件。以后构建项目时，automan 会看到 _auto.lock_ 文件已存在，并使用其中指定的版本。这让你自动拥有可复现的构建。

#### 更新包到新版本

当你确实想更新包时，automan 提供了 `update` 命令，它会忽略 _auto.lock_ 文件，根据 _auto.toml_ 中的规格重新确定最新版本：

```console
$ automan update
    Updating registry index
    Updating random v0.8.5 -> v0.8.6
```

### 生成随机数

让我们开始使用 `random` 来生成要猜的数字。下一步是更新 _src/main.auto_，如代码清单 2-3 所示。

<Listing number="2-3" file-name="src/main.auto" caption="添加生成随机数的代码">

```auto
use io
use random

fn main() ! {
    println("Guess the number!")

    let secret_number = random.int(1, 100)

    println("The secret number is: " + secret_number.to_string())

    println("Please input your guess.")

    var guess = ""
    io.read_line(guess)
        .expect("Failed to read line")

    println("You guessed: " + guess)
}
```

```rust
use std::io;
use rand::Rng;

fn main() {
    println!("Guess the number!");

    let secret_number = rand::thread_rng().gen_range(1..=100);

    println!("The secret number is: {secret_number}");

    println!("Please input your guess.");

    let mut guess = String::new();

    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");

    println!("You guessed: {guess}");
}
```

</Listing>

首先，我们添加 `use random`。然后在中间添加两行：调用 `random.int(1, 100)` 生成 1 到 100 之间的随机整数，并用 `let` 将其绑定到 `secret_number`（因为它不会改变）。第二行打印秘密数字以供调试——我们会在最终版本中删除它。

试着运行几次程序：

```console
$ automan run
   Compiling guessing_game v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 7
Please input your guess.
4
You guessed: 4

$ automan run
    Finished dev [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 83
Please input your guess.
5
You guessed: 5
```

你应该会得到不同的随机数，且都是 1 到 100 之间的数字。太棒了！

## 比较猜测与秘密数字

现在我们有了用户输入和随机数，可以比较它们了。如代码清单 2-4 所示。注意这段代码暂时还无法编译，我们稍后会解释原因。

<Listing number="2-4" file-name="src/main.auto" caption="处理比较两个数字的可能返回值">

```auto
use io
use random

fn main() ! {
    println("Guess the number!")
    let secret_number = random.int(1, 100)
    println("The secret number is: " + secret_number.to_string())
    println("Please input your guess.")

    var guess = ""
    io.read_line(guess)
        .expect("Failed to read line")

    println("You guessed: " + guess)

    guess is Ordering.Less -> println("Too small!")
    guess is Ordering.Greater -> println("Too big!")
    guess is Ordering.Equal -> println("You win!")
}
```

```rust
use std::cmp::Ordering;
use std::io;
use rand::Rng;

fn main() {
    // --snip--
    println!("Guess the number!");
    let secret_number = rand::thread_rng().gen_range(1..=100);
    println!("The secret number is: {secret_number}");
    println!("Please input your guess.");

    let mut guess = String::new();
    io::stdin()
        .read_line(&mut guess)
        .expect("Failed to read line");
    println!("You guessed: {guess}");

    match guess.cmp(&secret_number) {
        Ordering::Less => println!("Too small!"),
        Ordering::Greater => println!("Too big!"),
        Ordering::Equal => println!("You win!"),
    }
}
```

</Listing>

这里我们使用了 `is` 关键字，这是 Auto 的模式匹配机制。`is` 关键字让你可以将值与模式进行比较，并根据匹配到的模式执行相应代码。这类似于 Rust 的 `match` 表达式。

但是，代码清单 2-4 的代码暂时还无法编译。错误的核心是 _类型不匹配_。`guess` 是字符串，而 `secret_number` 是数字类型。我们需要先将字符串输入转换为数字。

### 将字符串转换为数字

我们通过添加以下代码来解决：

```auto
let guess = guess.trim().to_int().expect("Please type a number!")
```

我们创建了一个同名的新变量 `guess`。Auto 允许 _遮蔽（shadowing）_——用新值复用同一个变量名。这通常用于将值从一种类型转换为另一种类型。

我们调用 `.trim()` 去除任何空白字符（包括按回车产生的换行符），然后调用 `.to_int()` 将字符串转换为整数。如果转换失败（例如用户输入了 "hello"），`expect` 会用我们的消息使程序崩溃。

我们也可以显式标注类型，告诉编译器我们需要整数：

```auto
let guess: int = guess.trim().to_int().expect("Please type a number!")
```

现在运行程序：

```console
$ automan run
   Compiling guessing_game v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 58
Please input your guess.
  76
You guessed: 76
Too big!
```

很好！即使猜测值前面加了空格，程序仍然正确识别出用户猜了 76。

游戏的大部分功能已经完成，但用户只能猜一次。让我们添加循环来改变这一点！

## 通过循环允许多次猜测

`loop` 关键字创建无限循环。我们添加循环来给用户更多猜数字的机会：

<span class="filename">文件名：src/main.auto</span>

```auto
// --snip--
    loop {
        println("Please input your guess.")

        var guess = ""
        io.read_line(guess)
            .expect("Failed to read line")

        let guess: int = guess.trim().to_int().expect("Please type a number!")

        println("You guessed: " + guess.to_string())

        guess is Ordering.Less -> println("Too small!")
        guess is Ordering.Greater -> println("Too big!")
        guess is Ordering.Equal -> println("You win!")
    }
```

如你所见，我们把猜测输入提示之后的所有内容都放到了循环中。程序现在会永远要求再次猜测，这实际上带来了一个新问题——用户似乎无法退出！

用户随时可以使用键盘快捷键 <kbd>ctrl</kbd>-<kbd>c</kbd> 中断程序。但还有另一种方式：如果用户输入了非数字，程序会通过 `expect` 崩溃。我们可以利用这一点让用户退出——但这并不理想。让我们同时解决这两个问题。

### 猜对后退出

让我们通过添加 `break` 语句，使游戏在用户获胜时退出：

```auto
        guess is Ordering.Equal -> {
            println("You win!")
            break
        }
```

在 "You win!" 之后添加 `break`，使用户在猜对秘密数字时退出循环。退出循环也意味着退出程序，因为循环是 `main` 的最后部分。

### 处理无效输入

为了进一步完善游戏行为，与其在用户输入非数字时崩溃，不如让游戏忽略非数字输入，以便用户可以继续猜测。我们可以通过修改将 `guess` 从字符串转换为整数的那行代码来实现，如代码清单 2-5 所示。

<Listing number="2-5" file-name="src/main.auto" caption="忽略非数字猜测并要求重新输入，而不是崩溃">

```auto
let guess: int = guess.trim().to_int() is
    Ok(num) -> num
    Err(_) -> continue
```

```rust
let guess: u32 = match guess.trim().parse() {
    Ok(num) => num,
    Err(_) => continue,
};
```

</Listing>

我们将 `expect` 调用改为 `is` 表达式，从遇到错误就崩溃改为优雅地处理错误。`.to_int()` 方法返回一个表示成功或失败的结果。我们用 `is` 来匹配结果：

- 如果转换成功，返回 `Ok(num)`，我们提取出数字。
- 如果转换失败，返回 `Err(_)`，我们使用 `continue` 跳到循环的下一次迭代，要求重新输入。

现在程序应该完全按预期工作了。试试看：

```console
$ automan run
   Compiling guessing_game v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 61
Please input your guess.
10
You guessed: 10
Too small!
Please input your guess.
99
You guessed: 99
Too big!
Please input your guess.
foo
Please input your guess.
61
You guessed: 61
You win!
```

太棒了！再做最后一个小调整，我们就能完成猜数字游戏了。回想一下，程序仍然在打印秘密数字。这在测试时很有用，但会破坏游戏体验。让我们删除打印秘密数字的那行代码。代码清单 2-6 展示了最终代码。

<Listing number="2-6" file-name="src/main.auto" caption="完整的猜数字游戏代码">

```auto
use io
use random

fn main() ! {
    println("Guess the number!")
    let secret_number = random.int(1, 100)

    loop {
        println("Please input your guess.")

        var guess = ""
        io.read_line(guess)
            .expect("Failed to read line")

        let guess: int = guess.trim().to_int() is
            Ok(num) -> num
            Err(_) -> continue

        println("You guessed: " + guess.to_string())

        guess.cmp(secret_number) is
            Ordering.Less -> println("Too small!")
            Ordering.Greater -> println("Too big!")
            Ordering.Equal -> {
                println("You win!")
                break
            }
    }
}
```

```rust
use std::cmp::Ordering;
use std::io;
use rand::Rng;

fn main() {
    println!("Guess the number!");
    let secret_number = rand::thread_rng().gen_range(1..=100);

    loop {
        println!("Please input your guess.");

        let mut guess = String::new();

        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read line");

        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        println!("You guessed: {guess}");

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
```

</Listing>

至此，你已经成功构建了猜数字游戏。恭喜！

## 总结

这个项目通过实践的方式向你介绍了许多新的 Auto 概念：`let`、`var`、`is`、函数、外部包的使用等等。在接下来的几章中，你将更详细地学习这些概念。第 3 章介绍大多数编程语言都有的概念，如变量、数据类型和函数，并展示如何在 Auto 中使用它们。第 4 章探索 Auto 的内存模型。第 5 章讨论 `type` 关键字和方法语法，第 6 章解释枚举的工作原理。
