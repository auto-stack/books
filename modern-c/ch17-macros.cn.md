# 第十七章：函数式宏

> 级别 3 — 经验
>
> 文本替换、预处理器技巧，以及为什么 Auto 用编译时元编程取代宏。

函数式宏是 C 最强大也最危险的特性之一。它们在编译器看到代码之前通过文本替换实现元编程。Auto 采取了根本不同的方法：它通过 `#[]` comptime 系统提供编译时代码生成，这是类型安全且可预测的。

---

## 17.1 宏如何工作

宏由 C 预处理器在编译前处理。预处理器执行文本替换：

```c
// C 深入：宏基础
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define SQUARE(x)  ((x) * (x))
#define PI 3.14159265

int result = MAX(3, 7);        // 展开为：((3) > (7) ? (3) : (7))
int area = SQUARE(5);          // 展开为：((5) * (5))
double circ = 2 * PI * r;     // 展开为：2 * 3.14159265 * r
```

预处理器是翻译的独立阶段。它对 C 类型、作用域规则或语法一无所知。它执行字面文本替换。

宏展开分几步进行：

1. 扫描标记序列查找宏调用。
2. 替换参数（处理 `#` 和 `##`）。
3. 重新扫描结果查找更多宏。
4. 重复直到没有更多替换可能。

> **C 深入：** 重新扫描步骤可能导致无限递归。C 标准通过不在宏自身展开期间重新展开它来防止这种情况。但宏之间的相互递归是允许的，有时在高级宏编程中被有意使用。

**Auto 的方法。** Auto 没有预处理器和宏。C 中使用宏的每个操作在 Auto 中使用常规函数或 comptime 元编程：

```auto
// Auto：常规函数取代宏
fn safe_max(a int, b int) int {
    if a > b { a } else { b }
}

fn safe_square(n int) int {
    n * n
}
```

---

## 17.2 参数检查

宏不检查参数类型。替换是纯文本的，这会导致微妙的缺陷：

```c
// C 深入：宏陷阱
#define SQUARE(x) ((x) * (x))

int a = SQUARE(2 + 3);
// 展开为：((2 + 3) * (2 + 3)) = 25（有括号时正确）

// 但是这样呢？
#define BAD_SQUARE(x) x * x
int b = BAD_SQUARE(2 + 3);
// 展开为：2 + 3 * 2 + 3 = 2 + 6 + 3 = 11（错误！）
```

最危险的陷阱是双重求值：

```c
// C 深入：双重求值
#define MAX(a, b) ((a) > (b) ? (a) : (b))

int x = 5;
int y = MAX(x++, 3);
// 展开为：((x++) > (3) ? (x++) : (3))
// 如果 x > 3，x 被递增两次！x 变成 7，不是 6。
```

常见宏问题：

| 问题               | 示例                        | 后果                     |
|-------------------|-----------------------------|--------------------------|
| 缺少括号          | `x * x` 配 `2 + 3`          | 运算符优先级错误          |
| 双重求值          | `MAX(x++, y)`               | 副作用执行两次           |
| 无类型检查        | `MAX("hello", 3)`          | 编译通过，运行时崩溃     |
| 无法调试          | 单步进入宏                  | 调试器中不可见           |
| 作用域问题        | 宏使用局部变量              | 名称冲突                 |

> **C 深入：** 安全宏的规则：始终给每个参数和整个表达式加括号。`#define SQUARE(x) ((x) * (x))`。即使如此，双重求值也无法防止。唯一真正安全的宏是参数为简单标识符或常量的宏。

**Auto 的方法。** Auto 函数没有这些问题：

```auto
// Auto：没有宏陷阱
fn safe_max(a int, b int) int {
    if a > b { a } else { b }
}

fn main() {
    // 参数只求值一次
    var x int = 5
    let y int = safe_max(x, 3)   // x 求值一次
    print("x:", x)               // x 仍然是 5
    print("y:", y)               // y 是 5
}
```

<Listing path="listings/ch17/listing-17-01" title="宏到 Auto 函数" />

---

## 17.3 调用上下文

宏可以通过预定义标识符访问上下文信息：

```c
// C 深入：预定义宏
#define LOG(msg) printf("%s:%d: %s\n", __FILE__, __LINE__, msg)

void process(void) {
    LOG("starting process");    // 输出 "main.c:5: starting process"
    LOG("done");                // 输出 "main.c:6: done"
}
```

标准预定义宏：

| 宏            | 值                               |
|---------------|----------------------------------|
| `__FILE__`    | 源文件名（字符串字面量）          |
| `__LINE__`    | 当前行号（整数）                  |
| `__DATE__`    | 编译日期（字符串）                |
| `__TIME__`    | 编译时间（字符串）                |
| `__func__`    | 当前函数名（C99）                 |
| `__STDC__`    | 如果编译器符合 C 标准则为 1       |

这些对于调试、日志记录和断言很有用：

```c
// C 深入：使用上下文的断言
#define ASSERT(expr) do { \
    if (!(expr)) { \
        fprintf(stderr, "%s:%d: assertion failed: %s\n", \
                __FILE__, __LINE__, #expr); \
        abort(); \
    } \
} while (0)
```

> **C 深入：** `do { ... } while (0)` 惯用法将宏体包装起来，使其行为像单个语句。没有它，`if (cond) ASSERT(x); else ...` 会出错，因为 `else` 会附加到宏内的 `if` 上。

**Auto 的方法。** Auto 的 comptime `#[]` 系统提供类似功能：

```auto
// Auto：comptime 上下文
fn process() {
    // comptime #[] 提供编译时信息
    // #[file] -> 当前文件名
    // #[line] -> 当前行号
    // #[fn]   -> 当前函数名
    print("Processing...")    // Auto 的 print 在调试模式包含源信息
}
```

---

## 17.4 变长参数列表

宏通过 `__VA_ARGS__` 支持可变参数：

```c
// C 深入：可变宏
#define LOG(fmt, ...) printf("[LOG] " fmt "\n", __VA_ARGS__)

LOG("value: %d", 42);         // [LOG] value: 42
LOG("x=%d y=%d", x, y);      // [LOG] x=3 y=7
```

C23 添加了 `__VA_OPT__` 来处理 `__VA_ARGS__` 为空时的逗号：

```c
// C 深入：__VA_OPT__
#define LOG(fmt, ...) printf(fmt __VA_OPT__(,) __VA_ARGS__)
LOG("hello");                 // printf("hello") -- 没有尾随逗号
LOG("x=%d", 42);             // printf("x=%d", 42)
```

> **C 深入：** 在 `__VA_OPT__` 之前，空参数问题是重要的痛点。GCC 引入了 `##__VA_ARGS__` 作为扩展来消除前面的逗号。C23 用 `__VA_OPT__` 标准化了解决方案，但许多代码库仍在使用 GCC 扩展。

**Auto 的方法。** Auto 在语言中内置了可变参数函数：

```auto
// Auto：可变参数函数
fn print_all(items ...str) {
    for item in items {
        print(item)
    }
}

fn main() {
    print_all("hello", "world")
    print_all("one", "two", "three")
}
```

Auto 的可变参数函数是类型安全的。每个参数必须匹配声明的参数类型（或可转换为其）。

---

## 17.5 默认参数

C 宏可以通过巧妙的技巧模拟默认参数：

```c
// C 深入：模拟默认参数
#define GREET_IMPL(name, greeting) printf("%s, %s!\n", greeting, name)
#define GET_GREET(a, b, FUNC, ...) FUNC
#define GREET(...) GET_GREET(__VA_ARGS__, GREET_IMPL,)(\
    __VA_ARGS__)
```

这是不可读的、脆弱的，并且依赖预处理器怪癖。但它出现在生产代码中，因为 C 没有原生默认参数。

> **C 深入：** 模拟默认参数的技巧通过利用 `__VA_ARGS__` 映射到第 N 个参数这一事实来工作。当提供更少的参数时，默认函数名出现在正确位置。这种技术被包括 Linux 内核的 `dev_dbg` 宏系列在内的主要库使用。

**Auto 的方法。** Auto 未来可能支持默认参数：

```auto
// Auto：默认参数（计划中）
fn greet(name str, greeting str = "Hello") {
    print(greeting + ", " + name + "!")
}

fn main() {
    greet("World")             // Hello, World!
    greet("World", "Hi")      // Hi, World!
}
```

在默认参数实现之前，惯用的方法是定义包装函数：

```auto
// Auto：默认值的包装函数
fn greet(name str) {
    greet_with(name, "Hello")
}

fn greet_with(name str, greeting str) {
    print(greeting + ", " + name + "!")
}

fn main() {
    greet("World")             // Hello, World!
    greet_with("World", "Hi")  // Hi, World!
}
```

> **关键信息：** Auto 的 comptime `#[]` 用类型安全、可预测的编译时元编程系统取代了整个 C 预处理器。没有文本替换，没有双重求值，没有括号游戏。

---

## 快速参考

| 概念                | C 机制                       | Auto 机制                  |
|--------------------|------------------------------|----------------------------|
| 文本替换           | `#define` 预处理器           | 常规函数                   |
| 类型安全           | 无（文本的）                  | 完整类型检查               |
| 双重求值           | 常见陷阱                     | 不可能                     |
| 调试               | 调试器中不可见               | 正常函数调试               |
| 上下文信息         | `__FILE__`、`__LINE__`       | Comptime `#[]` 系统        |
| 可变参数           | `__VA_ARGS__`                | 可变参数函数               |
| 默认参数           | 宏技巧                       | 默认参数（计划中）         |
| 字符串化           | `#` 运算符                   | Comptime 操作              |
| 标记粘贴           | `##` 运算符                  | Comptime 代码生成          |

---

*宏是 C 最初的元编程系统。它们在文本层面工作，在编译器看到代码之前。Auto 将元编程移入语言本身，在这里它可以被类型检查、调试和理解。*
