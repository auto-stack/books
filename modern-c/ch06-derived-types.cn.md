# 第六章：派生数据类型

> 级别 1 — 入门
>
> 从基本类型构建复杂数据结构：数组、指针、结构体和类型别名。

C 从基本构建块派生出复杂类型。数组将相同类型的元素在内存中连续排列。指针间接引用其他对象。结构体将异构字段捆绑为一个单元。类型别名为现有类型赋予新名字。Auto 以更简洁的语法提供了所有这些功能。

---

## 6.1 数组

**数组**是相同类型元素的固定大小序列，在内存中连续存储。数组大小是其类型的一部分，运行时不能改变。

```c
// C
int primes[5] = { 2, 3, 5, 7, 11 };
printf("first = %d\n", primes[0]);    // first = 2
printf("count = %zu\n", sizeof(primes)/sizeof(primes[0]));  // count = 5
```

```auto
// Auto
let primes [5]int = [5]int{2, 3, 5, 7, 11}
print("first =", primes[0])
print("count =", len(primes))
```

主要区别：

| 特性               | C                          | Auto                        |
|-------------------|----------------------------|------------------------------|
| 声明              | `int a[5];`               | `let a [5]int`              |
| 类型中的大小      | 前缀：`int a[N]`          | 后缀：`[N]int`              |
| 数组长度          | `sizeof(a)/sizeof(a[0])`  | `len(a)`                    |
| 边界检查          | 无（未定义行为）          | 运行时检查（默认）          |
| 多维数组          | `int m[3][4]`             | `[3][4]int`                 |

**数组到指针的退化：** 在 C 中，数组名在大多数上下文中会退化为指向其第一个元素的指针。这是许多微妙 bug 的根源。Auto 没有这种退化——数组保持为数组。

```c
// C：退化行为
int a[5] = {1,2,3,4,5};
int *p = a;        // a 退化为 &a[0]
p[10] = 99;        // 未定义行为：越界
```

> **要点：** C 数组没有边界检查。对 5 元素数组访问 `a[10]` 能编译但不报错，会破坏内存。Auto 默认插入运行时边界检查。

<Listing path="listings/ch06/listing-06-01" title="数组与迭代" />

---

## 6.2 指针作为不透明类型

> **C 深入：** 指针是存储另一个对象地址的变量。指针是 C 最强大也最危险的特性。它们支持动态数据结构、高效的参数传递和硬件访问——但也带来内存泄漏、悬空引用和缓冲区溢出。

```c
// C：基本指针用法
int x = 42;
int *ptr = &x;         // ptr 保存 x 的地址
printf("*ptr = %d\n", *ptr);   // *ptr = 42（解引用）
*ptr = 99;              // 通过 ptr 修改 x
```

Auto 不暴露原始指针。相反它提供：

- **引用**——由编译器管理的安全、非空句柄。
- **可选类型**（`?T`）——使用前必须检查的可空引用。

```auto
// Auto：无原始指针
let x int = 42
// Auto 管理引用；不需要取地址运算符
print("Value:", x)

// 可空引用的可选类型
let maybe ?int = x
if maybe != nil {
    print("Has value:", maybe)
}
```

C 与 Auto 的指针对应关系：

| C 概念              | Auto 等价              | 备注                              |
|--------------------|-----------------------|-----------------------------------|
| `T *p`            | 引用 / `&T`           | 非空，编译器管理                  |
| `NULL`            | `nil`                 | 可选类型的显式空值               |
| `T *p`（可空）     | `?T`                  | 使用前必须检查                   |
| `*p`（解引用）     | 直接访问               | 不需要解引用语法                 |
| `&x`（取地址）     | 自动                   | 编译器管理地址                   |
| `p->field`        | `p.field` 或 `p.method()` | 统一访问语法                 |

<Listing path="listings/ch06/listing-06-02" title="指针作为不透明引用" />

> **要点：** 如果你从 C 过来，把 Auto 引用看作永不为空且自动释放的指针。可选类型用显式空值检查替代了可空指针。

---

## 6.3 结构体

**结构体**将可能不同类型的命名字段组合为一个单元：

```c
// C
struct Fraction {
    int num;
    int den;
};

struct Fraction half = { .num = 1, .den = 2 };
printf("1/2 = %f\n", (double)half.num / half.den);
```

```auto
// Auto
type Fraction {
    num int
    den int
}

let half Fraction = Fraction(1, 2)
print("1/2 =", half.to_float(half))
```

结构体处理的主要区别：

| 特性              | C                              | Auto                          |
|------------------|--------------------------------|-------------------------------|
| 声明              | `struct Name { ... };`         | `type Name { ... }`           |
| 使用              | `struct Name var;`             | `let var Name`                |
| 字段访问          | `var.field` 或 `ptr->field`    | `var.field`（统一）           |
| 初始化            | `{ .field = value }`           | `Name(value, ...)` 或 `.new()`|
| 方法              | 无（独立函数）                  | 关联函数                      |
| 需要类型别名      | 常需要 `typedef struct Name Name;` | 自动                      |

Auto 中的**关联函数**让你可以将行为附加到类型上：

```auto
type Fraction {
    num int
    den int
}

fn Fraction.new(n int, d int) Fraction {
    Fraction(n, d)
}

fn Fraction.to_float(f Fraction) float {
    float(f.num) / float(f.den)
}
```

这会转译为 C：

```c
struct Fraction Fraction_new(int n, int d) { ... }
float Fraction_to_float(struct Fraction f) { ... }
```

<Listing path="listings/ch06/listing-06-03" title="结构体与类型别名" />

> **要点：** Auto 的 `type` 关键字替代了 `struct`、`typedef`，并添加了关联函数。转译器自动生成 C `struct` 和伴随函数。

---

## 6.4 类型别名

C 使用 `typedef` 为类型创建替代名称：

```c
typedef unsigned int uint;
typedef struct Point Point;       // 便利别名
typedef int (*Comparator)(const void *, const void *);  // 函数指针类型
```

Auto 使用 `type` 关键字进行所有类型定义和别名：

```auto
type uint = u32                    // 现有类型的别名
type Point {                       // 新结构体类型
    x int
    y int
}
type Callback = fn(int, int) int   // 函数类型别名
```

`typedef` 到 Auto 的映射：

| C typedef                    | Auto 等价                    |
|------------------------------|------------------------------|
| `typedef int Width;`         | `type Width = int`           |
| `typedef struct S S;`        | 不需要（`type S {}`）        |
| `typedef void (*Fn)(int);`   | `type Fn = fn(int)`          |
| `typedef int Arr[10];`       | `type Arr = [10]int`         |

> **要点：** 在 C 中，`typedef` 是可选的但广泛用于清晰性。在 Auto 中，`type` 是定义新类型和别名的通用关键字，消除了 `struct` + `typedef` 的仪式。

---

## 快速参考

| 概念            | C 语法                          | Auto 语法                     |
|----------------|---------------------------------|-------------------------------|
| 数组声明        | `int a[5];`                    | `let a [5]int`               |
| 数组初始化      | `{ 1, 2, 3 }`                  | `[5]int{1, 2, 3}`            |
| 数组元素        | `a[i]`                         | `a[i]`                        |
| 数组长度        | `sizeof(a)/sizeof(a[0])`       | `len(a)`                      |
| 指针声明        | `int *p;`                      | 不暴露                        |
| 空指针          | `NULL`                         | `nil`                         |
| 可选引用        | `int *p`（可空）                | `?int`                        |
| 结构体声明      | `struct S { int x; };`         | `type S { x int }`            |
| 结构体初始化    | `{ .x = 1 }`                   | `S(1)` 或 `S.new(1)`          |
| 字段访问        | `s.field` / `p->field`         | `s.field`（统一）             |
| 类型别名        | `typedef int Width;`           | `type Width = int`            |
| 关联函数        | 独立函数                        | `fn S.method(self) ...`       |

---

*下一章：[第七章 — 函数](ch07-functions.cn.md)*
