# 数据结构

本章介绍 Auto 如何使用 type、enum 和 spec 来组织数据，以及它们如何映射到 C 的
struct、union、typedef 和函数指针模式。你将构建真实的数据结构，并了解 Auto 的
设计如何防止常见错误。

## 31. 结构体

C 使用 `struct` 将相关字段组合在一起：

```c
struct Point {
    int x;
    int y;
};
struct Point p = {3, 4};
```

Auto 使用 `type` 定义结构体。字段以逗号分隔，构造函数使用命名初始化：

<Listing name="structures" file="listings/ch03/listing-03-01">

```auto
type Point {
    x int
    y int
}

fn Point.modulus() float {
    float(self.x * self.x + self.y * self.y)
}

fn main() {
    let p Point = Point(3, 4)
    print("Point: (", p.x, ",", p.y, ")")
    print("Modulus:", p.modulus())
}
```

</Listing>

Auto 的 `Point(3, 4)` 转译为 C 的 `(struct Point){.x = 3, .y = 4}`，使用
指定初始化器。方法如 `Point.modulus()` 在 C 中变为独立函数
`Point_Modulus(struct Point *self)`。

## 32. 联合体

C 联合体允许不同类型共享同一块内存：

```c
union Value {
    int i;
    float f;
};
```

普通的 C 联合体是不安全的——没有标签来指示哪个变体是活动的。Auto 的 `enum`
创建带标签的联合体，同时携带标签和值：

<Listing name="unions" file="listings/ch03/listing-03-02">

```auto
enum Shape {
    Circle float
    Rect float, float
    Triangle float, float, float
}

fn area(s Shape) float {
    is s {
        Circle(r) => 3.14159 * r * r
        Rect(w, h) => w * h
        Triangle(a, b, c) => {
            let s float = (a + b + c) / 2.0
            (s * (s - a) * (s - b) * (s - c)) ** 0.5
        }
    }
}

fn main() {
    let c Shape = Shape.Circle(5.0)
    let r Shape = Shape.Rect(3.0, 4.0)
    print("Circle area:", area(c))
    print("Rect area:", area(r))
}
```

</Listing>

在 C 中，`enum Shape` 变为一个包含 `tag` 字段和 `union as` 字段的结构体。
`is` 表达式转译为对标签的 `switch` 语句。

## 33. Typedef 与 Auto type

C 使用 `typedef` 创建类型别名：

```c
typedef int UserId;
typedef float Score;
```

Auto 的 `type` 携带单个字段时可以达到相同效果，无需 `typedef` 关键字：

<Listing name="typedef" file="listings/ch03/listing-03-03">

```auto
type UserId int
type Score float

fn make_user(id int, score float) {
    let uid UserId = UserId(id)
    let s Score = Score(score)
    print("User ID:", uid)
    print("Score:", s)
}

fn main() {
    make_user(1, 95.5)
}
```

</Listing>

Auto 的包装类型比 C 的 `typedef` 更具表达力，因为它们创建不同的类型——你不会
意外地将 `UserId` 传递给需要普通 `int` 的地方。

## 34. 位域

C 允许指定结构体字段的位宽：

```c
struct Flags {
    unsigned int is_active : 1;
    unsigned int priority : 3;
};
```

位域是 C 独有的特性，用于内存受限的环境。Auto 不提供位域。请使用 `bool` 和
`int` 字段代替；编译器会在可能的情况下进行优化。

## 35. 枚举

C 的 `enum` 赋予整数常量：

```c
enum Color { RED, GREEN, BLUE };
enum Color c = GREEN;
```

Auto 的 `enum`（无负载时）映射到 C 的 `enum`，使用 `NAME_VARIANT` 前缀
避免名称冲突：

```auto
enum Color { RED, GREEN, BLUE }
```

变为：

```c
enum Color { COLOR_RED, COLOR_GREEN, COLOR_BLUE };
```

## 36. 链表

链表是一种基础数据结构。每个节点保存一个值和指向下一个节点的引用。Auto 的
`?T` 可选类型自然地表示"下一个或无"的链接。

<Listing name="linked-list" file="listings/ch03/listing-03-04">

```auto
type Node {
    value int
    next ?Node
}

fn new_node(val int) Node {
    Node(val, nil)
}

fn print_list(head ?Node) {
    var current ?Node = head
    while current != nil {
        print(current.value)
        current = current.next
    }
}

fn main() {
    let a Node = new_node(1)
    let b Node = new_node(2)
    let c Node = new_node(3)
    a.next = b
    b.next = c
    print("Linked list:")
    print_list(a)
}
```

</Listing>

在 C 中，`?Node` 变为 `struct Node*`（可为空的指针）。`nil` 字面量映射为
`NULL`。

## 37. 栈与队列

栈是一种后进先出（LIFO）数据结构。用数组和一个顶部索引来实现。

<Listing name="stack" file="listings/ch03/listing-03-05">

```auto
type Stack {
    items [100]int
    top int
}

fn Stack.new() Stack {
    Stack([100]int{}, 0)
}

fn Stack.push(s Stack, val int) {
    s.items[s.top] = val
    s.top = s.top + 1
}

fn Stack.pop(s Stack) int {
    s.top = s.top - 1
    s.items[s.top]
}

fn main() {
    var s Stack = Stack.new()
    s.push(s, 10)
    s.push(s, 20)
    s.push(s, 30)
    print("Popped:", s.pop(s))
    print("Popped:", s.pop(s))
    print("Top:", s.top)
}
```

</Listing>

队列会使用两个索引（前端和后端）或环形缓冲区。原理相同：将数组封装在 `type`
中并提供 `push`/`pop` 方法。

## 38. 哈希表

简单的哈希表使用桶数组和一个哈希函数。在 C 中，你需要为哈希和相等性策略
使用函数指针。在 Auto 中，`spec` 系统可以优雅地实现这一点：

```auto
spec Hasher {
    fn hash(key str) int
}
```

每个桶可以是链表（用于冲突链接）。完整实现超出了本章范围，但模式遵循与
第 2 章函数指针相同的 `spec` + `type` 方法。

## 39. C 中的 OOP 与 Auto 的 spec/type

C 没有类，但可以用结构体和函数指针模拟面向对象编程。Auto 的 `spec` 和 `type`
系统使这种方式变得惯用且类型安全。

<Listing name="oop" file="listings/ch03/listing-03-06">

```auto
spec Drawable {
    fn draw()
}

type CircleObj {
    radius float
}

fn CircleObj.draw() {
    print("Drawing circle with radius:", self.radius)
}

type SquareObj {
    side float
}

fn SquareObj.draw() {
    print("Drawing square with side:", self.side)
}

fn render(d Drawable) {
    d.draw()
}

fn main() {
    let c CircleObj = CircleObj(5.0)
    let s SquareObj = SquareObj(3.0)
    render(c)
    render(s)
}
```

</Listing>

`spec Drawable` 在 C 中生成一个包含函数指针的虚表结构体。每个实现的类型
（`CircleObj`、`SquareObj`）获得一个虚表实例和具体的方法函数。

## 40. 练习：图书管理系统

使用类型、方法和状态管理构建一个小型图书管理系统。

<Listing name="library" file="listings/ch03/listing-03-07">

```auto
type Book {
    title str
    author str
    available bool
}

fn Book.new(title str, author str) Book {
    Book(title, author, true)
}

fn Book.borrow(b Book) {
    if b.available {
        b.available = false
        print("Borrowed:", b.title)
    } else {
        print("Not available:", b.title)
    }
}

fn Book.return_book(b Book) {
    b.available = true
    print("Returned:", b.title)
}

fn main() {
    let b1 Book = Book.new("The C Programming Language", "K&R")
    let b2 Book = Book.new("Auto Programming", "Auto Team")
    b1.borrow(b1)
    b1.borrow(b1)
    b1.return_book(b1)
    b1.borrow(b1)
}
```

</Listing>

这个练习结合了 `type` 定义、方法、状态修改和条件逻辑——本章所有概念的
综合运用。

## 快速参考

| 概念 | Auto | C |
|------|------|---|
| 结构体 | `type Name { fields }` | `struct Name { fields };` |
| 构造函数 | `Name(v1, v2)` | `(struct Name){.f1=v1, .f2=v2}` |
| 方法 | `fn Name.method()` | `void Name_method(struct Name *self)` |
| 标签联合 | `enum Tag { Variant fields }` | `struct Tag { tag; union as; }` |
| 类型别名 | `type Name BaseType` | `typedef BaseType Name;` |
| 枚举 | `enum Color { RED }` | `enum Color { COLOR_RED };` |
| 可选类型 | `?T` | `T*`（可为空）|
| 链表节点 | `type Node { val, ?Node }` | `struct Node { val; Node* next; }` |
| 接口 | `spec Name { fn ... }` | 带函数指针的虚表 |
| 实现 | `type Foo as Spec { }` | 虚表实例 + 方法 |
| 空值 | `nil` | `NULL` |
| 字段访问 | `self.field` | `self->field` |
