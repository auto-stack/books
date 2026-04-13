# 引用与指针

_指针_是一个通用概念，指包含内存地址的变量。这个地址指向，或者说"指向"某些其他数据。Auto 中最常见的指针是_引用_，我们在[第 4 章][ch4]中学过。引用借用它们指向的值。它们除了引用数据外没有任何特殊功能，也没有额外开销。

而_智能指针_则是一种数据结构，它表现得像指针，但还有额外的元数据和功能。智能指针的概念并非 Rust 独有：智能指针起源于 C++，在其他语言中也存在。Rust 标准库中定义了多种智能指针，提供了超越引用的功能。Auto 通过与 Rust 的互操作共享了许多这些概念。

在 Auto 中，由于其所有权和隐式 move 的概念，引用和智能指针之间还有一个区别：引用只借用数据，而智能指针在很多情况下_拥有_它们指向的数据。

智能指针通常使用类型来实现。与普通类型不同，智能指针实现了提供指针行为的规范。`Deref` 规范允许智能指针类型的实例表现得像引用，这样你可以编写同时适用于引用和智能指针的代码。`Drop` 规范允许你自定义当智能指针实例离开作用域时运行的代码。本章将讨论这两个规范，并演示它们对智能指针为何重要。

由于智能指针模式是一个常用的通用设计模式，本章不会涵盖所有现有的智能指针。许多库都有自己的智能指针，你甚至可以编写自己的。我们将介绍最常见的智能指针模式：

- **堆分配**，在堆上分配值
- **引用计数**，允许多个所有权的类型
- **内部可变性**，在运行时而非编译时执行借用规则的类型

此外，我们还将介绍_内部可变性_模式，即不可变类型暴露修改内部值的 API。我们还会讨论引用循环：它们如何导致内存泄漏以及如何防止。

> **注意：** Auto 的智能指针类型通过 `use.rust` 机制利用 Rust 的标准库。虽然 Auto 有自己的内存模型（隐式 move 和 AutoFree），但此处描述的智能指针模式在使用 Rust 互操作时工作方式完全相同。原生 Auto 智能指针 API 计划在未来版本中提供。

让我们开始吧！

## 使用堆分配指向数据

最简单的智能指针是_盒子_（box），在 Rust 中写作 `Box<T>`。盒子允许你将数据存储在堆上而非栈上。栈上保留的是指向堆数据的指针。回顾 [第 4 章][ch4]中关于栈和堆区别的讨论。

盒子除了将数据存储在堆上而非栈上之外，没有性能开销。但它们也没有太多额外功能。你最常在以下情况使用它们：

- 当你有一个在编译时无法知道大小的类型，而你又想在一个需要确定大小的上下文中使用该类型的值
- 当你有大量数据，想要转移所有权但确保数据不会被复制
- 当你想拥有一个值，而你只关心它实现了某个特定规范，而不是具体的类型

### 在堆上存储数据

代码清单 15-1 展示了如何使用盒子在堆上存储一个 `int` 值。

<Listing number="15-1" file-name="src/main.at" caption="使用盒子在堆上存储 `int` 值">

```auto
use.rust std::boxed::Box

fn main() {
    let b = Box.new(5)
    print(f"b = ${b}")
}
```

```rust
fn main() {
    let b = Box::new(5);
    println!("b = {b}");
}
```

</Listing>

我们定义变量 `b` 为一个 `Box`，它指向堆上分配的值 `5`。这个程序会打印 `b = 5`；在这种情况下，我们可以像访问栈上的数据一样访问盒子中的数据。与任何拥有的值一样，当盒子离开作用域时（如 `b` 在 `main` 结束时），它会被释放。释放操作同时发生在盒子（存储在栈上）和它指向的数据（存储在堆上）。

### 使用盒子实现递归类型

_递归类型_的值可以将同类型的另一个值作为自身的一部分。递归类型会带来问题，因为编译器需要在编译时知道一个类型占用多少空间。然而，递归类型的值嵌套理论上可以无限继续，所以编译器无法知道该值需要多少空间。因为盒子有已知大小，我们可以通过在递归类型定义中插入盒子来启用递归类型。

作为递归类型的示例，让我们探索 cons 列表——函数式编程语言中常见的数据类型。

<Listing number="15-2" file-name="src/main.at" caption="尝试定义递归枚举（无法编译）">

```auto
// 这无法编译 — 递归类型有无限大小
enum List {
    Cons(int, List)
    Nil
}

fn main() {}
```

```rust
enum List {
    Cons(i32, List),
    Nil,
}

fn main() {}
```

</Listing>

错误显示该类型"有无限大小"。原因是 `List` 的某个变体是递归的：它直接包含自身的另一个值。因此，编译器无法确定存储 `List` 值需要多少空间。

因为 `Box<T>` 是指针，编译器始终知道 `Box<T>` 需要多少空间：指针的大小不会根据它指向的数据量而改变。这意味着我们可以在 `Cons` 变体中放一个 `Box<T>` 而不是直接放另一个 `List` 值。

<Listing number="15-3" file-name="src/main.at" caption="使用 `Box<T>` 使 `List` 具有已知大小">

```auto
use.rust std::boxed::Box

enum List {
    Cons(int, Box<List>)
    Nil
}

fn main() {
    let list = List.Cons(
        1,
        Box.new(List.Cons(
            2,
            Box.new(List.Cons(
                3,
                Box.new(List.Nil)
            ))
        ))
    )
}
```

```rust
enum List {
    Cons(i32, Box<List>),
    Nil,
}

use crate::List::{Cons, Nil};

fn main() {
    let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));
}
```

</Listing>

`Cons` 变体需要一个 `int` 的大小加上存储盒子指针数据的空间。`Nil` 变体不存储值，所以它在栈上需要的空间比 `Cons` 变体少。我们现在知道任何 `List` 值将占用一个 `int` 的大小加上盒子指针数据的大小。通过使用盒子，我们打破了无限的递归链，编译器就能计算出存储 `List` 值所需的大小。

## 将智能指针当作常规引用对待

实现 `Deref` 规范允许你自定义_解引用运算符_ `*` 的行为。通过实现 `Deref`，使智能指针可以像常规引用一样被对待，你可以编写操作引用的代码，并将其与智能指针一起使用。

### 通过指针追踪到值

常规引用是一种指针，理解指针的一种方式是将其视为指向存储在别处的值的箭头。在代码清单 15-4 中，我们创建了一个指向 `int` 值的引用，然后使用解引用运算符通过引用追踪到值。

<Listing number="15-4" file-name="src/main.at" caption="使用解引用运算符通过引用追踪值">

```auto
fn main() {
    let x = 5
    let y = &x

    assert_eq(5, x)
    assert_eq(5, *y)
}
```

```rust
fn main() {
    let x = 5;
    let y = &x;

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```

</Listing>

变量 `x` 持有一个 `int` 值 `5`。我们将 `y` 设为对 `x` 的引用。我们可以断言 `x` 等于 `5`。但是，如果要对 `y` 中的值进行断言，我们必须使用 `*y` 来追踪引用指向的值。

### 像 `Box<T>` 一样使用引用

我们可以重写代码清单 15-4 的代码，用 `Box<T>` 替代引用；在 `Box<T>` 上使用的解引用运算符与在引用上使用的方式相同。

<Listing number="15-5" file-name="src/main.at" caption="对 `Box<int>` 使用解引用运算符">

```auto
use.rust std::boxed::Box

fn main() {
    let x = 5
    let y = Box.new(x)

    assert_eq(5, x)
    assert_eq(5, *y)
}
```

```rust
fn main() {
    let x = 5;
    let y = Box::new(x);

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```

</Listing>

### 实现 `Deref` 规范

要启用 `*` 运算符的解引用功能，类型需要实现 `Deref` 规范。`Deref` 规范要求实现一个 `deref` 方法，该方法借用 `self` 并返回内部数据的引用。

<Listing number="15-6" file-name="src/main.at" caption="在 `MyBox<T>` 上实现 `Deref`">

```auto
type MyBox<T>(T)

ext MyBox {
    fn new(x T) MyBox<T> {
        MyBox(x)
    }
}

spec Deref for MyBox<T> {
    type Target = T

    fn deref() &T {
        &.0
    }
}

fn main() {
    let x = 5
    let y = MyBox.new(x)

    assert_eq(5, x)
    assert_eq(5, *y)
}
```

```rust
use std::ops::Deref;

struct MyBox<T>(T);

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        MyBox(x)
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn main() {
    let x = 5;
    let y = MyBox::new(x);

    assert_eq!(5, x);
    assert_eq!(5, *y);
}
```

</Listing>

`type Target = T` 语法为 `Deref` 规范定义了一个关联类型。我们在 `deref` 方法体中填入 `&.0`，使 `deref` 返回我们想通过 `*` 运算符访问的值的引用。

没有 `Deref` 规范，编译器只能解引用 `&` 引用。`deref` 方法使编译器能够获取任何实现了 `Deref` 的类型的值，并调用 `deref` 方法获取它知道如何解引用的引用。

当我们输入 `*y` 时，编译器实际上在幕后运行了 `*(y.deref())`。这个特性让我们编写的代码无论使用常规引用还是实现 `Deref` 的类型都能正常工作。

### Deref 强制转换

_Deref 强制转换_将实现了 `Deref` 规范的类型的引用转换为另一种类型的引用。例如，deref 强制转换可以将 `&String` 转换为 `&str`，因为 `String` 实现了返回 `&str` 的 `Deref`。当我们将特定类型值的引用作为函数参数传递，而参数类型不匹配时，deref 强制转换会自动发生。

<Listing number="15-7" file-name="src/main.at" caption="Deref 强制转换的实际应用">

```auto
fn hello(name String) {
    print(f"Hello, ${name}!")
}

fn main() {
    let m = MyBox.new(String.from("Auto"))
    hello(&m)  // deref 强制转换将 &MyBox<String> 转换为 &String
}
```

```rust
fn hello(name: &str) {
    println!("Hello, {name}!");
}

fn main() {
    let m = MyBox::new(String::from("Rust"));
    hello(&m);
}
```

</Listing>

这里我们用参数 `&m`（一个指向 `MyBox<String>` 值的引用）调用 `hello` 函数。因为 `MyBox<T>` 实现了 `Deref`，编译器可以通过调用 `deref` 将 `&MyBox<String>` 转换为 `&String`。标准库为 `String` 提供了返回字符串切片的 `Deref` 实现，编译器再次调用 `deref` 将 `&String` 转换为 `&str`，与 `hello` 函数的定义匹配。

Deref 强制转换也适用于可变引用：

1. 当 `T: Deref<Target=U>` 时，从 `&T` 到 `&U`
2. 当 `T: DerefMut<Target=U>` 时，从 `&mut T` 到 `&mut U`
3. 当 `T: Deref<Target=U>` 时，从 `&mut T` 到 `&U`

第三种情况比较特殊：编译器也会将可变引用强制转换为不可变引用。但反向_不可能_：不可变引用永远不会强制转换为可变引用。

## 使用 `Drop` 规范在清理时运行代码

对智能指针模式同样重要的第二个规范是 `Drop`，它让你可以自定义值即将离开作用域时发生的事情。你可以为任何类型实现 `Drop` 规范，该代码可用于释放文件或网络连接等资源。

在某些语言中，程序员必须在每次使用完某个类型的实例后手动调用代码来释放内存或资源。如果程序员忘记，系统可能会过载并崩溃。在 Auto 中，你可以指定当值离开作用域时运行特定的代码，编译器会自动插入这些代码。因此，你不需要在程序中到处小心放置清理代码——你仍然不会泄漏资源！

<Listing number="15-8" file-name="src/main.at" caption="实现 `Drop` 规范的类型">

```auto
type CustomSmartPointer {
    data String
}

ext CustomSmartPointer {
    fn new(data String) CustomSmartPointer {
        CustomSmartPointer(data)
    }
}

spec Drop for CustomSmartPointer {
    fn drop() {
        print(f"Dropping CustomSmartPointer with data `${.data}`!")
    }
}

fn main() {
    let c = CustomSmartPointer.new(String.from("my stuff"))
    let d = CustomSmartPointer.new(String.from("other stuff"))
    print("CustomSmartPointers created")
}
```

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data `{}`!", self.data);
    }
}

fn main() {
    let c = CustomSmartPointer {
        data: String::from("my stuff"),
    };
    let d = CustomSmartPointer {
        data: String::from("other stuff"),
    };
    println!("CustomSmartPointers created");
}
```

</Listing>

运行此程序时，我们会看到以下输出：

```text
CustomSmartPointers created
Dropping CustomSmartPointer with data `other stuff`!
Dropping CustomSmartPointer with data `my stuff`!
```

编译器在实例离开作用域时自动调用了 `drop`。变量按创建顺序的逆序被 drop，所以 `d` 在 `c` 之前被 drop。

### 使用 `drop` 提前释放值

有时你可能想提前清理一个值。一个例子是使用管理锁的智能指针：你可能想强制执行 `drop` 方法来释放锁，以便同一作用域中的其他代码可以获取锁。Auto 不允许你手动调用 `Drop` 规范的 `drop` 方法；相反，你需要使用标准库提供的 `drop()` 函数。

<Listing number="15-9" file-name="src/main.at" caption="调用 `drop()` 在值离开作用域之前显式释放">

```auto
type CustomSmartPointer {
    data String
}

spec Drop for CustomSmartPointer {
    fn drop() {
        print(f"Dropping CustomSmartPointer with data `${.data}`!")
    }
}

fn main() {
    let c = CustomSmartPointer(data: String.from("some data"))
    print("CustomSmartPointer created")
    drop(c)
    print("CustomSmartPointer dropped before the end of main")
}
```

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer with data `{}`!", self.data);
    }
}

fn main() {
    let c = CustomSmartPointer {
        data: String::from("some data"),
    };
    println!("CustomSmartPointer created");
    drop(c);
    println!("CustomSmartPointer dropped before the end of main");
}
```

</Listing>

运行此代码会打印：

```text
CustomSmartPointer created
Dropping CustomSmartPointer with data `some data`!
CustomSmartPointer dropped before the end of main
```

`Dropping` 消息出现在两个 `print` 语句之间，表明 `c` 在那时被 drop。有了 `Drop` 规范和 Auto 的所有权系统，你不需要记住清理——Auto 会自动完成。

## 引用计数：`Rc<T>`

在大多数情况下，所有权是清晰的：你确切知道哪个变量拥有给定的值。但是，有时一个值可能有多个所有者。例如，在图数据结构中，多条边可能指向同一个节点，该节点在概念上被所有指向它的边所拥有。

你必须显式启用多重所有权，使用 `Rc<T>` 类型，即_引用计数_的缩写。`Rc<T>` 类型跟踪对值的引用数量，以确定该值是否仍在使用。如果对值的引用为零，就可以在不使任何引用失效的情况下清理该值。

> **注意：** `Rc<T>` 仅用于单线程场景。当我们在[第 16 章][ch16]讨论并发时，将介绍多线程程序中如何进行引用计数。

### 使用 `Rc<T>` 共享数据

让我们回到 cons 列表的例子。这次，我们将创建两个列表，它们共享第三个列表的所有权。

<Listing number="15-10" file-name="src/main.at" caption="使用 `Rc<T>` 在两个列表之间共享所有权">

```auto
use.rust std::rc::Rc

enum List {
    Cons(int, Rc<List>)
    Nil
}

fn main() {
    let a = Rc.new(List.Cons(5, Rc.new(List.Cons(10, Rc.new(List.Nil)))))
    let b = List.Cons(3, Rc.clone(&a))
    let c = List.Cons(4, Rc.clone(&a))
}
```

```rust
use std::rc::Rc;

enum List {
    Cons(i32, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};

fn main() {
    let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
    let b = Cons(3, Rc::clone(&a));
    let c = Cons(4, Rc::clone(&a));
}
```

</Listing>

创建 `b` 时，我们不获取 `a` 的所有权，而是克隆 `a` 持有的 `Rc<List>`，将引用数从一增加到二，让 `a` 和 `b` 共享数据。创建 `c` 时也克隆 `a`，将引用数从二增加到三。

### 通过克隆增加引用计数

<Listing number="15-11" file-name="src/main.at" caption="打印引用计数">

```auto
use.rust std::rc::Rc

enum List {
    Cons(int, Rc<List>)
    Nil
}

fn main() {
    let a = Rc.new(List.Cons(5, Rc.new(List.Cons(10, Rc.new(List.Nil)))))
    print(f"count after creating a = ${Rc.strong_count(&a)}")

    let b = List.Cons(3, Rc.clone(&a))
    print(f"count after creating b = ${Rc.strong_count(&a)}")

    {
        let c = List.Cons(4, Rc.clone(&a))
        print(f"count after creating c = ${Rc.strong_count(&a)}")
    }

    print(f"count after c goes out of scope = ${Rc.strong_count(&a)}")
}
```

```rust
use std::rc::Rc;

enum List {
    Cons(i32, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};

fn main() {
    let a = Rc::new(Cons(5, Rc::new(Cons(10, Rc::new(Nil)))));
    println!("count after creating a = {}", Rc::strong_count(&a));
    let b = Cons(3, Rc::clone(&a));
    println!("count after creating b = {}", Rc::strong_count(&a));
    {
        let c = Cons(4, Rc::clone(&a));
        println!("count after creating c = {}", Rc::strong_count(&a));
    }
    println!("count after c goes out of scope = {}", Rc::strong_count(&a));
}
```

</Listing>

此代码打印：

```text
count after creating a = 1
count after creating b = 2
count after creating c = 3
count after c goes out of scope = 2
```

我们可以看到 `a` 中的 `Rc<List>` 初始引用计数为 1；每次调用 `clone`，计数增加 1。当 `c` 离开作用域时，计数减少 1。我们不需要调用函数来减少引用计数——`Drop` 实现会在 `Rc<T>` 值离开作用域时自动减少计数。

## `RefCell<T>` 与内部可变性模式

_内部可变性_是一种设计模式，允许你在存在不可变引用的情况下修改数据；通常，借用规则不允许这种操作。为了修改数据，该模式在数据结构内部使用 `sys`（等价于 Rust 的 `unsafe`）代码来绕过通常的管理修改和借用的规则。我们将在[第 20 章][ch20]进一步讨论 `sys`。

### 在运行时执行借用规则

与 `Rc<T>` 不同，`RefCell<T>` 类型表示对其持有数据的单一所有权。回顾在[第 4 章][ch4]中学到的借用规则：

- 在任何给定时间，你可以拥有_一个_可变引用或_任意数量_的不可变引用（但不能同时拥有）。
- 引用必须始终有效。

使用引用和 `Box<T>` 时，借用规则在编译时执行。使用 `RefCell<T>` 时，这些规则在_运行时_执行。使用引用时，如果违反规则，你会得到编译错误。使用 `RefCell<T>` 时，如果违反规则，程序会 panic 并退出。

以下是选择 `Box<T>`、`Rc<T>` 或 `RefCell<T>` 的原因总结：

| 类型 | 所有者 | 借用检查 | 可变性 |
|------|--------|----------|--------|
| `Box<T>` | 单一 | 编译时 | 不可变或可变 |
| `Rc<T>` | 多个 | 编译时 | 仅不可变 |
| `RefCell<T>` | 单一 | 运行时 | 不可变或可变 |

### 使用内部可变性：模拟对象

`RefCell<T>` 的一个实际用途是在测试中创建模拟对象。以下是使用 `Messenger` 规范的示例：

<Listing number="15-12" file-name="src/lib.at" caption="使用 `RefCell<T>` 在外部值不可变时修改内部值">

```auto
use.rust std::cell::RefCell

spec Messenger {
    fn send(msg String)
}

type LimitTracker<T Messenger> {
    messenger &T
    value int
    max int
}

ext LimitTracker {
    fn new(messenger &T, max int) LimitTracker<T> {
        LimitTracker(messenger, value: 0, max)
    }

    fn set_value(mut, value int) {
        .value = value
        let percentage = .value as f64 / .max as f64

        if percentage >= 1.0 {
            .messenger.send("Error: You are over your quota!")
        } else if percentage >= 0.9 {
            .messenger.send("Urgent warning: You've used up over 90% of your quota!")
        } else if percentage >= 0.75 {
            .messenger.send("Warning: You've used up over 75% of your quota!")
        }
    }
}

#[test]
fn it_sends_an_over_75_percent_warning_message() {
    type MockMessenger {
        sent_messages RefCell<List<String>>
    }

    ext MockMessenger {
        fn new() MockMessenger {
            MockMessenger(sent_messages: RefCell.new(List.new()))
        }
    }

    spec Messenger for MockMessenger {
        fn send(msg String) {
            .sent_messages.borrow_mut().push(msg)
        }
    }

    let mock_messenger = MockMessenger.new()
    var limit_tracker = LimitTracker.new(&mock_messenger, 100)

    limit_tracker.set_value(80)

    assert_eq(1, mock_messenger.sent_messages.borrow().len())
}
```

```rust
pub trait Messenger {
    fn send(&self, msg: &str);
}

pub struct LimitTracker<'a, T: Messenger> {
    messenger: &'a T,
    value: usize,
    max: usize,
}

impl<'a, T: Messenger> LimitTracker<'a, T> {
    pub fn new(messenger: &'a T, max: usize) -> LimitTracker<'a, T> {
        LimitTracker { messenger, value: 0, max }
    }

    pub fn set_value(&mut self, value: usize) {
        self.value = value;
        let percentage = self.value as f64 / self.max as f64;
        if percentage >= 1.0 {
            self.messenger.send("Error: You are over your quota!");
        } else if percentage >= 0.9 {
            self.messenger.send("Urgent warning: You've used up over 90%!");
        } else if percentage >= 0.75 {
            self.messenger.send("Warning: You've used up over 75%!");
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::RefCell;

    struct MockMessenger {
        sent_messages: RefCell<Vec<String>>,
    }

    impl MockMessenger {
        fn new() -> MockMessenger {
            MockMessenger { sent_messages: RefCell::new(vec![]) }
        }
    }

    impl Messenger for MockMessenger {
        fn send(&self, message: &str) {
            self.sent_messages.borrow_mut().push(String::from(message));
        }
    }

    #[test]
    fn it_sends_an_over_75_percent_warning_message() {
        let mock_messenger = MockMessenger::new();
        let mut limit_tracker = LimitTracker::new(&mock_messenger, 100);
        limit_tracker.set_value(80);
        assert_eq!(mock_messenger.sent_messages.borrow().len(), 1);
    }
}
```

</Listing>

`sent_messages` 字段现在是 `RefCell<List<String>>` 类型。`send` 方法对 `RefCell` 调用 `borrow_mut` 获取内部列表的可变引用。即使 `send` 接受 `self` 的不可变引用，我们仍然可以通过 `RefCell<T>` 修改内部数据。

### 组合使用 `Rc<T>` 和 `RefCell<T>`

`RefCell<T>` 的一种常见用法是与 `Rc<T>` 组合使用。回想一下，`Rc<T>` 允许你让多个所有者共享某些数据，但它只提供不可变访问。如果你有一个持有 `RefCell<T>` 的 `Rc<T>`，你就可以获得一个既有多个所有者_又_可以修改的值。

<Listing number="15-13" file-name="src/main.at" caption="使用 `Rc<RefCell<int>>` 创建可修改的 `List`">

```auto
use.rust std::cell::RefCell
use.rust std::rc::Rc

enum List {
    Cons(Rc<RefCell<int>>, Rc<List>)
    Nil
}

fn main() {
    let value = Rc.new(RefCell.new(5))

    let a = Rc.new(List.Cons(Rc.clone(&value), Rc.new(List.Nil)))

    let b = List.Cons(Rc.new(RefCell.new(3)), Rc.clone(&a))
    let c = List.Cons(Rc.new(RefCell.new(4)), Rc.clone(&a))

    *value.borrow_mut() += 10

    print(f"a after = ${a}")
    print(f"b after = ${b}")
    print(f"c after = ${c}")
}
```

```rust
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
enum List {
    Cons(Rc<RefCell<i32>>, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};

fn main() {
    let value = Rc::new(RefCell::new(5));
    let a = Rc::new(Cons(Rc::clone(&value), Rc::new(Nil)));
    let b = Cons(Rc::new(RefCell::new(3)), Rc::clone(&a));
    let c = Cons(Rc::new(RefCell::new(4)), Rc::clone(&a));
    *value.borrow_mut() += 10;
    println!("a after = {a:?}");
    println!("b after = {b:?}");
    println!("c after = {c:?}");
}
```

</Listing>

当我们打印 `a`、`b` 和 `c` 时，可以看到它们都显示修改后的值 `15` 而不是 `5`。通过使用 `RefCell<T>`，我们拥有一个外部不可变的 `List` 值，但可以在需要时修改数据。

## 引用循环可能导致内存泄漏

Auto 的内存安全保证使得意外创建永远不会被清理的内存（即_内存泄漏_）变得困难，但并非不可能。完全防止内存泄漏并非 Auto 的保证之一。我们可以通过使用 `Rc<T>` 和 `RefCell<T>` 来看到内存泄漏的可能性：可以创建引用循环，其中项相互引用。这会导致内存泄漏，因为循环中每个项的引用计数永远不会达到 0，值也永远不会被 drop。

### 创建引用循环

<Listing number="15-14" file-name="src/main.at" caption="创建两个相互指向的 `List` 值的引用循环">

```auto
use.rust std::cell::RefCell
use.rust std::rc::Rc

enum List {
    Cons(int, RefCell<Rc<List>>)
    Nil
}

ext List {
    fn tail() ?&RefCell<Rc<List>> {
        self is
            List.Cons(_, item) -> Some(item)
            List.Nil -> None
    }
}

fn main() {
    let a = Rc.new(List.Cons(5, RefCell.new(Rc.new(List.Nil))))

    print(f"a initial rc count = ${Rc.strong_count(&a)}")

    let b = Rc.new(List.Cons(10, RefCell.new(Rc.clone(&a))))

    print(f"a rc count after b creation = ${Rc.strong_count(&a)}")
    print(f"b initial rc count = ${Rc.strong_count(&b)}")

    // 创建循环：a 指向 b
    if let Some(link) = a.tail() {
        *link.borrow_mut() = Rc.clone(&b)
    }

    print(f"b rc count after changing a = ${Rc.strong_count(&b)}")
    print(f"a rc count after changing a = ${Rc.strong_count(&a)}")

    // 取消注释下一行将导致栈溢出：
    // print(f"a next item = ${a.tail()}")
}
```

```rust
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
enum List {
    Cons(i32, RefCell<Rc<List>>),
    Nil,
}

impl List {
    fn tail(&self) -> Option<&RefCell<Rc<List>>> {
        match self {
            Cons(_, item) => Some(item),
            Nil => None,
        }
    }
}

fn main() {
    let a = Rc::new(Cons(5, RefCell::new(Rc::new(Nil))));
    println!("a initial rc count = {}", Rc::strong_count(&a));
    let b = Rc::new(Cons(10, RefCell::new(Rc::clone(&a))));
    println!("a rc count after b creation = {}", Rc::strong_count(&a));
    println!("b initial rc count = {}", Rc::strong_count(&b));
    if let Some(link) = a.tail() {
        *link.borrow_mut() = Rc::clone(&b);
    }
    println!("b rc count after changing a = {}", Rc::strong_count(&b));
    println!("a rc count after changing a = {}", Rc::strong_count(&a));
}
```

</Listing>

创建循环后，`a` 和 `b` 的引用计数都是 2。`main` 结束时，`Rc<List>` 实例无法被 drop，因为它们的引用计数永远不会达到 0。内存将保持未回收状态。

### 使用 `Weak<T>` 防止引用循环

你可以通过调用 `Rc::downgrade` 创建 `Rc<T>` 中值的_弱引用_。弱引用不表示所有权关系，其计数不影响 `Rc<T>` 实例何时被清理。

<Listing number="15-15" file-name="src/main.at" caption="使用 `Weak<T>` 作为父引用的树结构">

```auto
use.rust std::cell::RefCell
use.rust std::rc::{Rc, Weak}

type Node {
    value int
    parent RefCell<Weak<Node>>
    children RefCell<List<Rc<Node>>>
}

fn main() {
    let leaf = Rc.new(Node(
        value: 3,
        parent: RefCell.new(Weak.new()),
        children: RefCell.new(List.new())
    ))

    print(f"leaf parent = ${leaf.parent.borrow().upgrade()}")

    {
        let branch = Rc.new(Node(
            value: 5,
            parent: RefCell.new(Weak.new()),
            children: RefCell.new([Rc.clone(&leaf)])
        ))

        *leaf.parent.borrow_mut() = Rc.downgrade(&branch)

        print(f"branch strong = ${Rc.strong_count(&branch)}, weak = ${Rc.weak_count(&branch)}")
        print(f"leaf strong = ${Rc.strong_count(&leaf)}, weak = ${Rc.weak_count(&leaf)}")
    }

    print(f"leaf parent = ${leaf.parent.borrow().upgrade()}")
    print(f"leaf strong = ${Rc.strong_count(&leaf)}, weak = ${Rc.weak_count(&leaf)}")
}
```

```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

#[derive(Debug)]
struct Node {
    value: i32,
    parent: RefCell<Weak<Node>>,
    children: RefCell<Vec<Rc<Node>>>,
}

fn main() {
    let leaf = Rc::new(Node {
        value: 3,
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![]),
    });
    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());
    {
        let branch = Rc::new(Node {
            value: 5,
            parent: RefCell::new(Weak::new()),
            children: RefCell::new(vec![Rc::clone(&leaf)]),
        });
        *leaf.parent.borrow_mut() = Rc::downgrade(&branch);
        println!("branch strong = {}, weak = {}",
            Rc::strong_count(&branch), Rc::weak_count(&branch));
        println!("leaf strong = {}, weak = {}",
            Rc::strong_count(&leaf), Rc::weak_count(&leaf));
    }
    println!("leaf parent = {:?}", leaf.parent.borrow().upgrade());
    println!("leaf strong = {}, weak = {}",
        Rc::strong_count(&leaf), Rc::weak_count(&leaf));
}
```

</Listing>

当内部作用域结束时，`branch` 离开作用域，`Rc<Node>` 的强引用计数减至 0，所以 `Node` 被 drop。来自 `leaf.parent` 的弱引用计数 1 不影响 `Node` 是否被 drop，因此不会产生内存泄漏！

如果我们尝试在作用域结束后访问 `leaf` 的父节点，我们会再次得到 `None`。管理计数和值 drop 的所有逻辑都内置在 `Rc<T>` 和 `Weak<T>` 及其 `Drop` 规范的实现中。

## 智能指针速查表

| 功能 | Auto | Rust |
|------|------|------|
| 堆分配 | `Box.new(v)` 通过 `use.rust` | `Box::new(v)` |
| 引用计数 | `Rc.new(v)` 通过 `use.rust` | `Rc::new(v)` |
| 内部可变性 | `RefCell.new(v)` 通过 `use.rust` | `RefCell::new(v)` |
| 解引用规范 | `spec Deref` | `impl Deref` |
| 清理规范 | `spec Drop` | `impl Drop` |
| 弱引用 | `Rc.downgrade(&v)` | `Rc::downgrade(&v)` |
| 共享 + 可变 | `Rc<RefCell<T>>` | `Rc<RefCell<T>>` |

## 总结

本章介绍了如何使用智能指针做出与 Auto 默认常规引用不同的保证和权衡：

1. **`Box<T>`** — 堆分配，单一所有权，支持递归类型
2. **`Deref` 规范** — 将智能指针当作常规引用使用，自动 deref 强制转换
3. **`Drop` 规范** — 值离开作用域时自动运行清理代码
4. **`Rc<T>`** — 引用计数，允许多个所有者共享同一数据
5. **`RefCell<T>`** — 内部可变性，运行时借用检查
6. **`Weak<T>`** — 防止可能导致内存泄漏的引用循环

在下一章，我们将探讨 Auto 的并发模型，它使用 Actor 模式而非 Rust 的线程模型。

[ch4]: ch04-ownership.md
[ch16]: ch16-concurrency.md
[ch20]: ch20-advanced.md
