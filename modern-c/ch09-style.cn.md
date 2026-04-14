# 第九章：风格

> 级别 2 — 认知
>
> 编写人类可读的代码：格式化、命名和国际化。

代码被阅读的次数远多于被编写的次数。风格不是装饰——它是减少缺陷、加速代码审查并使维护成为可能的工程纪律。本章涵盖 C 程序员在五十年中发展出的约定，以及 Auto 如何将其中许多编码到语言本身中。

---

## 9.1 格式化

一致的格式化是你对代码库能做的最简单的改进。C 社区已达成几项广泛接受的规则：

**缩进。** 在项目中始终使用 4 个空格或制表符。永远不要混合使用。大多数现代 C 项目更倾向于 4 空格缩进。

```c
// 好：一致的 4 空格缩进
if (x > 0) {
    for (int i = 0; i < x; i++) {
        printf("%d\n", i);
    }
}

// 坏：混合缩进
if (x > 0) {
	for (int i = 0; i < x; i++) {
        printf("%d\n", i);
	}
}
```

**行长度。** 保持行不超过 80 个字符。过长的行表明表达式过于复杂，应该拆分。

```c
// 好：跨行拆分
int result = compute_something(
    input_data,
    buffer_size,
    &output_count
);

// 坏：过长的行
int result = compute_something(input_data, buffer_size, &output_count);
```

**花括号风格。** C 中两种主流风格是 K&R（左花括号在同一行）和 Allman（左花括号独占一行）。选择一种并保持一致。

```c
// K&R 风格（C 中最常见）
if (condition) {
    do_something();
}

// Allman 风格
if (condition)
{
    do_something();
}
```

Auto 默认使用 K&R 风格，并通过 `auto fmt` 强制执行：

```auto
// Auto 强制一致的格式化
fn calculate_area(width float, height float) float {
    width * height
}
```

在项目上运行 `auto fmt` 会将每个文件重新格式化为统一的规范风格，彻底消除格式化争论。

> **要点：** 一致性比任何特定的风格选择都重要。如果你的项目有约定，遵循它。如果没有，采用 `auto fmt`。

---

## 9.2 命名

名称是意图的主要文档。精心选择的名称使代码自解释；糟糕的名称造成困惑。

**C 命名约定：**

| 实体             | 约定                | 示例                        |
|-----------------|---------------------|-----------------------------|
| 变量            | `snake_case`        | `buffer_size`, `row_count`  |
| 函数            | `snake_case`        | `compute_area`, `parse_int` |
| 类型名          | `PascalCase`        | `TreeNode`, `FileHandle`    |
| 宏/常量         | `UPPER_SNAKE_CASE`  | `MAX_SIZE`, `PI`            |
| 结构体成员      | `snake_case`        | `first_name`, `age`         |

**描述性名称。** 名称应传达某事物是什么或做什么：

```c
// 好：描述性名称
int student_count = 0;
float average_grade = 0.0f;
const char* output_filename = "result.txt";

// 坏：晦涩的缩写
int sc = 0;
float ag = 0.0f;
const char* ofn = "result.txt";
```

**Auto 命名约定。** Auto 对函数和变量使用 `snake_case`，对类型使用 `PascalCase`，并通过点表示法将函数与类型关联：

```auto
type Rectangle {
    width float
    height float
}

fn Rectangle.area(r Rectangle) float {
    r.width * r.height
}

fn main() {
    let rect Rectangle = Rectangle(5.0, 3.0)
    print("Area:", rect.area(rect))
}
```

Auto 命名系统的关键优势是关联函数（`Rectangle.area`）是可发现的——类型名充当命名空间。在 C 中，你必须依靠命名约定（`rectangle_area`）来达到同样的清晰度。

<Listing path="listings/ch09/listing-09-01" title="整洁的代码风格" />

> **要点：** 写出新手无需上下文就能理解的名称。避免单字母名称，循环计数器（`i`、`j`、`k`）除外。

---

## 9.3 国际化

现代软件必须处理各种语言的文本。C 历来在这方面表现不佳，但 C23 和 Auto 都提供了更好的支持。

**字符集。** C 的 `char` 至少 8 位，传统上保存 ASCII。C23 要求执行字符集包含基本字符集，并允许通过编码扩展字符：

```c
// C：源字符集必须至少支持 ASCII
// 扩展字符取决于区域设置
printf("Hello\n");      // 仅 ASCII
printf("Bonjour\n");    // ASCII 兼容
```

**UTF-8。** 国际文本的主流编码是 UTF-8，它将每个 Unicode 码点表示为 1-4 字节的序列。C23 引入了 `char8_t` 和 `u8string` 字面量：

```c
// C23
const char8_t* greeting = u8"Hello, world!";
```

Auto 内置 UTF-8 支持。`str` 类型始终使用 UTF-8 编码：

```auto
let greeting str = "Hello, world!"
let chinese str = "你好世界"
let emoji str = "Hello 🌍"
print(greeting)
print(chinese)
print(emoji)
```

**源代码编码。** Auto 源文件默认为 UTF-8。标识符可以使用 ASCII 字符。字符串字面量可以包含任何有效的 UTF-8：

```auto
// 有效的 Auto：UTF-8 字符串字面量
let message str = "中文 — Chinese"
let greeting str = "こんにちは — Japanese"
print(message)
print(greeting)
```

> **要点：** 始终使用 UTF-8 处理文本。C 的历史编码问题（Shift-JIS、Latin-1 等）已通过普遍采用 UTF-8 解决。Auto 将此设为默认。

---

## 快速参考

| 方面            | C 约定                      | Auto 约定                    |
|----------------|-----------------------------|------------------------------|
| 缩进           | 4 空格或制表符              | 4 空格（`fmt` 强制）         |
| 行长度          | 80 字符                     | 80 字符（强制）              |
| 花括号风格      | K&R 或 Allman               | K&R（强制）                  |
| 变量名          | `snake_case`               | `snake_case`                |
| 函数名          | `snake_case`               | `snake_case` / `Type.method` |
| 类型名          | `PascalCase`               | `PascalCase`                |
| 常量            | `UPPER_SNAKE_CASE`         | `UPPER_SNAKE_CASE`          |
| 字符串编码      | 平台相关                    | 始终 UTF-8                   |
| 格式化工具      | `clang-format`、`indent`   | `auto fmt`                  |

---

*建立了风格约定后，下一章将介绍如何跨文件组织代码并记录接口。*
