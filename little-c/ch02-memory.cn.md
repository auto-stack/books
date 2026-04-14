# 内存管理

本章探讨 C 语言中内存的工作方式以及 Auto 如何抽象这些细节。你将学习内存布局、
指针、数组、字符串、动态内存、函数指针，以及 Auto 如何防止常见的内存错误。

## 21. 内存布局

每个 C 程序将内存分为四个段：

```
+------------------+
| 代码段 (text)    |  编译后的机器指令
+------------------+
| 数据段 / BSS     |  全局和静态变量
+------------------+
| 堆 (heap)        |  malloc/free 区域（向上增长）
+------------------+
| 栈 (stack)       |  局部变量、调用帧（向下增长）
+------------------+
```

- **代码段**存放编译后的机器指令。
- **数据段**存放已初始化的全局变量；BSS 存放零初始化的全局变量。
- **堆**用于动态分配的内存（`malloc`/`free`）。
- **栈**用于局部变量和函数调用帧。

Auto 自然地映射到这个模型。函数内的 `let` 和 `var` 声明放在栈上。Auto 的
AutoFree 系统自动管理堆分配，你不需要手动调用 `malloc` 或 `free`。

<Listing name="memory-layout" file="listings/ch02/listing-02-01">

```auto
fn main() {
    let local int = 42
    print("Stack value:", local)

    // In C, global vars live in data segment
    // In Auto, all memory management is automatic
    print("Auto manages stack and heap automatically")
}
```

</Listing>

## 22. 指针与地址

在 C 中，每个变量都有一个内存地址。用 `&` 获取地址，用 `*` 解引用：

```c
int x = 42;
int *p = &x;    // p 保存 x 的地址
printf("%d\n", *p);  // 输出 42
```

Auto 不暴露原始指针。相反，它使用可选引用（`?T`）来表示可能引用另一个值
的变量。a2c 转译器在幕后生成指针代码。

<Listing name="pointers" file="listings/ch02/listing-02-02">

```auto
fn main() {
    let x int = 42
    let ptr ?int = x  // Auto optional reference
    print("Value:", x)
    print("Has reference:", ptr != nil)
}
```

</Listing>

## 23. 数组与指针算术

在 C 中，数组和指针密切相关。`a[i]` 等价于 `*(a + i)`。Auto 数组映射到
C 数组，并尽可能进行边界检查。

<Listing name="arrays" file="listings/ch02/listing-02-03">

```auto
fn main() {
    let scores [5]int = [5]int{90, 85, 78, 92, 88}
    for i in 0..5 {
        print("Score", i, "=", scores[i])
    }
    print("First three printed via loop")
    for i in 0..3 {
        print(scores[i])
    }
}
```

</Listing>

Auto 的 `a[i]` 直接映射到 C 的 `a[i]`。切片（`a[1..3]`）是 Auto 的编译时
特性；转译器生成循环或拷贝代码。

> **仅 C**：C 允许指针算术如 `p + 1` 来遍历内存。Auto 不暴露此特性。
> 请使用数组索引代替。

## 24. 字符串即字符数组

C 字符串是以空字符（`'\0'`）结尾的 `char` 数组。字符串 `"Hello"` 占用 6 个
字节：`H`、`e`、`l`、`l`、`o`、`\0`。

Auto 的 `str` 类型映射到 C 的 `char*`。Auto 自动处理空字符终止。Auto 中的
字符串拼接（`+`）在 C 中生成相应的 `malloc`、`strcpy` 和 `strcat` 调用。

<Listing name="strings" file="listings/ch02/listing-02-04">

```auto
fn main() {
    let greeting str = "Hello"
    let name str = "World"
    let full str = greeting + " " + name
    print(full)
    print("Length:", len(full))
}
```

</Listing>

内置函数 `len()` 映射到 C 的 `strlen()`。Auto 保证字符串始终以空字符结尾。

## 25. 动态内存

C 使用 `malloc` 分配堆内存，使用 `free` 释放：

```c
int *arr = malloc(10 * sizeof(int));
// ... 使用 arr ...
free(arr);
```

Auto 的 AutoFree 系统跟踪分配并在作用域结束时自动释放。你永远不需要在 Auto
代码中写 `malloc` 或 `free`。

<Listing name="dynamic-memory" file="listings/ch02/listing-02-05">

```auto
fn main() {
    // Auto handles memory automatically via AutoFree
    // No manual malloc/free needed
    var total int = 0
    for i in 1..11 {
        total = total + i
    }
    print("Sum 1..10 =", total)

    // C equivalent would use malloc:
    // int *arr = malloc(10 * sizeof(int));
    // ... use arr ...
    // free(arr);
    // Auto does this automatically
}
```

</Listing>

## 26. 内存泄漏与未定义行为

最常见的 C 内存错误包括：

- **内存泄漏**：忘记 `free` 已分配的内存。
- **释放后使用**：访问已释放的内存。
- **缓冲区溢出**：写入超出数组末尾的数据。
- **悬空指针**：使用指向已超出作用域的内存的指针。

Auto 从设计上防止这些问题：

- AutoFree 确保每个分配在作用域结束时被释放。
- 没有原始指针，意味着没有释放后使用或悬空指针的 bug。
- 数组边界在可能的情况下进行编译时检查。

## 27. const 与 volatile

C 的 `const` 限定符告诉编译器值不会改变：

```c
const int x = 42;
x = 10;  // 编译错误
```

Auto 的 `let` 等价于 `const`——一旦绑定，值就不能重新赋值。Auto 的 `var`
类似于普通的 C 变量。

C 的 `volatile` 限定符告诉编译器不要优化掉读写操作（例如用于硬件寄存器）。
Auto 不提供 `volatile`；这是 C 独有的底层系统编程特性。

## 28. 函数指针与回调

C 使用函数指针实现回调和策略模式：

```c
int (*op)(int, int);
op = &add;
result = op(3, 4);
```

Auto 用 `spec` 系统替代函数指针，提供类型安全的多态行为接口。

<Listing name="function-pointers" file="listings/ch02/listing-02-06">

```auto
spec IntOp {
    fn apply(a int, b int) int
}

type Adder {}

fn Adder.apply(a int, b int) int {
    a + b
}

type Multiplier {}

fn Multiplier.apply(a int, b int) int {
    a * b
}

fn compute(op Adder, a int, b int) int {
    op.apply(a, b)
}

fn main() {
    let adder Adder = Adder()
    let mult Multiplier = Multiplier()
    print("3 + 4 =", compute(adder, 3, 4))
}
```

</Listing>

## 29. 深拷贝与浅拷贝

在 C 中，赋值结构体是按值拷贝（字段的深拷贝）。赋值指针只拷贝地址（浅拷贝）：

```c
struct Point a = {1, 2};
struct Point b = a;     // 深拷贝：b 有自己的 x、y
struct Point *p = &a;   // 浅拷贝：p 指向 a
```

Auto 默认使用值语义。赋值 `let b Point = a` 创建一个独立的副本，就像 C 的
结构体赋值一样。Auto 的 `?T` 可选引用在需要共享访问时提供指针的等价功能。

## 30. 练习：内存管理

将所学的内存、递归和 Auto 的保障机制应用起来。

<Listing name="memory-practice" file="listings/ch02/listing-02-07">

```auto
fn fibonacci(n int) int {
    if n <= 1 {
        n
    } else {
        fibonacci(n - 1) + fibonacci(n - 2)
    }
}

fn main() {
    for i in 0..10 {
        print("fib(" + str(i) + ") =", fibonacci(i))
    }
}
```

</Listing>

递归的 `fibonacci` 函数为每次调用使用栈帧。Auto 确保即使递归很深也不会出现
内存泄漏——栈帧在函数返回时自动回收。

## 快速参考

| 概念 | Auto | C |
|------|------|---|
| 栈变量 | `let x int = 5` | `int x = 5;` |
| 堆分配 | 自动（AutoFree） | `malloc(size)` |
| 堆释放 | 自动 | `free(ptr)` |
| 指针 | 不暴露 | `int *p = &x` |
| 可选引用 | `?T` | `T*`（可为空）|
| 数组 | `[N]T{...}` | `T arr[N] = {...}` |
| 字符串 | `str` | `char*` |
| 字符串拼接 | `a + b` | `strcat`/`malloc` |
| 字符串长度 | `len(s)` | `strlen(s)` |
| 不可变 | `let x` | `const int x` |
| 可变 | `var x` | `int x` |
| 函数指针 | `spec` + `type` | `int (*fn)(int, int)` |
| 值拷贝 | 默认行为 | 结构体赋值 |
| 空值检查 | `x != nil` | `p != NULL` |
