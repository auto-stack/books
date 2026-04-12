# 理解所有权

_所有权（Ownership）_ 是一套管理 Auto 程序如何处理内存的规则。所有程序在运行过程中都必须管理其使用计算机内存的方式。某些语言具有垃圾回收（garbage collection）机制，会在程序运行时定期寻找不再使用的内存；而在另一些语言中，程序员必须显式地分配和释放内存。Auto 采用第三种方式：通过一个所有权系统来管理内存，编译器会在编译时检查一系列规则。如果任何规则被违反，程序将无法编译。所有权的所有特性都不会在程序运行时降低其速度。

Auto 的所有权模型受到 Rust 的启发，并共享相同的基本原则。关键区别在于 Auto 减少了对显式标注的需求：在 Rust 需要生命周期标记和显式 `&`/`&mut` 语法的地方，Auto 使用基于属性的 `.view` 和 `.mut` 等关键字来更清晰地表达借用意图。

理解所有权之后，你将为理解 Auto 的独特特性打下坚实的基础。在本章中，我们将通过一些专注于一种非常常见的数据结构——字符串——的示例来学习所有权。

> ### 栈和堆
>
> 许多编程语言不需要你经常思考栈（Stack）和堆（Heap）。但在像 Auto 这样的系统编程语言中，一个值是在栈上还是在堆上会影响语言的行为方式以及你必须做出某些决策的原因。
>
> 栈和堆都是代码在运行时可以使用的内存部分，但它们的结构方式不同。栈按照获取值的顺序存储值，并以相反的顺序移除值。这被称为 _后进先出（LIFO）_。所有存储在栈上的数据必须具有已知且固定的大小。在编译时大小未知或大小可能发生变化的数据必须存储在堆上。
>
> 堆的组织性较差：当你将数据放到堆上时，你需要请求一定数量的空间。内存分配器（memory allocator）在堆中找到一块足够大的空位，将其标记为正在使用，并返回一个 _指针（pointer）_，即该位置的地址。
>
> 向栈推入数据比在堆上分配更快，因为分配器永远不必搜索存储新数据的位置；该位置始终在栈顶。访问堆中的数据通常比访问栈中的数据慢，因为你必须跟随指针才能到达那里。
>
> 跟踪代码的哪些部分正在使用堆上的哪些数据、最小化堆上的重复数据量以及清理堆上未使用的数据以免空间耗尽——这些都是所有权所要解决的问题。

## 什么是所有权？

### 所有权规则

首先，让我们看一下所有权规则。在学习说明这些规则的示例时，请牢记这些规则：

- Auto 中的每个值都有一个 _所有者（owner）_。
- 同一时间只能有一个所有者。
- 当所有者离开作用域时，该值将被丢弃。

这些规则与 Rust 的所有权规则完全相同。Auto 的借用检查器（borrow checker）在编译时强制执行这些规则，确保无需垃圾回收即可实现内存安全。

### 变量作用域

作为所有权的第一个示例，我们将查看一些变量的作用域。_作用域（scope）_ 是程序中某个项有效的范围。

<Listing number="4-1" file-name="main.auto" caption="一个变量及其有效的作用域">

```auto
fn main() {
    // s is not valid here, it's not yet declared
    let s = "hello"   // s is valid from this point forward
    // do stuff with s
    print(s)
    // this scope is now over, and s is no longer valid
}
```

```rust
fn main() {
    // s is not valid here, it's not yet declared
    let s = "hello";   // s is valid from this point forward
    // do stuff with s
    println!("{}", s);
    // this scope is now over, and s is no longer valid
}
```

</Listing>

换句话说，这里有两个重要的时间点：

- 当 `s` _进入_ 作用域时，它是有效的。
- 在它 _离开_ 作用域之前，它一直保持有效。

### `String` 类型

为了说明所有权规则，我们需要一个比第三章中介绍的更复杂的数据类型。我们希望查看存储在堆上的数据，并探索 Auto 如何知道何时清理这些数据。

我们已经见过字符串字面量（string literal），其中字符串值被硬编码到程序中。字符串字面量很方便，但它们并不适用于所有情况，因为它们是不可变的。Auto 拥有 `String` 类型来管理在堆上分配的数据。你可以像这样从字符串字面量创建一个 `String`：

```auto
let s String = String.from("hello")
```

```rust
let s = String::from("hello");
```

在 Auto 中，我们使用 `String.from()`（点语法）而不是 Rust 的 `String::from()`（双冒号语法）。两者都会创建一个堆分配的字符串。

这种字符串 _可以_ 被修改：

```auto
var s String = String.from("hello")
s.append(", world!")   // append a string
print(s)               // prints "hello, world!"
```

```rust
let mut s = String::from("hello");
s.push_str(", world!"); // push a string
println!("{}", s);      // prints "hello, world!"
```

### 内存与分配

对于字符串字面量，文本被直接硬编码到最终的可执行文件中。但对于 `String` 类型，为了支持可变的、可增长的文本，我们需要在运行时在堆上分配内存。这意味着：

- 必须在运行时向内存分配器请求内存。
- 我们需要一种在完成后将此内存返回给分配器的方式。

第一部分在我们调用 `String.from()` 时完成。第二部分正是所有权大显身手的地方：在 Auto 中，一旦拥有该内存的变量离开作用域，内存就会自动返回。Auto 会在右花括号处自动调用清理函数（类似于 Rust 的 `drop`）。

<Listing number="4-2" file-name="main.auto" caption="创建 `String` 及其自动清理">

```auto
fn main() {
    let s String = String.from("hello")
    print(s)
}
```

```rust
fn main() {
    let s: String = String::from("hello");
    println!("{}", s);
}
```

</Listing>

当 `s` 离开作用域时，Auto 会自动释放堆内存。无需手动释放。

### 变量与数据交互的移动

多个变量可以以不同的方式与相同的数据交互。让我们看看 `String` 值会发生什么：

<Listing number="4-3" file-name="main.auto" caption="移动语义 —— `s1` 在赋值给 `s2` 后失效">

```auto
fn main() {
    let s1 String = String.from("hello")
    let s2 = s1.move
    print(s2)
    // s1 is no longer valid here
}
```

```rust
fn main() {
    let s1: String = String::from("hello");
    let s2 = s1;  // s1 is moved to s2
    println!("{}", s2);
    // s1 is no longer valid here
}
```

</Listing>

在 Auto 中，`.move` 属性显式地表明所有权正在被转移。原始变量（`s1`）在移动后失效。这可以防止 _双重释放（double free）_ 错误，即两个变量都试图释放相同的堆内存。

> 注意：在许多情况下，Auto 可以推断出何时需要移动，你可以直接写 `let s2 = s1` 而不需要显式的 `.move`。然而，使用 `.move` 可以使所有权转移更加清晰和有意图性。

### 变量与数据交互的克隆

如果我们确实想要深度复制 `String` 的堆数据，可以使用 `.clone()` 方法：

<Listing number="4-4" file-name="main.auto" caption="使用 `clone` 进行深拷贝">

```auto
fn main() {
    let s1 String = String.from("hello")
    let s2 = s1.clone()
    print(f"s1 = $s1, s2 = $s2")
}
```

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1.clone();
    println!("s1 = {}, s2 = {}", s1, s2);
}
```

</Listing>

当你看到对 `.clone()` 的调用时，你就知道正在执行一些可能代价高昂的代码——它创建了堆数据的完整副本。

### 仅栈数据：复制

在编译时大小已知的类型完全存储在栈上，因此复制实际值非常快。没有理由阻止原始变量在赋值后仍然有效：

<Listing number="4-5" file-name="main.auto" caption="仅栈数据被复制，而非移动">

```auto
fn main() {
    let x = 5
    let y = x
    print(f"x = $x, y = $y")
}
```

```rust
fn main() {
    let x = 5;
    let y = x;
    println!("x = {}, y = {}", x, y);
}
```

</Listing>

`x` 和 `y` 都有效，因为整数实现了 `Copy` 特征（trait）。这同样适用于：

- 所有整数类型
- 布尔类型（`bool`）
- 所有浮点类型
- 字符类型（`char`）
- 元组，如果它们只包含同样实现了 `Copy` 的类型

### 所有权与函数

将变量传递给函数会移动或复制它，就像赋值一样：

<Listing number="4-6" file-name="main.auto" caption="带有所有权和作用域的函数">

```auto
fn take_ownership(s String) {
    print(f"took ownership of: $s")
}

fn make_copy(i int) {
    print(f"made copy of: $i")
}

fn main() {
    let s String = String.from("hello")
    take_ownership(s)
    // s is no longer valid here — ownership moved into function

    let x = 5
    make_copy(x)
    // x is still valid — integers are Copy types
}
```

```rust
fn take_ownership(s: String) {
    println!("took ownership of: {}", s);
}

fn make_copy(i: i32) {
    println!("made copy of: {}", i);
}

fn main() {
    let s: String = String::from("hello");
    take_ownership(s);
    // s is no longer valid here — ownership moved into function

    let x: i32 = 5;
    make_copy(x);
    // x is still valid — integers are Copy types
}
```

</Listing>

### 返回值与作用域

返回值也可以转移所有权：

<Listing number="4-7" file-name="main.auto" caption="转移返回值的所有权">

```auto
fn give_ownership() String {
    let s String = String.from("yours")
    s.move
}

fn take_and_give_back(s String) String {
    s.move
}

fn main() {
    let s1 = give_ownership()
    print(f"s1 = $s1")

    let s2 String = String.from("hello")
    let s3 = take_and_give_back(s2)
    print(f"s3 = $s3")
}
```

```rust
fn give_ownership() -> String {
    let s = String::from("yours");
    s
}

fn take_and_give_back(s: String) -> String {
    s
}

fn main() {
    let s1 = give_ownership();
    println!("s1 = {}", s1);

    let s2 = String::from("hello");
    let s3 = take_and_give_back(s2);
    println!("s3 = {}", s3);
}
```

</Listing>

在每个函数中都获取所有权然后再返回所有权是很繁琐的。如果我们想让一个函数使用某个值但不获取所有权呢？这就是 _引用（reference）_ 的用武之地。

## 引用与借用

上面代码的问题在于，我们必须将 `String` 返回给调用函数，以便在调用后仍能使用它。相反，我们可以提供一个指向 `String` 值的 _引用_。引用类似于指针，它是一个地址，我们可以通过它访问存储在该地址的数据；该数据由其他变量拥有。与指针不同的是，引用保证指向某个特定类型的有效值。

在 Auto 中，你使用 `.view` 属性（用于不可变借用）或 `.mut` 属性（用于可变借用）来创建引用：

| Auto | Rust | 含义 |
|------|------|------|
| `s.view` | `&s` | 不可变引用（借用） |
| `s.mut` | `&mut s` | 可变引用（借用） |
| `s.move` | `s` | 所有权转移（移动） |

### 使用 `.view` 进行不可变借用

以下是如何定义和使用一个 `calculate_length` 函数，该函数借用 `String` 而不是获取所有权：

<Listing number="4-8" file-name="main.auto" caption="使用 `.view` 借用值而不获取所有权">

```auto
fn calculate_length(s String) int {
    s.length()
}

fn main() {
    let s1 String = String.from("hello")
    let len = calculate_length(s1.view)
    print(f"The length of '$s1' is $len.")
}
```

```rust
fn calculate_length(s: &str) -> usize {
    s.len()
}

fn main() {
    let s1 = String::from("hello");
    let len = calculate_length(&s1);
    println!("The length of '{}' is {}.", s1, len);
}
```

</Listing>

`.view` 属性创建一个不可变引用。因为引用不拥有数据，所以 `s1` 在函数调用后仍然有效。创建引用的行为被称为 _借用（borrowing）_——就像现实生活中一样，如果一个人拥有某样东西，你可以向他借用。用完之后，你要归还它。你并不拥有它。

### 使用 `.mut` 进行可变借用

我们还可以使用 `.mut` 属性来 _可变地_ 借用一个值：

<Listing number="4-9" file-name="main.auto" caption="使用 `.mut` 借用并修改值">

```auto
fn append_world(s String) {
    s.append(" world")
}

fn main() {
    var s1 String = String.from("hello")
    append_world(s1.mut)
    print(s1)
}
```

```rust
fn append_world(s: &mut String) {
    s.push_str(" world");
}

fn main() {
    let mut s1 = String::from("hello");
    append_world(&mut s1);
    println!("{}", s1);
}
```

</Listing>

可变引用有一个重要的限制：如果你对一个值有可变引用，你就不能再拥有对该值的其他引用。这可以在编译时防止 _数据竞争（data race）_。

### 借用规则

Auto 强制执行与 Rust 相同的借用规则：

1. 在任何给定时间，你可以拥有 _一个_ 可变引用 _或_ 任意数量的不可变引用。
2. 引用必须始终有效。

<Listing number="4-10" file-name="main.auto" caption="允许多个不可变借用">

```auto
fn main() {
    let s String = String.from("hello")

    let r1 = s.view
    let r2 = s.view
    print(f"r1 = $r1, r2 = $r2")
    // Multiple immutable borrows are allowed
}
```

```rust
fn main() {
    let s = String::from("hello");

    let r1 = &s;
    let r2 = &s;
    println!("r1 = {}, r2 = {}", r1, r2);
    // Multiple immutable borrows are allowed
}
```

</Listing>

这是没有问题的，因为多个不可变引用不会互相影响——只读取数据的人无法影响其他人读取数据。

但以下代码无法编译：

```auto,ignore,does_not_compile
fn main() {
    var s String = String.from("hello")
    let r1 = s.mut
    let r2 = s.mut   // ERROR: cannot borrow `s` as mutable more than once
    print(f"r1 = $r1, r2 = $r2")
}
```

```rust,ignore,does_not_compile
fn main() {
    let mut s = String::from("hello");
    let r1 = &mut s;
    let r2 = &mut s; // ERROR: cannot borrow `s` as mutable more than once
    println!("r1 = {}, r2 = {}", r1, r2);
}
```

### 悬垂引用

Auto 的编译器保证引用永远不会 _悬垂_——也就是说，引用永远不会指向已被释放的内存。如果你尝试创建悬垂引用（dangling reference），编译器会在编译时捕获它。

### Auto 与 Rust：显式生命周期标注

Auto 和 Rust 之间的一个关键区别是 Auto 不需要显式的 _生命周期标注（lifetime annotation）_。在 Rust 中，返回引用的函数有时需要生命周期参数（例如 `fn first_word<'a>(s: &'a str) -> &'a str`）。Auto 的编译器自动执行 _生命周期推断（lifetime inference）_，类似于它推断类型的方式。这消除了一个重要的复杂性来源，同时保持了相同的安全保证。

## 切片类型

_切片（slice）_ 允许你引用集合中一段连续的元素序列。切片是一种引用，因此它不具有所有权。

### 字符串切片

_字符串切片（string slice）_ 是对 `String` 一部分的引用：

<Listing number="4-11" file-name="main.auto" caption="使用索引查找第一个单词（有问题的方式）">

```auto
fn first_word(s String) int {
    let bytes = s.bytes()
    var i = 0
    for b in bytes {
        if b == 32 {
            return i
        }
        i = i + 1
    }
    return s.length()
}

fn main() {
    var s String = String.from("hello world")
    let word = first_word(s.view)
    print(f"first word ends at index $word")

    s.clear()
    // word is now a stale index — the string has changed!
    print(f"stale index = $word")
}
```

```rust
fn first_word(s: &str) -> usize {
    let bytes = s.as_bytes();
    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return i;
        }
    }
    s.len()
}

fn main() {
    let mut s = String::from("hello world");
    let word = first_word(&s);
    println!("first word ends at index {}", word);

    s.clear();
    // word is now a stale index — the string has changed!
    println!("stale index = {}", word);
}
```

</Listing>

返回索引的问题在于，如果字符串发生变化，索引就会变得过时。切片通过将引用与原始数据绑定来解决这个问题。

<Listing number="4-12" file-name="main.auto" caption="使用字符串切片查找第一个单词">

```auto
fn first_word_slice(s String) String {
    let bytes = s.bytes()
    var i = 0
    for b in bytes {
        if b == 32 {
            return s[0..i]
        }
        i = i + 1
    }
    return s[0..s.length()]
}

fn main() {
    let s String = String.from("hello world")
    let word = first_word_slice(s.view)
    print(f"first word: $word")
}
```

```rust
fn first_word_slice(s: &str) -> &str {
    let bytes = s.as_bytes();
    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }
    &s[..]
}

fn main() {
    let s = String::from("hello world");
    let word = first_word_slice(&s);
    println!("first word: {}", word);
}
```

</Listing>

Auto 使用与 Rust 相同的范围语法来表示切片：`s[0..5]`、`s[3..]`、`s[..5]`、`s[..]`。

### 字符串字面量作为切片

字符串字面量存储在二进制文件中。它们的类型实际上是字符串切片——它们是指向预分配数据的不可变引用。

### 数组切片

切片不仅适用于字符串，也适用于数组：

<Listing number="4-13" file-name="main.auto" caption="数组切片">

```auto
fn main() {
    let a = [1, 2, 3, 4, 5]
    let slice = a[1..3]
    print(f"slice = $slice")
}
```

```rust
fn main() {
    let a = [1, 2, 3, 4, 5];
    let slice = &a[1..3];
    println!("slice = {:?}", slice);
}
```

</Listing>

此切片在 Auto 中的类型为 `[]int`（相当于 Rust 中的 `&[i32]`）。它的工作方式与字符串切片相同，通过存储对第一个元素的引用和长度来实现。

## 总结

所有权、借用和切片的概念确保了 Auto 程序在编译时的内存安全。Auto 为你提供了与 Rust 相同的内存控制能力，但语法更加精简：

| 概念 | Auto | Rust |
|------|------|------|
| 不可变借用 | `s.view` | `&s` |
| 可变借用 | `s.mut` | `&mut s` |
| 转移所有权 | `s.move` | `s` |
| 深拷贝 | `s.clone()` | `s.clone()` |
| 生命周期标注 | （推断） | `'a`, `'b` |
| 字符串切片 | `s[0..5]` | `&s[0..5]` |

数据的所有者在其离开作用域时会自动清理该数据，因此你不必为了获得内存安全而编写和调试额外的代码。所有权影响了 Auto 许多其他部分的工作方式，因此我们将在本书的其余部分继续讨论这些概念。

让我们继续第五章，看看如何使用 Auto 的 `type` 关键字将数据组织在一起。
