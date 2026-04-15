# 函数与接口

在本章中，我们将使用函数绘制基于文本的图形，并演示**接口设计**（interface design）——一种让函数协同工作的设计方法。在此过程中，我们将学习封装、泛化和重构——软件开发中三个最重要的概念。

## 用字符画图

我们不使用图形化的海龟，而是用 `*` 和 `#` 等字符在终端中绘制图形。这种方法有一个优点：我们可以在不需要图形库的情况下，看到相同的设计原则——封装、泛化和重构。

例如，下面是一个用星号组成的简单"正方形"：

```
*****
*****
*****
*****
*****
```

我们可以用一个 `for` 循环重复打印一行字符来绘制它：

```auto
for i in 0..5 {
    print("*" * 5)
}
```

在继续之前，看看你能否修改这个程序来绘制一个 3 行 7 列的矩形。

## 封装

让我们把绘制重复图案的代码放到一个函数中。

<Listing number="4-1" file-name="encapsulation.auto" caption="封装：将重复代码包装在函数中">

```auto
fn print_banner(text: str) {
    let border = "=" * (text.len() + 4)
    print(border)
    print("= $text =")
    print(border)
}

fn main() {
    // 封装之前：重复的代码
    print("=========")
    print("= Hello =")
    print("=========")
    print()
    print("===========")
    print("= Welcome =")
    print("===========")
    print()
    print("========")
    print("= Bye =")
    print("========")

    print()

    // 封装之后：调用函数
    print_banner("Hello")
    print()
    print_banner("Welcome")
    print()
    print_banner("Bye")
}
```

```python
def print_banner(text):
    border = "=" * (len(text) + 4)
    print(border)
    print(f"= {text} =")
    print(border)


def main():
    # 封装之前：重复的代码
    print("=========")
    print("= Hello =")
    print("=========")
    print()
    print("===========")
    print("= Welcome =")
    print("===========")
    print()
    print("========")
    print("= Bye =")
    print("========")

    print()

    # 封装之后：调用函数
    print_banner("Hello")
    print()
    print_banner("Welcome")
    print()
    print_banner("Bye")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

"封装之前"部分展示了三个代码块，每个块都打印一个围绕单词的横幅。三个代码块几乎完全相同——只有单词不同。"封装之后"部分定义了 `print_banner`，它接受 `text` 作为参数，并使用 `text.len() + 4` 动态计算边框长度。现在我们可以用任意单词调用 `print_banner`，获得适当大小的横幅。

将一段代码包装在函数中称为**封装**（encapsulation）。封装的好处之一是它为代码赋予了一个名称，起到了文档的作用。另一个好处是，如果重用代码，调用两次函数比复制粘贴函数体要简洁得多！

## 泛化

下一步是给我们的绘图函数添加参数，使它们更加通用。

<Listing number="4-2" file-name="generalization.auto" caption="泛化：添加参数使函数可复用">

```auto
// 绘制一行重复的字符
fn draw_row(ch: str, width: int) {
    print(ch * width)
}

// 绘制指定宽度和高度的空心方框
fn draw_box(ch: str, width: int, height: int) {
    draw_row(ch, width)
    for i in 0..(height - 2) {
        print("$ch" + " " * (width - 2) + "$ch")
    }
    if height > 1 {
        draw_row(ch, width)
    }
}

// 在更宽的画布中绘制居中的方框
fn draw_centered_box(ch: str, width: int, height: int, canvas_width: int) {
    let padding = (canvas_width - width) / 2
    for i in 0..height {
        print(" " * padding + draw_row_str(ch, width))
    }
}

// 辅助函数：返回一行字符串但不打印
fn draw_row_str(ch: str, width: int) -> str {
    ch * width
}

fn main() {
    // 简单的行
    print("Simple row:")
    draw_row("*", 10)
    print()

    // 方框
    print("Box 5x3:")
    draw_box("#", 5, 3)
    print()

    // 在更宽画布上居中的方框
    print("Centered box 7x3 on canvas of 15:")
    draw_centered_box("+", 7, 3, 15)
}
```

```python
def draw_row(ch, width):
    print(ch * width)


def draw_box(ch, width, height):
    draw_row(ch, width)
    for i in range(height - 2):
        print(f"{ch}" + " " * (width - 2) + f"{ch}")
    if height > 1:
        draw_row(ch, width)


def draw_centered_box(ch, width, height, canvas_width):
    padding = (canvas_width - width) // 2
    for i in range(height):
        print(" " * padding + draw_row_str(ch, width))


def draw_row_str(ch, width):
    return ch * width


def main():
    # 简单的行
    print("Simple row:")
    draw_row("*", 10)
    print()

    # 方框
    print("Box 5x3:")
    draw_box("#", 5, 3)
    print()

    # 在更宽画布上居中的方框
    print("Centered box 7x3 on canvas of 15:")
    draw_centered_box("+", 7, 3, 15)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`draw_row` 接受一个字符 `ch` 和一个 `width`，打印一行。`draw_box` 调用 `draw_row` 绘制上下边框，中间部分用空格填充。`draw_centered_box` 增加了 `canvas_width` 参数，将方框居中在更宽的行中。

给函数添加参数称为**泛化**（generalization），因为它使函数更加通用：固定大小时只能绘制一种图形；有了参数，就能绘制许多种。

当一个函数有多个数字参数时，很容易忘记它们是什么，或者它们应该按什么顺序排列。在 Auto 中，你可以使用命名参数使调用更清晰：

```auto
draw_centered_box(ch="+", width=7, height=3, canvas_width=15)
```

赋值运算符 `=` 的这种用法提醒了我们参数的工作方式——当你调用函数时，参数被赋给参数名。

## 重构

现在假设我们既想要实心方框又想要空心方框。我们可以写两个独立的函数，但它们会共享很多相同的逻辑。更好的方法是重构。

<Listing number="4-3" file-name="refactoring.auto" caption="重构：简化并消除重复">

```auto
// --- 重构之前：重复的逻辑 ---

fn draw_filled_box(ch: str, width: int, height: int) {
    for i in 0..height {
        for j in 0..width {
            print(ch, terminator: "")
        }
        print()
    }
}

fn draw_empty_box(ch: str, width: int, height: int) {
    for i in 0..height {
        for j in 0..width {
            if i == 0 || i == height - 1 || j == 0 || j == width - 1 {
                print(ch, terminator: "")
            } else {
                print(" ", terminator: "")
            }
        }
        print()
    }
}

// --- 重构之后：共享的辅助函数 ---

// 辅助函数：返回一行字符串
fn make_row(ch: str, fill: str, width: int, is_edge: bool) -> str {
    if is_edge {
        ch * width
    } else {
        "$ch" + fill * (width - 2) + "$ch"
    }
}

fn draw_box_v2(ch: str, width: int, height: int, filled: bool) {
    let fill = if filled { ch } else { " " }
    for i in 0..height {
        let is_edge = i == 0 || i == height - 1
        print(make_row(ch, fill, width, is_edge))
    }
}

fn main() {
    // 重构之前：两个独立的函数
    print("Filled box 5x3:")
    draw_filled_box("*", 5, 3)
    print()

    print("Empty box 5x3:")
    draw_empty_box("#", 5, 3)
    print()

    // 重构之后：一个带参数的函数
    print("Filled box 5x3 (v2):")
    draw_box_v2("*", 5, 3, true)
    print()

    print("Empty box 5x3 (v2):")
    draw_box_v2("#", 5, 3, false)
}
```

```python
def draw_filled_box(ch, width, height):
    for i in range(height):
        for j in range(width):
            print(ch, end="")
        print()


def draw_empty_box(ch, width, height):
    for i in range(height):
        for j in range(width):
            if i == 0 or i == height - 1 or j == 0 or j == width - 1:
                print(ch, end="")
            else:
                print(" ", end="")
        print()


def make_row(ch, fill, width, is_edge):
    if is_edge:
        return ch * width
    else:
        return f"{ch}" + fill * (width - 2) + f"{ch}"


def draw_box_v2(ch, width, height, filled):
    fill = ch if filled else " "
    for i in range(height):
        is_edge = i == 0 or i == height - 1
        print(make_row(ch, fill, width, is_edge))


def main():
    # 重构之前：两个独立的函数
    print("Filled box 5x3:")
    draw_filled_box("*", 5, 3)
    print()

    print("Empty box 5x3:")
    draw_empty_box("#", 5, 3)
    print()

    # 重构之后：一个带参数的函数
    print("Filled box 5x3 (v2):")
    draw_box_v2("*", 5, 3, True)
    print()

    print("Empty box 5x3 (v2):")
    draw_box_v2("#", 5, 3, False)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

"重构之前"部分有两个函数：`draw_filled_box` 使用嵌套的 `for` 循环将每个单元格打印为 `ch`，而 `draw_empty_box` 使用条件判断来决定是打印 `ch` 还是空格。两个函数共享相同的外层循环结构。

"重构之后"部分提取了一个辅助函数 `make_row`，它将一行构建为字符串。`draw_box_v2` 使用 `make_row` 并添加了 `filled` 参数。如果 `filled` 为 `true`，填充字符为 `ch`（与边框相同）；如果为 `false`，填充为空格。现在一个函数就能处理两种情况。

这种在不改变行为的情况下改进代码的修改称为**重构**（refactoring）。如果我们事先规划好了，可能一开始就会写 `make_row`，从而避免重构，但在项目开始时，你往往不了解足够的信息来设计所有函数。一旦开始编码，你对问题的理解就更深入了。有时候重构说明你学到了新东西。

## 开发计划

**开发计划**（development plan）是一种编写程序的过程。我们在本章中使用的流程是"封装和泛化"。步骤如下：

1. 首先编写一个没有函数定义的小程序。
2. 程序可以运行后，识别其中一段有逻辑的代码，将其封装在函数中并命名。
3. 通过添加适当的参数来泛化函数。
4. 重复步骤 1 到 3，直到拥有一组可工作的函数。
5. 寻找通过重构来改进程序的机会。例如，如果在多个地方有相似的代码，考虑将其提取到一个适当通用的函数中。

这个过程有一些缺点——我们稍后会看到替代方案——但如果你事先不知道如何将程序划分为函数，它会很有用。这种方法让你可以边做边设计。

函数的设计有两个部分：

* **接口**（interface）是函数的使用方式，包括它的名称、它接受的参数以及函数应该做什么。
* **实现**（implementation）是函数如何完成它应该做的事情。

例如，`draw_box` 的"重构之前"和"重构之后"版本具有相同的接口——它们接受相同的参数并产生相同的输出——但有不同的实现。

## 文档字符串

**文档字符串**（docstring）是函数开头的注释，用于解释接口（"doc"是"documentation"的缩写）。Auto 使用 `//` 表示注释，你可以在每一行使用 `//` 来编写多行文档字符串：

```auto
// 绘制一行重复的字符。
// ch: 要重复的字符
// width: 字符的宽度
fn draw_row(ch: str, width: int) {
    print(ch * width)
}
```

文档字符串应该：

* 简明地解释函数的功能，而不涉及它如何工作的细节，
* 解释每个参数对函数行为的影响，以及
* 在不明显的情况下，指明每个参数应该是什么类型。

编写这种文档是接口设计的重要组成部分。设计良好的接口应该易于解释；如果你很难解释你的某个函数，也许接口可以改进。

## 栈图

当 `draw_box` 调用 `draw_row` 时，我们可以用栈图来展示这个函数调用序列以及每个函数的参数。以下是 `draw_box("#", 5, 3)` 调用 `draw_row("#", 5)` 时的文本表示：

```
+-----------------------+
| main                  |
+-----------------------+
| draw_box              |
| ch -> "#"             |
| width -> 5            |
| height -> 3           |
+-----------------------+
| draw_row              |
| ch -> "#"             |
| width -> 5            |
+-----------------------+
```

注意 `draw_row` 中的 `ch` 值和 `draw_box` 中的 `ch` 值是不同的——嗯，在这个例子中它们恰好是相同的值，但关键点是参数是局部的。你可以在不同的函数中使用相同的参数名；它在每个函数中是不同的变量。

## 调试

接口就像函数和调用者之间的契约。调用者同意提供某些参数，函数同意完成某些工作。

例如，`draw_box` 需要三个参数：`ch` 应该是单字符字符串；`width` 应该是正整数；`height` 应该是正整数。

这些要求称为**前置条件**（precondition），因为它们应该在函数开始执行之前为真。相应地，函数结束时的条件称为**后置条件**（postcondition）。后置条件包括函数的预期效果（如打印方框）和任何副作用。

前置条件是调用者的责任。如果调用者违反了前置条件而函数不能正常工作，那么 bug 在调用者，不在函数。

如果前置条件满足而后置条件不满足，那么 bug 在函数。如果你的前置条件和后置条件是清晰的，它们可以帮助调试。

## 术语表

**接口设计 (interface design):**
设计函数接口的过程，包括函数应该接受哪些参数。

**封装 (encapsulation):**
将一系列语句转换为函数定义的过程。

**泛化 (generalization):**
用适当通用的东西（如变量或参数）替换不必要的特定东西（如数字）的过程。

**重构 (refactoring):**
修改一个可工作的程序以改进函数接口和代码其他质量的过程。

**开发计划 (development plan):**
编写程序的过程。

**文档字符串 (docstring):**
出现在函数定义顶部的注释，用于记录函数的接口。

**前置条件 (precondition):**
在函数开始之前调用者应该满足的要求。

**后置条件 (postcondition):**
在函数结束之前函数应该满足的要求。

## 练习

### 练习

编写一个名为 `rectangle` 的函数，用指定字符绘制给定宽度和高度的实心矩形。例如，`rectangle("*", 8, 4)` 应该产生：

```
********
********
********
********
```

### 练习

编写一个名为 `rhombus` 的函数，绘制给定大小的菱形。例如，`rhombus("*", 3)` 应该产生：

```
  *
 ***
*****
 ***
  *
```

### 练习

编写一个更通用的函数 `parallelogram`，绘制给定宽度、高度和偏移量的实心平行四边形。然后重写 `rectangle`，使其使用偏移量为 `0` 的 `parallelogram`。

### 练习

编写一个名为 `triangle` 的函数，用指定字符绘制给定高度的等腰三角形。例如，`triangle("*", 5)` 应该产生：

```
    *
   ***
  *****
 *******
*********
```
