# 常用集合

Auto 的标准库包含许多非常有用的数据结构，称为 _集合（collections）_。大多数其他数据类型表示一个特定的值，而集合可以包含多个值。与内置的数组和元组类型不同，这些集合指向的数据存储在堆上，这意味着数据量不需要在编译时确定，可以在程序运行时增长或缩小。

在本章中，我们将讨论三种在程序中非常常用的集合：

- _列表_（`List<T>`）允许你将可变数量的值依次存储在一起。
- _字符串_（`String`）是字符的集合。我们之前已经提到过 `String` 类型，本章将深入讨论。
- _哈希映射_（`Map<K, V>`）允许你将一个值与特定的键关联起来。

我们将讨论如何创建和更新列表、字符串和哈希映射，以及每种集合的独特之处。

## 使用 `List<T>` 存储值列表

我们首先介绍的集合类型是 `List<T>`，也称为列表（等价于 Rust 的 `Vec<T>`）。列表允许你在单个数据结构中存储多个值，这些值在内存中相邻排列。列表只能存储相同类型的值。

### 创建新列表

要创建一个新的空列表，我们调用 `List.new()`：

<Listing number="8-1" file-name="main.auto" caption="创建新列表并使用 `push` 添加元素">

```auto
fn main() {
    var v = List.new()
    v.push(10)
    v.push(20)
    v.push(30)

    let len = v.len()
    print(f"Length: ${len}")
}
```

```rust
fn main() {
    let mut v = Vec::new();
    v.push(10);
    v.push(20);
    v.push(30);

    let len = v.len();
    println!("Length: {}", len);
}
```

</Listing>

注意我们使用 `var` 使列表可变，以便使用 `push` 添加元素。元素类型从第一次 `push` 调用中推断 — 由于我们 push 了 `10`（一个 `int`），列表就是 `List<int>`。

### 读取列表元素

有两种方式引用列表中存储的值：通过索引，或使用 `??`（空值合并）运算符进行安全访问。

<Listing number="8-2" file-name="main.auto" caption="使用索引和 `??` 运算符读取列表元素">

```auto
fn main() {
    var v = List.new()
    v.push(10)
    v.push(20)
    v.push(30)

    let third = v[2] ?? 0
    let missing = v[100] ?? 0
    print(f"Third: ${third}")
    print(f"Missing: ${missing}")
}
```

```rust
fn main() {
    let mut v = vec![10, 20, 30];

    let third = v.get(2).copied().unwrap_or(0);
    let missing = v.get(100).copied().unwrap_or(0);
    println!("Third: {}", third);
    println!("Missing: {}", missing);
}
```

</Listing>

在 Auto 中，`list[i]` 返回 `?T`（Option 类型）— 如果索引有效则为 `Some(value)`，如果越界则为 `None`。`??` 运算符提供默认值，替代了 Rust 中冗长的 `.get(i).copied().unwrap_or(default)` 模式。

这是 Auto 相对于 Rust 的一个关键安全改进：Auto 的列表索引永远不会 panic。你必须显式处理索引可能越界的情况。

### 遍历列表

要访问列表中的每个元素，我们遍历所有元素：

<Listing number="8-3" file-name="main.auto" caption="使用 `for` 循环遍历列表">

```auto
fn main() {
    var v = List.new()
    v.push(10)
    v.push(20)
    v.push(30)

    for item in v {
        print(f"Item: ${item}")
    }
}
```

```rust
fn main() {
    let v = vec![10, 20, 30];

    for item in v {
        println!("Item: {}", item);
    }
}
```

</Listing>

### 使用枚举存储多种类型

列表只能存储相同类型的值。当你需要存储不同类型时，可以定义一个枚举，其变体持有不同的值类型：

<Listing number="8-4" file-name="main.auto" caption="定义枚举以在列表中存储不同类型的值">

```auto
enum CellValue {
    Int int
    Text String
    Float float
}

fn main() {
    var row = List.new()
    row.push(CellValue.Int(1))
    row.push(CellValue.Text("hello"))
    row.push(CellValue.Float(3.14))
    print(f"Row length: ${row.len()}")
}
```

```rust
enum CellValue {
    Int(i32),
    Text(String),
    Float(f64),
}

fn main() {
    let mut row = Vec::new();
    row.push(CellValue::Int(1));
    row.push(CellValue::Text(String::from("hello")));
    row.push(CellValue::Float(3.14));
    println!("Row length: {}", row.len());
}
```

</Listing>

## 使用字符串存储 UTF-8 编码的文本

我们在前面的章节中已经大量使用了 `String`。`String` 是一个可增长的、可变的、拥有的、UTF-8 编码的字符串类型。让我们看看一些常见操作。

### 创建和更新字符串

<Listing number="8-5" file-name="main.auto" caption="创建和更新字符串">

```auto
fn main() {
    let s1 = "hello".to_string()
    let s2 = String.from("world")
    print(f"s1: ${s1}")
    print(f"s2: ${s2}")

    var s3 = String.from("foo")
    s3.push_str("bar")
    print(f"s3: ${s3}")
}
```

```rust
fn main() {
    let s1 = "hello".to_string();
    let s2 = String::from("world");
    println!("s1: {}", s1);
    println!("s2: {}", s2);

    let mut s3 = String::from("foo");
    s3.push_str("bar");
    println!("s3: {}", s3);
}
```

</Listing>

关键区别：

| 特性 | Auto | Rust |
|------|------|------|
| 从字面量创建 | `"hello".to_string()` | `"hello".to_string()` |
| 从字面量创建 | `String.from("world")` | `String::from("world")` |
| 追加字符串 | `s.push_str("bar")` | `s.push_str("bar")` |

### 使用 f-字符串拼接

Auto 使用 f-字符串插值进行字符串拼接，而非 Rust 的 `+` 运算符或 `format!` 宏：

<Listing number="8-6" file-name="main.auto" caption="使用 f-字符串拼接字符串">

```auto
fn main() {
    let s1 = "Hello"
    let s2 = "world"
    let s3 = f"${s1}, ${s2}!"
    print(s3)
}
```

```rust
fn main() {
    let s1 = String::from("Hello");
    let s2 = String::from("world");
    let s3 = format!("{}, {}!", s1, s2);
    println!("{}", s3);
}
```

</Listing>

f-字符串是 Auto 构建字符串的首选方式。它们比 `+` 拼接更易读，且不获取任何变量的所有权。

### 字符串索引

与 Rust 一样，Auto 不支持直接对字符串进行字节索引（例如 `"hello"[0]`）。这是因为字符串是 UTF-8 编码的，字节索引可能不对应有效的字符边界。

要遍历字符，使用 `chars` 方法：

```auto
for c in "hello".chars() {
    print(c.to_string())
}
```

## 使用哈希映射存储键值对

我们最后介绍的常用集合是哈希映射。`Map<K, V>` 类型存储从类型 `K` 的键到类型 `V` 的值的映射。在 Auto 中，`Map` 通过 `use.rust` 指令从 Rust 标准库引入。

### 创建新哈希映射

<Listing number="8-7" file-name="main.auto" caption="创建新哈希映射并插入键值对">

```auto
use.rust std::collections::HashMap

fn main() {
    var scores = HashMap.new()
    scores.insert("Blue", 10)
    scores.insert("Yellow", 50)
    print("Scores inserted")
}
```

```rust
use std::collections::HashMap;

fn main() {
    let mut scores = HashMap::new();
    scores.insert(String::from("Blue"), 10);
    scores.insert(String::from("Yellow"), 50);
    println!("Scores inserted");
}
```

</Listing>

关键区别：

| 特性 | Auto | Rust |
|------|------|------|
| 导入 | `use.rust std::collections::HashMap` | `use std::collections::HashMap;` |
| 创建空映射 | `HashMap.new()` | `HashMap::new()` |
| 插入 | `map.insert(key, val)` | `map.insert(key, val)` |

### 访问值

要从哈希映射中获取值，使用 `get` 方法，它返回 `?V`：

```auto
use.rust std::collections::HashMap

fn main() {
    var scores = HashMap.new()
    scores.insert("Blue", 10)
    let score = scores.get("Blue") ?? 0
    print(f"Score: ${score}")
}
```

### 更新哈希映射

使用相同键再次调用 `insert` 即可覆盖值：

```auto
scores.insert("Blue", 25)  // 覆盖之前的值 10
```

## 总结

Auto 的集合类型提供了与 Rust 相同的功能，但 API 更加简洁安全：

| 概念 | Auto | Rust |
|------|------|------|
| 动态数组 | `List<T>` | `Vec<T>` |
| 创建列表 | `List.new()` | `Vec::new()` / `vec![]` |
| 添加元素 | `v.push(val)` | `v.push(val)` |
| 安全访问 | `v[i] ?? default` | `v.get(i).copied().unwrap_or(default)` |
| 遍历 | `for item in v` | `for item in v` |
| 哈希映射 | `Map<K, V>` / `HashMap` | `HashMap<K, V>` |
| 字符串拼接 | `f"${a}, ${b}"` | `format!("{}, {}", a, b)` |
| 字符串追加 | `s.push_str("text")` | `s.push_str("text")` |

最显著的改进是 Auto 的安全列表索引 — `v[i]` 返回 `?T` 而非 panic，`??` 运算符提供了简洁的缺失值处理方式。这消除了一整类运行时错误。

在下一章中，我们将更深入地讨论错误处理。
