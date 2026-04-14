# 第十八章：类型泛型编程

> 级别 3 -- 经验
>
> _Generic、类型推断和匿名函数——在 C 中编写跨类型工作的代码，以及 Auto 的泛型系统如何使其自然化。

C 被设计为类型化语言：每个对象都有类型，操作针对特定类型定义。但实际程序需要不管数据的精确类型都能操作。C 已经演化出类型泛型编程的机制——`_Generic`、`auto`、`typeof`——Auto 通过完整的泛型系统进一步推进了这些想法。

---

## 18.1 固有的类型泛型特性

C 一直通过转换和提升具有隐式类型泛型特性：

```c
// C 深入：隐式转换
short s = 42;
int i = s;          // short 提升为 int（整数提升）
long l = i;         // int 转换为 long（通常转换）
double d = l;       // long 转换为 double（通常转换）

int a = 3;
double b = 4.2;
double c = a + b;   // a 在加法前被转换为 double
```

通常算术转换规则确定二元操作的公共类型：

1. 对两个操作数执行整数提升。
2. 如果类型不同，"较窄"的类型被转换为"较宽"的类型。
3. 如果两者都是整数类型，有符号性根据标准中的复杂规则解决。

> **C 深入：** C 中的整数提升规则经常令人惊讶。在大多数平台上，`short` 值在任何算术操作之前被提升为 `int`。这意味着 `short a, b; auto c = a + b;` 产生 `int`，而不是 `short`。这些规则还以不明显的方式与有符号性交互：`unsigned int` 对 `long` 取决于平台大小。

这些转换是自动的但不总是安全的：

```c
// C 深入：转换陷阱
int big = 2147483647;    // 32 位 int 的 INT_MAX
float f = big;            // 可能丢失精度（float 有 23 位尾数）
int back = f;             // 如果 f > INT_MAX，实现定义的行为

unsigned int u = -1;     // 定义良好的：通过模转换得到 UINT_MAX
int signed_val = u;       // 如果 u > INT_MAX，实现定义的行为
```

**Auto 的方法。** Auto 要求类型之间的显式转换。没有隐式窄化转换：

```auto
// Auto：显式转换
fn main() {
    let i int = 42
    let d float = float(i)     // 显式转换
    let s int = int(d)         // 显式转换
    print("i:", i)
    print("d:", d)
    print("s:", s)
}
```

---

## 18.2 泛型选择

C11 引入了 `_Generic` 用于编译时类型分发：

```c
// C 深入：_Generic
#include <stdio.h>

#define print_val(x) _Generic((x), \
    int: print_int,                \
    double: print_double,          \
    char*: print_string            \
)(x)

void print_int(int x) { printf("%d\n", x); }
void print_double(double x) { printf("%f\n", x); }
void print_string(char *x) { printf("%s\n", x); }

int main(void) {
    print_val(42);            // 调用 print_int
    print_val(3.14);          // 调用 print_double
    print_val("hello");       // 调用 print_string
    return 0;
}
```

`_Generic` 是编译时构造。编译器根据控制表达式的类型选择匹配的关联。它不在运行时求值表达式。

> **C 深入：** `_Generic` 功能强大但冗长。每种类型需要自己的函数，映射必须手动维护。它对限定类型也有令人惊讶的行为：`const int` 和 `int` 对 `_Generic` 是不同类型，所以你可能需要两者的条目。

`<tgmath.h>` 头文件使用 `_Generic` 提供类型泛型数学函数：

```c
// C 深入：tgmath.h
#include <tgmath.h>

double d = sqrt(2.0);       // 调用 sqrt(double)
float f = sqrtf(2.0f);      // 调用 sqrtf(float) -- 但有 tgmath：
float g = sqrt(2.0f);       // 也调用 sqrtf！类型泛型分发
```

**Auto 的方法。** Auto 计划通过 `spec` 约束提供泛型：

```auto
// Auto：带 spec 约束的泛型（计划中）
// fn add<T>(a T, b T) T where T: Numeric {
//     a + b
// }

// 目前，使用单独的函数或 comptime 分发
fn generic_add(a int, b int) int {
    a + b
}

fn generic_add_f(a float, b float) float {
    a + b
}
```

<Listing path="listings/ch18/listing-18-01" title="类型泛型编程" />

---

## 18.3 类型推断

C23 通过 `auto` 关键字和 `typeof` 引入了类型推断：

```c
// C 深入：C23 类型推断
auto x = 42;               // int
auto pi = 3.14;             // double（C 默认为 double）
auto name = "hello";        // char*（指针，不是数组）

typeof(x) y = x;            // y 与 x 类型相同：int
typeof(3.14) z = 2.72;     // z 是 double
```

C23 中的 `auto` 关键字与旧 C 中的 `auto` 不同，旧 C 意味着"自动存储期"（栈变量）。在 C23 中，`auto` 意味着"从初始化器推导类型"。

`typeof`（和 `typeof_unqual`）给出表达式的类型：

```c
// C 深入：typeof 用法
int arr[10];
typeof(arr) other;          // int[10]
typeof(arr[0]) val;         // int
typeof(&arr) ptr;           // int(*)[10]

// 在宏中很有用
#define SWAP(a, b) do { \
    typeof(a) _tmp = a; \
    a = b; \
    b = _tmp; \
} while (0)
```

> **C 深入：** C23 的 `auto` 不改变类型系统——它只是在编译时推导类型。结果类型与你显式写出的完全相同。这与 C++ 的 `auto` 不同，C++ 可以推导不同类型（例如，丢弃引用）。C 的 `auto` 总是推导初始化器表达式的非限定类型。

**Auto 的方法。** Auto 通过 `var` 提供类型推断：

```auto
// Auto：类型推断
fn main() {
    var x = 42           // 推导为 int
    var pi = 3.14        // 推导为 float
    var name = "Auto"    // 推导为 str
    var flag = true      // 推导为 bool

    print("x:", x)
    print("pi:", pi)
    print("name:", name)
    print("flag:", flag)
}
```

<Listing path="listings/ch18/listing-18-02" title="类型推断" />

C23 `auto` 与 Auto `var` 的主要区别：

| 特性            | C23 `auto`               | Auto `var`                |
|----------------|--------------------------|---------------------------|
| 声明           | `auto x = 42;`           | `var x = 42`              |
| 类型推导       | 从初始化器                | 从初始化器                |
| 必须初始化     | 是                       | 是                        |
| 不能为 NULL    | 否（可以是指针）          | 没有空指针                |
| 字符串类型     | `char*`                  | `str`（拥有的字符串）     |

---

## 18.4 匿名函数

C 在标准语言中没有匿名函数（lambda）。最接近的等价物是函数指针：

```c
// C 深入：函数指针
int add(int a, int b) { return a + b; }
int mul(int a, int b) { return a * b; }

int apply(int (*op)(int, int), int a, int b) {
    return op(a, b);
}

int main(void) {
    printf("%d\n", apply(add, 3, 7));  // 10
    printf("%d\n", apply(mul, 3, 7));  // 21
    return 0;
}
```

Apple 的 Blocks 扩展为 C 添加了匿名函数：

```c
// C 深入：Apple Blocks（扩展）
#include <Block.h>

int main(void) {
    int (^add)(int, int) = ^(int a, int b) {
        return a + b;
    };
    printf("%d\n", add(3, 7));  // 10
    return 0;
}
```

> **C 深入：** Blocks 扩展不是标准 C 的一部分。它由 Clang 和 Apple 的工具链支持。GNU C 有嵌套函数作为扩展，但它们不是可重入的，不能从函数返回。两个扩展都不可移植。

**Auto 的方法。** Auto 计划将闭包支持为第一类值：

```auto
// Auto：闭包（计划中）
fn apply(f fn(int, int) int, a int, b int) int {
    f(a, b)
}

fn main() {
    let add = fn(a int, b int) int { a + b }
    let mul = fn(a int, b int) int { a * b }

    print("add:", apply(add, 3, 7))    // 10
    print("mul:", apply(mul, 3, 7))    // 21
}
```

在闭包实现之前，函数指针与 C 中的工作方式相同：

```auto
// Auto：函数值（当前）
fn add(a int, b int) int { a + b }

fn apply(f fn(int, int) int, a int, b int) int {
    f(a, b)
}

fn main() {
    print("result:", apply(add, 3, 7))
}
```

> **C 深入：** C 中缺乏标准闭包是一个重大限制。C++ 有 lambda（自 C++11 起），Rust 有闭包，Go 有匿名函数，甚至 Java 也有 lambda。C 坚持编译时函数定义使得高阶编程变得笨拙。Auto 的闭包设计从这些语言中汲取灵感，提供自然的闭包语法。

---

## 快速参考

| 概念                | C 机制                       | Auto 机制                  |
|--------------------|------------------------------|----------------------------|
| 类型转换           | 隐式（有规则）                | 显式                       |
| 类型分发           | `_Generic`（C11）            | 带 `spec` 的泛型           |
| 类型泛型数学       | `<tgmath.h>`                | 计划中的泛型               |
| 类型推断           | `auto`（C23）                | `var`                      |
| 表达式类型         | `typeof`（C23）              | 从上下文推断               |
| 匿名函数           | Blocks（扩展）               | 闭包（计划中）             |
| 函数指针           | `int (*)(int, int)`          | `fn(int, int) int`         |

---

*C 中的类型泛型编程需要层层宏、`_Generic` 和编译器扩展。Auto 使其自然化：编写一次算法，类型系统确保它对每种类型都正确工作。*
