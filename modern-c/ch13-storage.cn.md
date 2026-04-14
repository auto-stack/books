# 第十三章：存储

> 级别 2 — 认知
>
> malloc、存储期、初始化——C 如何管理对象生命周期以及 Auto 如何使其自动化。

内存管理是 C 程序最容易出错的地方。内存泄漏、释放后使用、双重释放和悬空指针占据了 C 安全漏洞的很大一部分。本章研究 C 的存储机制，并展示 Auto 如何消除整类内存错误。

---

## 13.1 malloc 及相关函数

C 提供四个函数用于动态内存分配：

```c
// C 深入：动态分配
void *malloc(size_t size);        // 分配 size 字节（未初始化）
void *calloc(size_t n, size_t s); // 分配 n*s 字节（零初始化）
void *realloc(void *p, size_t s); // 调整分配大小（可能移动）
void free(void *p);               // 释放
```

C 中的典型用法：

```c
// C 深入：malloc 生命周期
int *arr = malloc(10 * sizeof(int));  // 分配
if (!arr) { /* 处理错误 */ }           // 检查 NULL
for (int i = 0; i < 10; i++) {
    arr[i] = i * i;                    // 使用
}
// ... 稍后 ...
free(arr);                             // 释放
arr = NULL;                            // 避免悬空指针
```

问题层出不穷：

- **忘记释放**：随时间增长的内存泄漏。
- **释放后使用**：未定义行为，通常可被利用。
- **双重释放**：破坏堆分配器的内部状态。
- **不检查 NULL**：解引用失败的分配导致崩溃。
- **错误大小**：写 `malloc(sizeof(int*))` 而本意是 `malloc(sizeof(int))`。

**Auto 的替代：自动存储。** Auto 自动管理对象生命周期。Auto 中没有 `malloc`、`free`、`realloc` 或 `calloc`：

```auto
// Auto：没有 malloc/free，自动生命周期管理
var arr [10]int
for i in 0..10 {
    arr[i] = i * i
}
print("First:", arr[0])
// 不需要 free——存储自动回收
```

当 Auto 需要动态大小的集合时，标准库提供带有自动清理的可增长容器：

```auto
// Auto：可增长缓冲区
type Buffer {
    data [256]int
    size int
}

fn Buffer.new() Buffer {
    Buffer([256]int{}, 0)
}

fn Buffer.push(b Buffer, val int) {
    if b.size < 256 {
        b.data[b.size] = val
        b.size = b.size + 1
    }
}
```

<Listing path="listings/ch13/listing-13-01" title="malloc 与存储期" />

> **C 深入：** `malloc` 返回 `void*`，C 将其隐式转换为任何指针类型。这意味着 `int *p = malloc(...)` 在 C 中无需转换即可工作，但在 C++ 中不行。许多程序员添加转换 `(int*)malloc(...)`，这更糟——它抑制了忘记包含 `<stdlib.h>` 时的警告。

---

## 13.2 存储期

每个 C 对象具有三种**存储期**之一：

| 存储期    | 生命周期                          | 示例                   |
|----------|-----------------------------------|------------------------|
| 静态      | 整个程序执行期间                   | 全局变量、`static` 局部变量 |
| 自动      | 包含块的执行期间                   | 局部变量               |
| 分配      | 从 `malloc` 到 `free`             | 堆对象                 |

```c
// C 深入：存储期
int global = 42;              // 静态：永远存在

void example(void) {
    static int count = 0;     // 静态：永远存在，仅初始化一次
    int local = 10;           // 自动：直到块结束
    int *heap = malloc(sizeof(int)); // 分配：直到 free()
    *heap = 20;
    free(heap);
}
```

C 存储模型最危险的方面是返回指向自动变量的指针：

```c
// C 深入：经典缺陷——悬空指针
int* make_value(void) {
    int x = 42;
    return &x;    // 警告：返回了局部变量的地址！
}
// *make_value() 是未定义行为
```

**Auto 的方法：值语义。** Auto 默认使用值语义。函数返回值，而不是指针。调用者获得自己的副本：

```auto
// Auto：安全的值返回
fn make_value() int {
    let x int = 42
    x    // 按值返回——始终安全
}

fn main() {
    let v int = make_value()
    print("Got:", v)    // 42，不可能有悬空指针
}
```

> **C 深入：** C99 添加了变长数组（VLA）以避免局部大小数组使用 `malloc`。但 VLA 有问题：无限制的栈分配可能静默溢出栈，并且它们在 C11 中被设为可选。Auto 改为提供固定大小数组和可增长容器。

---

## 13.3 在定义之前使用对象

在 C 中，变量必须在使用前声明。这听起来简单，但与 `goto`、前向引用和相互引用的结构体的交互增加了复杂性：

```c
// C 深入：前向声明
struct Node;                        // 前向声明
struct Node {
    int value;
    struct Node *next;             // 指向前向声明类型的指针
};

// 函数前向声明
static int helper(int x);          // 声明
int compute(int x) {
    return helper(x * 2);          // 在定义之前使用
}
static int helper(int x) {         // 定义
    return x + 1;
}
```

对于函数，C 允许在定义之前使用函数，但前提是提供了前向声明（原型）。没有原型时，C 历史上假定函数返回 `int`——这是微妙缺陷的来源。

**Auto 的方法：声明顺序无关。** Auto 在整个编译单元中解析函数和类型引用。前向声明是不必要的：

```auto
// Auto：顺序无关的定义
fn compute(x int) int {
    helper(x * 2)     // 在定义之前使用——没问题
}

fn helper(x int) int {
    x + 1
}

fn main() {
    print("Result:", compute(5))
}
```

> **C 深入：** C 标准规定跳过带有 VLA 或可变修改类型的变量声明是未定义行为。Auto 完全避免 VLA 并且没有 `goto`，消除了这类问题。

---

## 13.4 初始化

C 提供多种初始化对象的方式，选择错误会产生后果：

```c
// C 深入：初始化形式
int a;                          // 未初始化：包含垃圾值
int b = 0;                      // 复制初始化
int c = {42};                   // 花括号初始化
int arr[3] = {1, 2, 3};        // 数组初始化
int zeros[5] = {0};             // 所有元素归零

struct Point { int x; int y; };
struct Point p1 = {1, 2};            // 位置初始化
struct Point p2 = {.y = 2, .x = 1};  // 指定初始化器（C99）
struct Point p3 = (struct Point){3, 4}; // 复合字面量
```

未初始化的局部变量是 C 最常见的缺陷来源之一：

```c
// C 深入：未初始化变量
int x;              // 垃圾值
printf("%d\n", x);  // 未定义行为：不确定的值
```

**Auto 的方法：强制初始化。** Auto 要求每个变量在声明时初始化。默认值由构造函数提供：

```auto
// Auto：所有变量初始化
type Config {
    name str
    value int
    active bool
}

fn Config.default() Config {
    Config("unnamed", 0, false)
}

fn Config.with_name(name str) Config {
    Config(name, 0, true)
}

fn main() {
    let default_cfg Config = Config.default()
    let named_cfg Config = Config.with_name("production")
    print("Default:", default_cfg.name, default_cfg.active)
    print("Named:", named_cfg.name, named_cfg.active)
}
```

<Listing path="listings/ch13/listing-13-02" title="初始化模式" />

> **C 深入：** 指定初始化器（`{.x = 1, .y = 2}`）是 C99 最好的特性之一。它们使结构体初始化自文档化且与顺序无关。Auto 使用构造函数达到相同目的，提供带类型安全的命名初始化。

---

## 13.5 机器模型

在最低层，C 的机器模型将内存视为平坦的字节数组。每个字节有地址，每个对象占用连续的地址范围：

```c
// C 深入：内存作为字节数组
int value = 0x41424344;
unsigned char *bytes = (unsigned char *)&value;
for (size_t i = 0; i < sizeof(value); i++) {
    printf("byte[%zu] = 0x%02x\n", i, bytes[i]);
}
// 小端序输出：
// byte[0] = 0x44  ('D')
// byte[1] = 0x43  ('C')
// byte[2] = 0x42  ('B')
// byte[3] = 0x41  ('A')
```

机器模型有重要含义：

- **字节序**：多字节值的字节顺序因平台而异。
- **填充**：结构体可能包含成员之间的未命名填充字节。
- **陷阱表示**：某些位模式可能导致硬件故障。
- **符号性**：负整数使用二进制补码（C23 中强制要求）。

**Auto 的方法：抽象的机器模型。** Auto 程序员不需要考虑字节序、填充或陷阱表示。a2c 转译器在生成 C 代码时处理这些细节：

```auto
// Auto：不关心字节级表示
let value int = 0x41424344
print("Value:", value)
// a2c 为目标平台生成正确的代码
```

> **C 深入：** 在 C23 之前，有符号整数的表示是实现定义的。C 理论上可以使用符号-绝对值或反码。实际上，每个实现都使用二进制补码。C23 最终将其设为强制要求，消除了一个实际上从未产生影响的可移植性问题。

---

## 快速参考

| 概念                | C 机制                      | Auto 机制                  |
|--------------------|-----------------------------|----------------------------|
| 动态分配           | `malloc`、`calloc`          | 自动、容器                 |
| 释放              | `free`                     | 自动清理                   |
| 调整分配大小       | `realloc`                  | 可增长容器                 |
| 存储期            | 静态 / 自动 / 分配          | 自动                       |
| 前向声明           | 原型                        | 不需要                     |
| 初始化            | 多种形式                    | 构造函数，强制初始化       |
| 指定初始化器       | `{.field = val}`           | 构造函数参数               |
| 未初始化变量       | 允许（危险）                | 禁止                       |
| 机器模型          | 字节数组、字节序             | 已抽象                     |

---

*存储和初始化是可靠程序的基础。Auto 通过移除手动分配和强制初始化，消除了整类内存管理缺陷。下一章将介绍 I/O 和文本处理。*
