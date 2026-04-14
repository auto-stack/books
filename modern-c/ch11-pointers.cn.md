# 第十一章：指针

> 级别 2 — 认知
>
> C 最强大也最危险的特性，以及 Auto 如何消除这种危险。

指针是 C 的标志性特性。它们提供对内存的直接访问，实现高效的数据结构，并支撑每一个重要的 C 程序。它们也是大多数 C 缺陷的根源：空指针解引用、悬空指针、缓冲区溢出和释放后使用错误。

Auto 从用户代码中消除了裸指针，同时保留了它们提供的表达能力。本章深入探讨 C 指针，让你理解 Auto 为你处理了什么。

---

## 11.1 指针操作

**指针**是存储另一个变量地址的变量。C 提供两个基本指针运算符：

- `&`（取地址）：获取变量的内存地址
- `*`（解引用）：访问内存地址处的值

```c
// C 深入：基本指针操作
int x = 42;
int *ptr = &x;       // ptr 保存 x 的地址
printf("Address: %p\n", (void*)ptr);
printf("Value: %d\n", *ptr);    // 解引用：打印 42

*ptr = 99;            // 通过指针修改 x
printf("x is now: %d\n", x);    // 打印 99
```

**指针算术。** 指向数组元素的指针支持算术运算：

```c
// C 深入：指针算术
int arr[5] = {10, 20, 30, 40, 50};
int *p = arr;         // p 指向 arr[0]

p += 3;               // p 现在指向 arr[3]
printf("%d\n", *p);   // 打印 40

int diff = p - arr;   // 指针减法：3
```

编译器将偏移量乘以 `sizeof(int)`，所以 `p += 3` 实际上向地址添加了 `3 * sizeof(int)` 字节。这就是为什么指针算术需要类型化指针——类型决定了元素大小。

**Auto 的替代。** Auto 没有指针类型。数组索引替代指针算术：

```auto
let arr [5]int = [5]int{10, 20, 30, 40, 50}
print("arr[3]:", arr[3])   // 直接索引，无指针
```

<Listing path="listings/ch11/listing-11-01" title="指针操作" />

> **C 深入：** 在 C 中，`arr[i]` 被定义为 `*(arr + i)`。下标运算符是指针算术的语法糖。理解这种等价关系对于阅读 C 代码至关重要。

---

## 11.2 指针与结构体

指向结构体的指针在 C 中无处不在。它们实现高效的按引用传递和链式数据结构：

```c
// C 深入：指向结构体的指针
typedef struct {
    float x;
    float y;
} Point;

Point p = {3.0f, 4.0f};
Point *ptr = &p;

// 通过指针访问成员
printf("x = %f\n", ptr->x);    // -> 运算符
printf("y = %f\n", ptr->y);

// 等价写法：(*ptr).x
printf("x = %f\n", (*ptr).x);
```

`->` 运算符是解引用结构体指针并访问成员的语法糖：`ptr->member` 等价于 `(*ptr).member`。

**链式结构。** 指针实现自引用类型：

```c
// C 深入：链表节点
typedef struct Node {
    int data;
    struct Node *next;    // 指向相同类型的指针
} Node;

Node c = {30, NULL};
Node b = {20, &c};
Node a = {10, &b};

// 遍历：a -> b -> c
Node *current = &a;
while (current != NULL) {
    printf("%d ", current->data);
    current = current->next;
}
// 输出：10 20 30
```

**Auto 的替代。** Auto 按值传递结构体并使用关联函数。链式数据结构使用带变体的 `enum`：

```auto
type Point {
    x float
    y float
}

fn Point.distance_from_origin(p Point) float {
    (p.x * p.x + p.y * p.y) ** 0.5
}
```

<Listing path="listings/ch11/listing-11-02" title="指针与结构体" />

> **C 深入：** `->` 运算符的存在是因为 `.` 的优先级高于 `*`。写 `*ptr.x` 会被解析为 `*(ptr.x)`，这是错误的。`->` 运算符避免了这个问题。

---

## 11.3 指针与数组

在 C 中，数组和指针深度关联。当数组名在表达式中使用时（`sizeof` 操作数除外），它会**退化**为指向其首元素的指针：

```c
// C 深入：数组到指针退化
int arr[5] = {10, 20, 30, 40, 50};
int *p = arr;        // arr 退化为 &arr[0]

// 这些是等价的：
arr[2] == *(arr + 2);
*(p + 2) == p[2];     // 指针也支持 []
```

这种退化有重要影响：

1. 数组不能赋值（`arr2 = arr1` 是非法的）。
2. 传递给函数的数组变成指针——`sizeof` 给出指针大小，而不是数组大小。
3. 指针算术自动按元素大小缩放。

```c
// C 深入：数组参数退化
void print_sum(int *arr, size_t n) {
    // 这里 sizeof(arr) == sizeof(int*)，不是数组大小！
    int sum = 0;
    for (size_t i = 0; i < n; i++) {
        sum += arr[i];
    }
    printf("Sum: %d\n", sum);
}
```

**Auto 的替代。** Auto 数组是携带其长度的真正类型：

```auto
let arr [5]int = [5]int{10, 20, 30, 40, 50}
let length int = len(arr)   // 5 — 无退化，无信息丢失
print("Third element:", arr[2])
```

> **C 深入：** 数组和指针之间的关系是 C 中最令初学者困惑的方面。数组不是指针——它只是在大多数上下文中转换为指针。`sizeof(arr)` 给出完整数组大小，但仅在 `arr` 被声明为数组的作用域中有效。

---

## 11.4 函数指针

C 允许指向函数的指针，实现回调和运行时多态：

```c
// C 深入：函数指针
int ascending(int a, int b) { return a - b; }
int descending(int a, int b) { return b - a; }

// 函数指针类型
typedef int (*Comparator)(int, int);

void sort(int *arr, size_t n, Comparator cmp) {
    // 使用提供的比较器排序
    for (size_t i = 0; i < n - 1; i++) {
        for (size_t j = 0; j < n - i - 1; j++) {
            if (cmp(arr[j], arr[j+1]) > 0) {
                int tmp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = tmp;
            }
        }
    }
}

int main(void) {
    int data[] = {5, 2, 8, 1, 9};
    sort(data, 5, ascending);    // 升序排序
    sort(data, 5, descending);   // 降序排序
}
```

函数指针的语法是出了名的晦涩：

```c
// C 深入：阅读函数指针声明
int (*cmp)(int, int);              // 指向函数(int,int)->int 的指针
void (*signal(int, void(*)(int)))(int);  // 真正难以理解的
```

**Auto 的替代：`spec`。** Auto 提供 `spec` 作为函数指针和虚分派的安全、可读的替代：

```auto
spec Comparator {
    fn compare(a int, b int) int
}

type Ascending {}

fn Ascending.compare(a int, b int) int {
    if a < b { -1 } else if a > b { 1 } else { 0 }
}

type Descending {}

fn Descending.compare(a int, b int) int {
    if a > b { -1 } else if a < b { 1 } else { 0 }
}
```

任何实现了 `Comparator` 的类型都可以在需要 `Comparator` 的地方使用。a2c 转译器在底层生成虚表（函数指针表）。

<Listing path="listings/ch11/listing-11-03" title="函数指针与 spec" />

> **C 深入：** 函数指针是 C 实现运行时多态的唯一机制。它们在标准库（`qsort`、`signal`）、GUI 框架（回调）和插件架构中使用。Auto 的 `spec` 提供了相同的功能，并具有编译时类型安全。

---

## 快速参考

| 概念                  | C 机制                  | Auto 机制                  |
|----------------------|-------------------------|----------------------------|
| 变量取地址           | `&x`                    | 不暴露                     |
| 解引用              | `*ptr`                  | 不暴露                     |
| 指针算术            | `ptr + n`、`ptr++`      | 数组索引 `arr[i]`          |
| 结构体指针访问      | `ptr->member`           | 直接 `p.member`            |
| 数组退化            | 自动                    | 不会发生                   |
| 空指针              | `NULL`                  | `nil`（在特定类型中）      |
| 函数指针            | `int (*f)(int, int)`    | `spec` 及其实现            |
| 链式结构            | `struct Node *next`     | `enum` 变体                |
| 回调                | 函数指针                | `spec` 实现                |

---

*指针直接关联到 C 如何建模内存。下一章将全面深入地介绍 C 内存模型——对象、表示、联合体、对齐和严格别名规则。*
