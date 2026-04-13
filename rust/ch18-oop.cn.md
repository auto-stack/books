# Auto 中的面向对象模式

面向对象编程（OOP）是一种程序建模方式。对象作为编程概念最早出现在 20 世纪 60 年代的 Simula 编程语言中。许多相互竞争的定义描述了什么是 OOP，按照某些定义，Auto 是面向对象的，但按照另一些定义则不是。在本章中，我们将探讨通常被认为面向对象的某些特征，以及这些特征如何转化为惯用的 Auto 代码。

Auto 提供了三个实现 OOP 风格模式的关键机制：

- **`spec`** — 规范定义共享行为（类似于 Rust 的 `trait`）
- **`is`** — 类型组合和行为契约（替代继承）
- **`has`** — 通过组合委托行为

我们还将展示如何在 Auto 中实现面向对象设计模式，并讨论这样做与利用 Auto 自身优势实现解决方案之间的权衡。

## 面向对象语言的特征

在编程社区中，对于一种语言必须具备哪些特征才能被认为是面向对象的，并没有共识。Auto 受到多种编程范式的影响，包括 OOP；例如，我们在第 13 章中探讨了来自函数式编程的特性。可以说，OOP 语言共享某些常见特征——即对象、封装和继承。让我们看看每个特征意味着什么以及 Auto 是否支持它。

### 对象包含数据和行为

《设计模式：可复用面向对象软件的基础》（Erich Gamma、Richard Helm、Ralph Johnson 和 John Vlissides 合著，Addison-Wesley 1994 年出版）一书被俗称为"四人帮"（GoF）书，它这样定义 OOP：

> 面向对象程序由对象组成。__对象__同时封装了数据和操作这些数据的过程。这些过程通常被称为__方法__或__操作__。

按照这个定义，Auto 是面向对象的：类型有数据，`ext` 块为类型提供方法。尽管带有方法的类型在 Auto 中不被称为"对象"，但它们提供了四人帮定义的对象所具有的相同功能。

<Listing number="18-1" file-name="src/lib.at" caption="封装数据和行为的类型">

```auto
pub type AveragedCollection {
    list List<int>
    average f64
}

ext AveragedCollection {
    pub fn new() AveragedCollection {
        AveragedCollection(list: List.new(), average: 0.0)
    }

    pub fn add(mut, value int) {
        .list.push(value)
        .update_average()
    }

    pub fn remove(mut) ?int {
        let result = .list.pop()
        if let Some(value) = result {
            .update_average()
        }
        result
    }

    pub fn average() f64 {
        .average
    }

    fn update_average(mut) {
        let total = .list.fold(0, (acc, x) => acc + x)
        .average = total as f64 / .list.len() as f64
    }
}
```

```rust
pub struct AveragedCollection {
    list: Vec<i32>,
    average: f64,
}

impl AveragedCollection {
    pub fn new() -> AveragedCollection {
        AveragedCollection { list: Vec::new(), average: 0.0 }
    }

    pub fn add(&mut self, value: i32) {
        self.list.push(value);
        self.update_average();
    }

    pub fn remove(&mut self) -> Option<i32> {
        let result = self.list.pop();
        if result.is_some() {
            self.update_average();
        }
        result
    }

    pub fn average(&self) -> f64 {
        self.average
    }

    fn update_average(&mut self) {
        let total: i32 = self.list.iter().sum();
        self.average = total as f64 / self.list.len() as f64;
    }
}
```

</Listing>

`type` 关键字定义带有字段的数据结构，`ext` 块附加行为。这就是 Auto 中传统 OOP 语言类的等价物。

### 封装隐藏实现细节

与 OOP 相关的另一个方面是_封装_的概念，即对象的实现细节不能被使用该对象的代码访问。因此，与对象交互的唯一方式是通过其公共 API。

在代码清单 18-1 中，`list` 和 `average` 字段在 Auto 中默认是私有的。只有标记为 `pub` 的方法才能从类型外部访问。`update_average` 方法是私有的——它是一个实现细节。

我们在第 7 章讨论了如何控制封装：我们可以使用 `pub` 关键字来决定代码中哪些模块、类型、函数和方法应该是公共的，默认情况下其他所有内容都是私有的。

因为我们封装了 `AveragedCollection` 的实现细节，我们可以在未来轻松更改诸如数据结构等方面。例如，我们可以用 `Set<int>` 替代 `List<int>` 作为 `list` 字段。只要 `add`、`remove` 和 `average` 公共方法的签名保持不变，使用 `AveragedCollection` 的代码就不需要更改。

如果封装是一种语言被认为是面向对象的必要方面，那么 Auto 满足这个要求。

### 继承：被组合和规范取代

_继承_是一种机制，通过它对象可以从另一个对象的定义中继承元素，从而获得父对象的数据和行为，无需再次定义。

如果一种语言必须具备继承才能被认为是面向对象的，那么 Auto 不是这样的语言。无法定义一个继承父类型字段和方法实现的类型。

然而，Auto 提供了强大的替代方案：

1. **带默认实现的 `spec`** — 用于代码复用（类似 Rust 的 trait）
2. **`is` 组合** — 用于类型关系（替代继承）
3. **`has` 委托** — 将行为转发给包含的类型

你选择继承主要有两个原因。一是代码复用：你可以为一种类型实现特定行为，继承使你能够为不同的类型复用该实现。在 Auto 中，你可以通过 `spec` 默认实现实现这一点。

使用继承的另一个原因与类型系统有关：使子类型能够在与父类型相同的地方使用。这也被称为_多态_。在 Auto 中，你通过 `spec` 约束和泛型类型实现这一点。

### 多态

_多态_意味着如果多个对象共享某些特征，你可以在运行时互相替换它们。

Auto 使用泛型来抽象不同的可能类型，使用 `spec` 约束来施加这些类型必须提供什么。这有时被称为_有界参数多态_，与 Rust 采用的方法相同。

## `is`/`has`/`spec` 三角关系

Auto 的 OOP 方法以三个协同工作的关键字为中心：

| 关键字 | 用途 | OOP 等价物 |
|--------|------|-----------|
| `spec` | 定义共享行为 | 接口 / Trait |
| `is` | 组合类型，声明契约 | 继承（类型关系） |
| `has` | 通过组合委托行为 | 组合 + 委托 |

### `spec`：定义共享行为

`spec` 定义了一组类型必须实现的方法。这与 Rust 的 `trait` 或 Java/Go 中的接口完全相同：

<Listing number="18-2" file-name="src/lib.at" caption="定义带默认实现的规范">

```auto
pub spec Summary {
    fn summarize() String {
        "(阅读更多...)"
    }
}
```

```rust
pub trait Summary {
    fn summarize(&self) -> String {
        String::from("(Read more...)")
    }
}
```

</Listing>

类型使用 `spec ... for Type` 语法实现规范：

<Listing number="18-3" file-name="src/lib.at" caption="为类型实现规范">

```auto
type Article {
    title String
    author String
    content String
}

spec Summary for Article {
    fn summarize() String {
        f"${.title} by ${.author}"
    }
}
```

```rust
pub struct Article {
    pub title: String,
    pub author: String,
    pub content: String,
}

impl Summary for Article {
    fn summarize(&self) -> String {
        format!("{} by {}", self.title, self.author)
    }
}
```

</Listing>

### `is`：类型组合和契约

`is` 关键字有两个用途：

1. **组合类型** — 将一个类型的字段嵌入另一个类型
2. **声明规范契约** — 声明一个类型满足某个规范

<Listing number="18-4" file-name="src/main.at" caption="使用 `is` 进行类型组合">

```auto
type Animal {
    name String
    age int
}

type Dog {
    is Animal          // Dog 拥有 Animal 的所有字段
    breed String
}

fn main() {
    let dog = Dog(name: "Rex", age: 3, breed: "German Shepherd")
    print(f"${dog.name} is ${dog.age} years old")  // 直接访问 Animal 字段
    print(f"Breed: ${dog.breed}")
}
```

```rust
struct Animal {
    name: String,
    age: i32,
}

struct Dog {
    animal: Animal,    // 手动组合
    breed: String,
}

fn main() {
    let dog = Dog {
        animal: Animal { name: String::from("Rex"), age: 3 },
        breed: String::from("German Shepherd"),
    };
    println!("{} is {} years old", dog.animal.name, dog.animal.age);
    println!("Breed: {}", dog.breed);
}
```

</Listing>

在 Rust 中，组合需要访问嵌套字段（`dog.animal.name`）。在 Auto 中，`is` 扁平化组合——`dog.name` 可以直接使用，因为 `Dog is Animal`。

你也可以使用 `is` 来声明类型实现了某个规范：

```auto
type Dog {
    is Animal
    is Summary       // 声明 Dog 实现了 Summary
    breed String
}
```

### `has`：通过组合委托

`has` 关键字将方法实现委托给包含的类型：

<Listing number="18-5" file-name="src/main.at" caption="使用 `has` 进行委托">

```auto
type Engine {
    horsepower int
}

ext Engine {
    fn start() {
        print("Engine started!")
    }

    fn stop() {
        print("Engine stopped!")
    }
}

type Car {
    has Engine            // Car 委托 Engine 的方法
    make String
    model String
}

fn main() {
    let car = Car(
        horsepower: 200,
        make: "Toyota",
        model: "Camry"
    )
    car.start()           // 委托给 Engine.start()
    car.stop()            // 委托给 Engine.stop()
}
```

```rust
struct Engine {
    horsepower: i32,
}

impl Engine {
    fn start(&self) {
        println!("Engine started!");
    }

    fn stop(&self) {
        println!("Engine stopped!");
    }
}

struct Car {
    engine: Engine,
    make: String,
    model: String,
}

impl Car {
    fn start(&self) {
        self.engine.start();    // 手动委托
    }

    fn stop(&self) {
        self.engine.stop();     // 手动委托
    }
}

fn main() {
    let car = Car {
        engine: Engine { horsepower: 200 },
        make: String::from("Toyota"),
        model: String::from("Camry"),
    };
    car.start();
    car.stop();
}
```

</Listing>

在 Rust 中，你必须手动编写委托方法（`self.engine.start()`）。Auto 的 `has` 关键字自动将方法调用转发给包含的类型。

### `is` vs `has`

| 特性 | `is` | `has` |
|------|------|-------|
| 用途 | 组合字段 | 委托行为 |
| 字段访问 | 扁平化（直接） | 通过字段 |
| 方法委托 | 否 | 是 |
| 多重性 | 一个类型可以 `is` 多个类型 | 一个类型可以 `has` 多个类型 |
| 类比 | 继承（数据） | 组合（行为） |

当你想共享数据结构时使用 `is`。当你想共享行为但不暴露内部类型的字段时使用 `has`。

## 使用规范实现多态

### 规范对象：动态派发

与 Rust 的 `dyn Trait` 一样，Auto 通过规范对象支持动态派发。当你需要一个都实现同一规范的异构类型集合时，使用规范对象：

<Listing number="18-6" file-name="src/lib.at" caption="使用规范对象构建 GUI 库">

```auto
pub spec Draw {
    fn draw()
}

pub type Screen {
    components List<Box<dyn Draw>>
}

ext Screen {
    pub fn run() {
        for component in .components {
            component.draw()
        }
    }
}
```

```rust
pub trait Draw {
    fn draw(&self);
}

pub struct Screen {
    pub components: Vec<Box<dyn Draw>>,
}

impl Screen {
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw();
        }
    }
}
```

</Listing>

`dyn Draw` 语法创建一个_规范对象_——对实现 `Draw` 规范的任何类型的引用。这与 Rust 的 `dyn Trait` 完全类似。

### 为具体类型实现规范

<Listing number="18-7" file-name="src/lib.at" caption="为 `Button` 实现 `Draw`">

```auto
pub type Button {
    width int
    height int
    label String
}

spec Draw for Button {
    fn draw() {
        // 实际绘制按钮的代码
    }
}
```

```rust
pub struct Button {
    pub width: u32,
    pub height: u32,
    pub label: String,
}

impl Draw for Button {
    fn draw(&self) {
        // 实际绘制按钮的代码
    }
}
```

</Listing>

现在 `Screen` 可以同时持有 `Button` 和其他任何实现 `Draw` 的类型：

<Listing number="18-8" file-name="src/main.at" caption="使用规范对象的异构类型">

```auto
use gui::{Button, Screen, Draw}

type SelectBox {
    width int
    height int
    options List<String>
}

spec Draw for SelectBox {
    fn draw() {
        // 实际绘制选择框的代码
    }
}

fn main() {
    let screen = Screen(components: [
        Box.new(SelectBox(
            width: 75,
            height: 10,
            options: ["Yes", "Maybe", "No"]
        )),
        Box.new(Button(
            width: 50,
            height: 10,
            label: "OK"
        )),
    ])

    screen.run()
}
```

```rust
use gui::{Button, Screen, Draw};

struct SelectBox {
    width: u32,
    height: u32,
    options: Vec<String>,
}

impl Draw for SelectBox {
    fn draw(&self) {
        // 实际绘制选择框的代码
    }
}

fn main() {
    let screen = Screen {
        components: vec![
            Box::new(SelectBox {
                width: 75,
                height: 10,
                options: vec![
                    String::from("Yes"),
                    String::from("Maybe"),
                    String::from("No"),
                ],
            }),
            Box::new(Button {
                width: 50,
                height: 10,
                label: String::from("OK"),
            }),
        ],
    };

    screen.run();
}
```

</Listing>

### 静态派发 vs 动态派发

当你使用带规范约束的泛型时，Auto 执行_静态派发_——编译器为每个具体类型生成专门的代码。这与 Rust 中的单态化相同：

```auto
// 静态派发：每个 T 获得自己的编译版本
fn draw_all<T Draw>(items List<T>) {
    for item in items {
        item.draw()
    }
}
```

当你使用规范对象（`dyn Draw`）时，Auto 执行_动态派发_——调用的方法在运行时通过虚表确定：

```auto
// 动态派发：方法在运行时查找
fn draw_all(items List<Box<dyn Draw>>) {
    for item in items {
        item.draw()
    }
}
```

| 方面 | 静态派发（泛型） | 动态派发（`dyn`） |
|------|----------------|------------------|
| 性能 | 更快（可内联） | 轻微开销（虚表查找） |
| 灵活性 | 每次调用单一类型 | 每次调用多种类型 |
| 二进制大小 | 更大（单态化） | 更小 |
| 何时使用 | 类型统一时 | 类型混合时 |

## Auto 中的状态模式

一个经典的 OOP 设计模式是_状态模式_，其中对象的行为根据其内部状态而改变。让我们实现一个博客文章工作流，它经历以下状态：草稿 → 审核 → 发布。

### 实现状态模式

<Listing number="18-9" file-name="src/lib.at" caption="使用状态模式的博客文章工作流">

```auto
type Post {
    state Box<dyn State>
    content String
}

spec State {
    fn request_review() Box<dyn State>
    fn approve() Box<dyn State>
    fn content() String {
        ""  // 默认：无内容
    }
}

type Draft {}

spec State for Draft {
    fn request_review() Box<dyn State> {
        Box.new(PendingReview())
    }

    fn approve() Box<dyn State> {
        Box.new(Draft())  // 不能批准草稿
    }
}

type PendingReview {}

spec State for PendingReview {
    fn request_review() Box<dyn State> {
        Box.new(PendingReview())  // 保持审核状态
    }

    fn approve() Box<dyn State> {
        Box.new(Published())
    }
}

type Published {}

spec State for Published {
    fn content() String {
        .content  // 返回实际内容
    }
}

ext Post {
    fn new() Post {
        Post(
            state: Box.new(Draft()),
            content: ""
        )
    }

    fn add_text(mut, text String) {
        .content += text
    }

    fn request_review(mut) {
        .state = .state.request_review()
    }

    fn approve(mut) {
        .state = .state.approve()
    }

    fn content() String {
        .state.content()
    }
}
```

```rust
pub struct Post {
    state: Option<Box<dyn State>>,
    content: String,
}

trait State {
    fn request_review(self: Box<Self>) -> Option<Box<dyn State>>;
    fn approve(self: Box<Self>) -> Option<Box<dyn State>>;
    fn content<'a>(&self, _post: &'a Post) -> &'a str {
        ""
    }
}

struct Draft {}

impl State for Draft {
    fn request_review(self: Box<Self>) -> Option<Box<dyn State>> {
        Some(Box::new(PendingReview {}))
    }
    fn approve(self: Box<Self>) -> Option<Box<dyn State>> {
        Some(self)
    }
}

struct PendingReview {}

impl State for PendingReview {
    fn request_review(self: Box<Self>) -> Option<Box<dyn State>> {
        Some(self)
    }
    fn approve(self: Box<Self>) -> Option<Box<dyn State>> {
        Some(Box::new(Published {}))
    }
}

struct Published {}

impl State for Published {
    fn content<'a>(&self, post: &'a Post) -> &'a str {
        &post.content
    }
}

impl Post {
    pub fn new() -> Post {
        Post {
            state: Some(Box::new(Draft {})),
            content: String::new(),
        }
    }

    pub fn add_text(&mut self, text: &str) {
        self.content.push_str(text);
    }

    pub fn request_review(&mut self) {
        if let Some(s) = self.state.take() {
            self.state = Some(s.request_review());
        }
    }

    pub fn approve(&mut self) {
        if let Some(s) = self.state.take() {
            self.state = Some(s.approve());
        }
    }

    pub fn content(&self) -> &str {
        self.state.as_ref().unwrap().content(self)
    }
}
```

</Listing>

使用文章：

<Listing number="18-10" file-name="src/main.at" caption="使用博客文章状态机">

```auto
fn main() {
    let post = Post.new()
    post.add_text("I ate a salad for lunch today")

    post.request_review()
    post.approve()

    print(post.content())  // I ate a salad for lunch today
}
```

```rust
fn main() {
    let mut post = Post::new();
    post.add_text("I ate a salad for lunch today");

    post.request_review();
    post.approve();

    assert_eq!("I ate a salad for lunch today", post.content());
}
```

</Listing>

### 将状态编码到类型系统中

Auto 的 `is` 关键字提供了一种替代方案：将状态直接编码到类型系统中。我们不为运行时状态转换使用不同的类型，而是为每个状态使用不同的类型：

<Listing number="18-11" file-name="src/main.at" caption="将状态编码到类型系统中">

```auto
type DraftPost {
    content String
}

ext DraftPost {
    fn add_text(mut, text String) {
        .content += text
    }

    fn request_review() ReviewPost {
        ReviewPost(content: .content)
    }
}

type ReviewPost {
    content String
}

ext ReviewPost {
    fn approve() PublishedPost {
        PublishedPost(content: .content)
    }

    fn reject() DraftPost {
        DraftPost(content: .content)
    }
}

type PublishedPost {
    content String
}

ext PublishedPost {
    fn content() String {
        .content
    }
}
```

```rust
pub struct DraftPost {
    content: String,
}

impl DraftPost {
    pub fn add_text(&mut self, text: &str) {
        self.content.push_str(text);
    }

    pub fn request_review(self) -> PendingReviewPost {
        PendingReviewPost {
            content: self.content,
        }
    }
}

pub struct PendingReviewPost {
    content: String,
}

impl PendingReviewPost {
    pub fn approve(self) -> Post {
        Post {
            content: self.content,
        }
    }
}

pub struct Post {
    content: String,
}

impl Post {
    pub fn content(&self) -> &str {
        &self.content
    }
}
```

</Listing>

这种方法有一个显著优势：_类型系统_在编译时防止无效操作。你不能对 `DraftPost` 调用 `content()`——它不存在于该类型上。你不能对 `DraftPost` 调用 `approve()`——只有 `request_review()` 可用。编译器强制执行状态转换。

用法：

```auto
fn main() {
    let draft = DraftPost(content: "")
    draft.add_text("I ate a salad for lunch today")

    let review = draft.request_review()
    let published = review.approve()

    print(published.content())
}
```

```rust
fn main() {
    let mut draft = DraftPost { content: String::new() };
    draft.add_text("I ate a salad for lunch today");

    let review = draft.request_review();
    let published = review.approve();

    println!("{}", published.content());
}
```

这是惯用的 Auto 方法：使用类型系统使非法状态不可表示，而不是依赖运行时检查。

## `is`/`has`/`spec` vs Rust 的 OOP

| OOP 概念 | Rust | Auto |
|----------|------|------|
| 接口 / Trait | `trait` | `spec` |
| 实现 | `impl Trait for Type` | `spec Trait for Type` |
| 动态派发 | `dyn Trait` | `dyn Spec` |
| 组合 | 手动：`self.inner.method()` | `has`：自动委托 |
| 字段嵌入 | 手动：`self.inner.field` | `is`：扁平化访问 |
| 默认方法 | `trait` 带默认方法体 | `spec` 带默认方法体 |
| 无继承 | 无继承 | 无继承（使用 `is`/`has`） |
| 状态模式 | `Box<dyn State>` | `dyn State` 或类型状态 |

Auto 的 `is` 和 `has` 关键字消除了 Rust 在组合和委托时所需的样板代码。在 Rust 中，组合两个结构体并委托方法需要手动编写包装方法。在 Auto 中，`has` 自动生成这些包装器。

## 面向对象模式速查表

| 功能 | Auto | Rust |
|------|------|------|
| 定义接口 | `spec Name { }` | `trait Name { }` |
| 实现接口 | `spec Name for Type { }` | `impl Name for Type { }` |
| 动态派发 | `dyn Spec` | `dyn Trait` |
| 组合字段 | `is Type` | 手动嵌入 |
| 委托方法 | `has Type` | 手动委托 |
| 默认方法 | spec 中的方法体 | trait 中的方法体 |
| 封装 | `pub` / 默认私有 | `pub` / 默认私有 |
| 多态 | 泛型 + spec 约束 | 泛型 + trait 约束 |

## 总结

Auto 通过一组功能组合支持面向对象模式：

1. **`type` 和 `ext`** — 封装数据和行为，像对象一样
2. **封装** — `pub` 控制可见性，字段默认私有
3. **`spec`** — 定义共享行为，像接口或 trait
4. **`is`** — 通过扁平化字段访问组合类型
5. **`has`** — 通过自动方法转发委托行为
6. **`dyn Spec`** — 异构集合的动态派发
7. **类型状态模式** — 将状态编码到类型系统中实现编译时安全

Auto 故意避免继承，转而使用组合（`is`/`has`）和行为契约（`spec`）。这产生了更灵活的设计，类型只共享它们明确选择加入的行为，类型系统在编译时而非运行时捕获无效的状态转换。

在下一章，我们将探讨 Auto 使用 `is` 关键字的模式匹配，以及它与 Rust 的 `match` 表达式的比较。
