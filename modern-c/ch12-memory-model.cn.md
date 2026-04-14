# 第十二章：C 内存模型

> 级别 2 — 认知
>
> 对象、字节、联合体、有效类型、对齐——最深的 C 内部机制。

这是本书技术密度最高的一章。C 内存模型定义了数据如何存储、访问和在字节级别解释。理解它对于编写正确的底层 C 以及欣赏 Auto 抽象了什么都至关重要。

---

## 12.1 统一内存模型

在 C 中，所有数据——整数、浮点数、结构体、数组——都作为连续的**字节**序列存储。每个字节有唯一地址，内存中的每个对象都可以作为原始字节检查。

```c
// C 深入：对象表示
int x = 42;
unsigned char *bytes = (unsigned char*)&x;
printf("Byte 0: 0x%02x\n", bytes[0]);
printf("Byte 1: 0x%02x\n", bytes[1]);
// 小端序：0x2a, 0x00（对于 int32）
```

关键概念：

- **对象**：保存特定类型值的存储区域。
- **表示**：编码该值的字节序列。
- **`sizeof`**：对象占用的字节数。

```c
// C 深入：常见类型的大小
printf("sizeof(char):   %zu\n", sizeof(char));   // 始终为 1
printf("sizeof(int):    %zu\n", sizeof(int));    // 通常为 4
printf("sizeof(float):  %zu\n", sizeof(float));  // 通常为 4
printf("sizeof(double): %zu\n", sizeof(double)); // 通常为 8
printf("sizeof(int*):   %zu\n", sizeof(int*));   // 4 或 8
```

类型的大小决定了指针算术前进多少字节。`sizeof(char)` 根据定义始终为 1——它是 C 中存储的基本单位。

> **C 深入：** C 保证任何对象都可以使用 `memcpy` 逐字节复制。这是序列化和反序列化的基础。Auto 对其值类型提供相同的保证。

---

## 12.2 联合体

**联合体**是一种所有成员共享相同内存位置的类型。联合体的大小等于其最大成员的大小：

```c
// C 深入：联合体
union Value {
    int i;
    float f;
    char s[16];
};

union Value v;
v.i = 42;                // 以 int 存储
printf("%d\n", v.i);     // 以 int 读取：42
v.f = 3.14f;             // 以 float 覆盖
printf("%f\n", v.f);     // 以 float 读取：3.14
// printf("%d\n", v.i);  // 未定义行为：类型错误！
```

从非最后写入的成员读取在标准 C 中是未定义行为（符号变体有例外）。这使得裸联合体很危险。

**标签联合体**通过将判别符（标签）与联合体配对解决了这个问题：

```c
// C 深入：标签联合体
enum ValueType { VAL_INT, VAL_FLOAT, VAL_STRING };

struct TaggedValue {
    enum ValueType tag;
    union {
        int i;
        float f;
        char s[16];
    } data;
};

void describe(struct TaggedValue v) {
    switch (v.tag) {
        case VAL_INT:    printf("integer: %d\n", v.data.i); break;
        case VAL_FLOAT:  printf("float: %f\n", v.data.f); break;
        case VAL_STRING: printf("string: %s\n", v.data.s); break;
    }
}
```

**Auto 的替代：带数据的 `enum`。** Auto 将标签联合体作为一等特性提供，消除了手动管理：

```auto
enum Value {
    IntVal int
    FloatVal float
    StrVal str
}

fn describe(v Value) str {
    is v {
        IntVal(n) => "integer: " + str(n)
        FloatVal(f) => "float: " + str(f)
        StrVal(s) => "string: " + s
    }
}
```

<Listing path="listings/ch12/listing-12-01" title="内存模型与联合体" />

> **C 深入：** 标签联合体是 C 中最常见的模式之一。它们如此基础，以至于 Rust 有 `enum`、Swift 有 `enum with associated values`、Auto 有 `enum`——都通过语言支持而非手动纪律提供相同的能力。

---

## 12.3 内存与状态

C 中的每个对象都有一个**有效类型**，决定它如何被访问。C 标准施加了**严格别名规则**：对象的存储值只能通过具有以下类型之一的左值表达式访问：

- 与对象有效类型兼容的类型
- 与有效类型兼容的类型的限定版本
- 与有效类型对应的有符号或无符号类型
- 字符类型（`char`、`unsigned char`、`signed char`）

```c
// C 深入：严格别名违规
int x = 42;
float *fp = (float*)&x;   // 违规：float* 不能别名 int
*fp = 3.14f;               // 未定义行为

// 正确：使用 memcpy 进行类型双关
float f;
memcpy(&f, &x, sizeof(f)); // 定义良好的字节级复制
```

严格别名规则存在是因为编译器假设不同类型的指针不会别名同一内存，从而启用优化。违反它会导致静默的错误编译——最糟糕的缺陷类型。

> **C 深入：** `char*` 是通用逃生通道。你始终可以通过 `char*` 或 `unsigned char*` 访问任何对象的字节。这就是 `memcpy` 和 `printf` 内部的工作方式。

---

## 12.4 指向非特定对象的指针：`void*`

C 的 `void*` 是可以指向任何对象类型的通用指针，但不能直接解引用：

```c
// C 深入：void*
void *generic = &x;           // 任何指针转换为 void*
int *specific = generic;      // void* 隐式转换回来

// 不能解引用 void*：
// *generic;                   // 错误：不完整类型

// 必须先转换：
printf("%d\n", *(int*)generic);
```

`void*` 在 C 中广泛用于泛型接口：

```c
void qsort(void *base, size_t nmemb, size_t size,
           int (*compar)(const void*, const void*));
```

Auto 完全避免 `void*`。Auto 中的泛型函数使用类型参数或 `spec` 约束：

```auto
// Auto：没有 void*，泛型是类型安全的
fn max(a int, b int) int {
    if a > b { a } else { b }
}
```

> **C 深入：** `void*` 是许多 C 缺陷的根本原因。它绕过类型系统，因此将错误类型传递给 `qsort` 的比较器会导致未定义行为，且没有编译器警告。Auto 的类型系统完全防止了这类错误。

---

## 12.5 显式转换

C 允许在任何指针类型之间进行显式类型转换（强制转换）：

```c
// C 深入：显式转换
int x = 0x41424344;
char *bytes = (char*)&x;        // int* 到 char*
printf("%c\n", bytes[0]);       // 小端序上为 'D'

// 危险：不相关的类型
float f = 1.0f;
int *ip = (int*)&f;             // float* 到 int*
printf("%d\n", *ip);            // 实现定义的
```

转换类别：

| 转换                     | 安全性           | 示例                      |
|-------------------------|------------------|---------------------------|
| 整数到整数               | 可能丢失值       | `(int)3.14`               |
| 指针到整数               | 实现定义         | `(uintptr_t)ptr`          |
| 整数到指针               | 实现定义         | `(int*)0x1234`            |
| 指针到指针               | 通常是 UB        | `(float*)&int_var`        |
| 指针到 `void*`          | 始终安全         | `(void*)ptr`              |
| `void*` 到指针           | 正确时安全       | `(int*)void_ptr`          |

**Auto 的方法。** Auto 提供显式的安全转换函数：

```auto
let x int = 42
let f float = float(x)   // 安全的、定义良好的转换
print("int to float:", f)
```

不兼容类型之间的转换在编译时被捕获。没有办法在不通过字节级接口的情况下将字节重新解释为不同类型。

> **C 深入：** C 的转换运算符 `(Type)value` 是语言中最危险的特性之一。它告诉编译器"相信我，我知道我在做什么"——而通常程序员是错的。C++ 引入了 `static_cast`、`reinterpret_cast` 和 `dynamic_cast` 来区分这些情况。Auto 完全消除了对大多数转换的需求。

---

## 12.6 有效类型

当内存被动态分配时，它最初没有有效类型。当通过类型化左值存储值时，类型被建立：

```c
// C 深入：已分配内存的有效类型
void *raw = malloc(sizeof(int));
int *ip = (int*)raw;
*ip = 42;                  // *raw 的有效类型现在是 int
printf("%d\n", *ip);       // 正确：访问匹配有效类型

float *fp = (float*)raw;
*fp = 3.14f;               // 有效类型现在是 float
printf("%f\n", *fp);       // 正确
// printf("%d\n", *ip);    // UB：有效类型已改为 float
```

这很重要，因为编译器可以自由假设 `int*` 和 `float*` 永远不会指向同一内存（严格别名）。更改有效类型然后通过旧类型访问是未定义行为。

Auto 的类型系统完全防止了这种情况。内存始终通过其声明的类型访问。没有办法更改变量的有效类型。

> **C 深入：** 有效类型和严格别名共同构成了 C 语义中最微妙的领域。编译器优化（特别是自动向量化）依赖严格别名。GCC 和 Clang 中的 `-fstrict-aliasing` 标志启用这些优化。使用 `-Wstrict-aliasing` 获取潜在违规的警告。

---

## 12.7 对齐

每个 C 类型都有一个**对齐要求**——该类型的对象可以在其中分配的连续地址之间的字节数：

```c
// C 深入：对齐
printf("alignof(char):   %zu\n", alignof(char));   // 1
printf("alignof(int):    %zu\n", alignof(int));    // 通常为 4
printf("alignof(double): %zu\n", alignof(double)); // 通常为 8

// 显式对齐
alignas(16) int aligned_x = 42;  // 16 字节对齐
```

未对齐访问可能导致：

- **性能下降**（在 x86 上硬件缓慢处理）
- **总线错误**（在 ARM 和其他架构上程序崩溃）
- **SIMD 失败**（向量操作需要 16/32/64 字节对齐）

C23 提供 `alignas` 和 `alignof`（或 `_Alignas` 和 `_Alignof`）：

```c
// C 深入：结构体中的对齐
struct aligned_data {
    alignas(16) float vec[4];  // SIMD 友好的对齐
    int count;
};
```

编译器可能在结构体成员之间插入**填充字节**以满足对齐：

```c
struct Example {
    char  a;    // 1 字节 + 3 填充
    int   b;    // 4 字节
    char  c;    // 1 字节 + 3 填充
};
// sizeof(struct Example) == 12（不是 6）
```

<Listing path="listings/ch12/listing-12-02" title="有效类型与对齐" />

**Auto 的方法。** Auto 自动处理对齐。a2c 转译器添加适当的 `alignas` 说明符并重新排列结构体成员以实现最佳打包。程序员永远不需要考虑对齐。

> **C 深入：** `malloc` 始终返回按 `max_align_t`（最大基本对齐）对齐的内存。对于扩展对齐（如 AVX-512 的 64 字节），使用 `aligned_alloc` 或 `posix_memalign`。Auto 自动封装这些。

---

## 快速参考

| 概念                | C 机制                      | Auto 机制                  |
|--------------------|-----------------------------|----------------------------|
| 对象表示           | 通过 `unsigned char*` 的字节 | 已抽象                     |
| 标签联合体         | `struct { enum + union }`   | 带数据变体的 `enum`        |
| 有效类型           | 运行时属性                   | 始终为声明类型             |
| 严格别名           | 编译器假设                   | 类型系统强制               |
| 泛型指针           | `void*`                    | 不暴露                     |
| 类型双关           | 指针转换或 `memcpy`         | 仅限显式转换               |
| 对齐              | `alignas`、`alignof`       | 自动                       |
| 结构体填充         | 编译器插入                   | 自动                       |
| 大小查询           | `sizeof`                   | `sizeof`                   |
| 字节复制           | `memcpy`                   | `copy`                     |

---

*这完成了级别 2 — 认知。你现在在字节级别理解了 C 内存模型以及 Auto 如何抽象其危险。下一级别将进入体验阶段，我们将把这些知识投入实践。*
