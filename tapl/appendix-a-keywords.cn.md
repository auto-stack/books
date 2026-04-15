# 附录 A：关键字参考

本附录按类别列出 Auto 语言的所有关键字、运算符和内置构造。每个条目包含一行描述、首次引入的章节号以及最小用法示例。

---

## 1. 声明

| 关键字 | 说明 | 章节 | 示例 |
|--------|------|------|------|
| `fn` | 定义函数或方法 | 第 3 章 | `fn add(a int, b int) int { a + b }` |
| `let` | 声明不可变绑定 | 第 2 章 | `let x = 10` |
| `var` | 声明可变绑定 | 第 2 章 | `var count = 0` |
| `const` | 声明编译期常量 | 第 2 章 | `const MAX_SIZE = 1024` |
| `type` | 定义自定义数据类型（结构体） | 第 6 章 | `type Point { x f64, y f64 }` |
| `enum` | 定义标签联合体或 C 风格枚举 | 第 7 章 | `enum Color { RED = 1, GREEN = 2 }` |
| `task` | 定义 actor 任务 | 第 15 章 | `task Counter { var count int = 0 }` |
| `mod` | 声明模块 | 第 10 章 | `mod network { ... }` |
| `use` | 导入模块或包 | 第 10 章 | `use io` |
| `use.rust` | 导入 Rust 标准库类型 | 第 10 章 | `use.rust std::collections::HashMap` |
| `import` | 从模块中导入特定项 | 第 10 章 | `import fmt::println` |
| `pub` | 将项标记为公开可见 | 第 10 章 | `pub fn greet() { ... }` |
| `static` | 将方法标记为静态（类型级）方法 | 第 6 章 | `static fn new() Counter { ... }` |

---

## 2. 控制流

| 关键字 | 说明 | 章节 | 示例 |
|--------|------|------|------|
| `if` | 条件分支 | 第 3 章 | `if x > 0 { print("positive") }` |
| `else` | `if` 的备选分支 | 第 3 章 | `if ok { ... } else { ... }` |
| `is` | 模式匹配（替代 `match`） | 第 7 章 | `is x { 0 => print("zero"), else => ... }` |
| `else`（在 `is` 中） | 模式匹配中的兜底分支 | 第 7 章 | `is val { _ => ... }` |
| `for` | 迭代循环或条件循环（替代 `while`） | 第 3 章 | `for i < 10 { i = i + 1 }` |
| `for ... in` | 遍历集合 | 第 3 章 | `for item in list { print(item) }` |
| `for ... in ..` | 范围迭代 | 第 3 章 | `for i in 0..10 { print(i) }` |
| `loop` | 无限循环 | 第 3 章 | `loop { ... }` |
| `break` | 提前退出循环 | 第 3 章 | `if done { break }` |
| `continue` | 跳过当前循环迭代 | 第 3 章 | `if skip { continue }` |
| `return` | 从函数返回值 | 第 3 章 | `return x + 1` |
| `yield` | 从迭代器或生成器产生值 | 第 19 章 | `yield item` |

---

## 3. 面向对象编程

| 关键字 | 说明 | 章节 | 示例 |
|--------|------|------|------|
| `is`（在类型定义中） | 单继承 | 第 8 章 | `type Hawk is Bird { speed f64 }` |
| `has` | 组合与自动委托 | 第 8 章 | `type Car has Engine { brand str }` |
| `spec` | 定义行为契约（trait） | 第 8 章 | `spec Drawable { fn draw() }` |
| `as` | 为类型实现 spec | 第 8 章 | `ext Circle as Drawable { ... }` |
| `ext` | 为类型定义方法（后置扩展） | 第 6 章 | `ext Point { fn distance() f64 { ... } }` |
| `mut fn` | 声明修改接收者的方法 | 第 8 章 | `mut fn increment() void { .count = .count + 1 }` |
| `super` | 访问父类型的字段或方法 | 第 8 章 | `super.fly()` |

---

## 4. 错误处理

| 关键字 | 说明 | 章节 | 示例 |
|--------|------|------|------|
| `?T` | 可选（可空）类型 | 第 9 章 | `fn find(id int) ?User { ... }` |
| `!T` | 错误传播结果类型 | 第 9 章 | `fn read(path str) !str { ... }` |
| `?`（运算符） | 传播错误或解包值 | 第 9 章 | `let data = fs.read("f.txt")?` |
| `!`（在函数上） | 将函数标记为可传播错误 | 第 9 章 | `fn main() ! { ... }` |
| `try` | 开始 try 块进行异常式错误处理 | 第 9 章 | `try { risky_operation() }` |
| `catch` | 捕获 try 块中的错误 | 第 9 章 | `catch e { print(e) }` |
| `throw` | 显式抛出错误 | 第 9 章 | `throw "something went wrong"` |
| `Some` | 构造包含数据的可选值 | 第 9 章 | `Some(42)` |
| `None` | 表示缺失的可选值 | 第 9 章 | `None` |
| `Ok` | 构造成功结果 | 第 9 章 | `Ok(value)` |
| `Err` | 构造错误结果 | 第 9 章 | `Err("not found")` |

---

## 5. 并发

| 关键字 | 说明 | 章节 | 示例 |
|--------|------|------|------|
| `spawn` | 启动新的 actor 任务 | 第 15 章 | `let handle = spawn Counter()` |
| `send` | 向 actor 发送消息 | 第 15 章 | `handle.send(Increment)` |
| `receive` | 在 actor 中接收消息 | 第 15 章 | `let msg = receive` |
| `on` | 对传入消息进行模式匹配（actor 邮箱） | 第 7、15 章 | `on Increment => .count = .count + 1` |
| `select` | 等待多个异步操作 | 第 16 章 | `select { msg => ..., timeout => ... }` |
| `task` | 定义 actor 蓝图 | 第 15 章 | `task PingPong { ... }` |
| `~T` | 蓝图类型（延迟/期约） | 第 16 章 | `fn fetch(url str) ~str { ... }` |
| `.await` | 等待异步蓝图解析完成 | 第 16 章 | `let data = fetch(url).await` |

---

## 6. 内存与所有权

| 关键字 | 说明 | 章节 | 示例 |
|--------|------|------|------|
| `view T` | 以只读方式借用值 | 第 11 章 | `fn print_name(v view User) { ... }` |
| `mut T` | 以可变方式借用值 | 第 11 章 | `fn reset(m mut Counter) { m.count = 0 }` |
| `*T` | 原始指针类型（不安全，需 `sys` 上下文） | 第 11 章 | `let ptr *int = sys addr_of(x)` |
| `move` | 显式转移所有权 | 第 12 章 | `consume(move data)` |
| `clone` | 创建值的深拷贝 | 第 12 章 | `let copy = data.clone()` |
| `free` | 手动释放值 | 第 12 章 | `free(buf)` |
| `sys` | 进入不安全上下文（底层访问） | 第 11 章 | `sys { let p = *addr }` |

---

## 7. 泛型

| 关键字 | 说明 | 章节 | 示例 |
|--------|------|------|------|
| `<T>` | 泛型类型参数 | 第 13 章 | `fn identity(x T) T { x }` |
| `<T, U>` | 多个泛型参数 | 第 13 章 | `type Pair<T, U> { first T, second U }` |
| `where` | 泛型约束子句 | 第 13 章 | `fn compare<T>(a T, b T) int where T: Ord { ... }` |
| `impl` | 在 where 子句中满足 spec 约束 | 第 13 章 | `where T: impl Drawable` |
| `List<T>` | 泛型动态数组 | 第 4、13 章 | `let list List<int> = List.new()` |
| `Map<K, V>` | 泛型哈希映射 | 第 4、13 章 | `let m Map<str, int> = {}` |
| `Result<T, E>` | 泛型结果类型 | 第 9、13 章 | `fn divide(a int, b int) Result<int, str> { ... }` |

---

## 8. 属性与元编程

| 属性 | 说明 | 章节 | 示例 |
|------|------|------|------|
| `#[test]` | 将函数标记为测试函数 | 第 18 章 | `#[test] fn test_add() { ... }` |
| `#[comptime]` | 在编译期求值函数或代码块 | 第 20 章 | `#[comptime] fn name() str { "hello" }` |
| `#[cfg(...)]` | 根据目标平台或特性进行条件编译 | 第 20 章 | `#[cfg(target_os = "linux")] fn linux_only() { ... }` |
| `#[macro]` | 定义编译期宏 | 第 20 章 | `#[macro] fn assert_eq(a, b) { ... }` |
| `#[inline]` | 提示编译器内联函数 | 第 20 章 | `#[inline] fn small_fn() int { 42 }` |
| `#[derive(...)]` | 自动生成常见 trait 实现 | 第 20 章 | `#[derive(Debug, Clone)] type Point { x f64, y f64 }` |

---

## 9. 字面量与内置类型

| 关键字 / 字面量 | 说明 | 章节 | 示例 |
|----------------|------|------|------|
| `true` | 布尔值真 | 第 2 章 | `let active = true` |
| `false` | 布尔值假 | 第 2 章 | `let done = false` |
| `nil` | 空值 / 缺失值 | 第 9 章 | `let x ?int = nil` |
| `str` | 字符串类型 | 第 2 章 | `let name str = "Auto"` |
| `int` | 默认整数类型（32 位） | 第 2 章 | `let x int = 42` |
| `f64` | 64 位浮点数类型 | 第 2 章 | `let pi f64 = 3.14` |
| `bool` | 布尔类型 | 第 2 章 | `let flag bool = true` |
| `char` | Unicode 字符类型 | 第 7 章 | `let c char = 'A'` |
| `void` | 单元类型（无有意义返回值） | 第 3 章 | `fn greet() void { print("hi") }` |
| `List<T>` | 动态数组类型 | 第 4 章 | `var items = List.new()` |
| `Map<K, V>` | 哈希映射类型 | 第 4 章 | `var m Map<str, int> = {}` |
| `Set<T>` | 哈希集合类型 | 第 4 章 | `var s Set<int> = Set.new()` |

---

## 10. 其他

| 关键字 | 说明 | 章节 | 示例 |
|--------|------|------|------|
| `self` | 访问当前实例（通过 `.` 前缀，非参数） | 第 6 章 | `.name`（等同其他语言中的 `self.name`） |
| `super` | 在继承中引用父类型 | 第 8 章 | `super.fly()` |
| `print` | 向标准输出打印值 | 第 1 章 | `print("Hello, Auto!")` |
| `automan` | Auto 的包管理器和构建工具 | 第 1 章 | `$ automan new my_project` |
| `.`（字段访问） | 访问字段或调用方法 | 第 6 章 | `point.x` / `list.len()` |
| `..`（范围） | 创建半开范围 | 第 3 章 | `for i in 0..10 { ... }` |
| `$var` | 字符串插值（变量） | 第 2 章 | `print("Hello, $name")` |
| `${expr}` | 字符串插值（表达式） | 第 2 章 | `print("result: ${a + b}")` |
| `_` | 通配符模式（忽略值） | 第 7 章 | `is x { _ => print("anything") }` |

---

## 快速交叉索引：关键字与章节对照

| 章节 | 标题 | 引入的关键字 |
|------|------|-------------|
| 1 | 入门指南 | `fn`、`print`、`automan` |
| 2 | 变量与运算符 | `let`、`var`、`const`、`true`、`false`、`str`、`int`、`f64`、`bool`、`$var` |
| 3 | 函数与控制流 | `if`、`else`、`for`、`loop`、`break`、`continue`、`return`、`void`、`..` |
| 4 | 集合与节点 | `List<T>`、`Map<K, V>`、`Set<T>` |
| 6 | 类型与 `let` | `type`、`ext`、`static`、`self`（隐式）、元组 |
| 7 | 枚举与模式匹配 | `enum`、`is`、`on`、`char`、`_` |
| 8 | 面向对象重塑 | `is`（继承）、`has`、`spec`、`as`、`mut fn`、`super` |
| 9 | 错误处理 | `?T`、`!T`、`?`、`try`、`catch`、`throw`、`Some`、`None`、`Ok`、`Err` |
| 10 | 包与模块 | `mod`、`use`、`use.rust`、`import`、`pub` |
| 11 | 引用与指针 | `view`、`mut`、`*T`、`sys`、生命周期 |
| 12 | 内存与所有权 | `move`、`clone`、`free`、所有权规则 |
| 13 | 泛型 | `<T>`、`where`、`impl`（约束）、泛型类型 |
| 15 | Actor 并发 | `spawn`、`send`、`receive`、`on`、`task`、`select` |
| 16 | 异步 `~T` | `~T`、`.await`、异步函数 |
| 17 | 智能类型转换与流式类型 | `if x is T`、联合类型、流敏感类型收窄 |
| 18 | 测试 | `#[test]`、`assert_eq`、`assert` |
| 19 | 闭包与迭代器 | `yield`、闭包、`.iter()`、`.map()`、`.filter()`、`.fold()` |
| 20 | 编译期与元编程 | `#[comptime]`、`#[cfg(...)]`、`#[macro]`、`#[inline]`、`#[derive(...)]` |
