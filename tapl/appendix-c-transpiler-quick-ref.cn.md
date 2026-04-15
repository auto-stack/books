# 附录 C：转译器速查手册

本附录是面向已熟悉 Rust、Python、C 或 TypeScript 的开发者的速查表。每张表的左列展示常见的 Auto 模式，右列展示其在四种目标语言中的等价写法。你可以用它快速将 Auto 语法映射到你熟悉——或者快速了解 Auto 程序转译到你所用语言后的样子。

> **提示：** 本附录仅涵盖语法映射。关于每种设计决策背后的原理，请参阅各节"另见"注释中列出的章节。

---

## C.1 变量与可变性

Auto 区分可变绑定（`var`）和不可变绑定（`let`）。类型从初始化表达式中推断。

*另见：[第 2 章 —— 变量与运算符][ch02]、[第 6 章 —— 类型与 `let`][ch06]*

| Auto | Rust | Python | C | TypeScript | 说明 |
|------|------|--------|---|------------|------|
| `var x = 5` | `let mut x: i64 = 5;` | `x = 5` | `int x = 5;` | `let x = 5;` | Auto `var` 始终可变；类型自动推断 |
| `let x = 5` | `let x: i64 = 5;` | `x = 5` | `const int x = 5;` | `const x = 5;` | Auto `let` 不可变；重新赋值会导致编译错误 |
| `var x: Int = 5` | `let mut x: i64 = 5;` | `x: int = 5` | `int x = 5;` | `let x: number = 5;` | 显式类型标注覆盖类型推断 |
| `var name = "Alice"` | `let mut name = String::from("Alice");` | `name = "Alice"` | `char name[] = "Alice";` | `let name = "Alice";` | 字符串在 Auto 中是一等公民；无需手动分配内存 |
| `var pi = 3.14` | `let mut pi: f64 = 3.14;` | `pi = 3.14` | `double pi = 3.14;` | `let pi = 3.14;` | Auto 的 `Float` 映射为 64 位浮点数 |
| `let (a, b) = (1, 2)` | `let (a, b) = (1, 2);` | `a, b = 1, 2` | -- | `const [a, b] = [1, 2];` | 元组解构；C 没有内置等价写法 |

---

## C.2 函数

函数使用 `fn` 关键字定义。参数类型写在参数名之后（不带冒号）。返回类型默认推断，除非显式标注。

*另见：[第 3 章 —— 函数与控制流][ch03]、[第 6 章 —— 类型与 `let`][ch06]*

| Auto | Rust | Python | C | TypeScript | 说明 |
|------|------|--------|---|------------|------|
| `fn add(a Int, b Int) Int { return a + b }` | `fn add(a: i64, b: i64) -> i64 { a + b }` | `def add(a: int, b: int) -> int: return a + b` | `int add(int a, int b) { return a + b; }` | `function add(a: number, b: number): number { return a + b; }` | 显式返回类型标注 |
| `fn greet(name String) { print("Hi " + name) }` | `fn greet(name: String) { println!("Hi {}", name); }` | `def greet(name: str): print(f"Hi {name}")` | `void greet(const char* name) { printf("Hi %s", name); }` | `function greet(name: string): void { ... }` | 返回类型推断为 `Unit` |
| `fn abs(x Int) Int { if x < 0 { -x } else { x } }` | `fn abs(x: i64) -> i64 { if x < 0 { -x } else { x } }` | `def abs(x: int) -> int: return -x if x < 0 else x` | `int abs(int x) { return x < 0 ? -x : x; }` | `function abs(x: number): number { return x < 0 ? -x : x; }` | 隐式返回（最后一个表达式） |
| `fn main() { ... }` | `fn main() { ... }` | `def main(): ...` | `int main(void) { ... }` | （无标准入口点） | 程序入口 |
| `return expr` | `return expr;` / `expr`（尾部） | `return expr` | `return expr;` | `return expr;` | Auto 同时支持显式 `return` 和隐式尾部表达式返回 |

---

## C.3 控制流

Auto 使用 `if/else if/else`、`for`（条件式和范围式）以及 `on` 进行模式匹配。没有 `switch` 关键字。

*另见：[第 3 章 —— 函数与控制流][ch03]、[第 7 章 —— 枚举与模式匹配][ch07]*

| Auto | Rust | Python | C | TypeScript | 说明 |
|------|------|--------|---|------------|------|
| `if x > 0 { ... } else if x == 0 { ... } else { ... }` | `if x > 0 { ... } else if x == 0 { ... } else { ... }` | `if x > 0: ... elif x == 0: ... else: ...` | `if (x > 0) { ... } else if (x == 0) { ... } else { ... }` | `if (x > 0) { ... } else if (x === 0) { ... } else { ... }` | Auto `if` 是表达式；可以返回值 |
| `var y = if x > 0 { x } else { -x }` | `let y = if x > 0 { x } else { -x };` | `y = x if x > 0 else -x` | `int y = x > 0 ? x : -x;` | `const y = x > 0 ? x : -x;` | 条件表达式 |
| `for true { ... }` | `loop { ... }` | `while True: ...` | `for (;;) { ... }` | `while (true) { ... }` | 无限循环 |
| `for i in 0..10 { ... }` | `for i in 0..10 { ... }` | `for i in range(10): ...` | `for (int i = 0; i < 10; i++) { ... }` | `for (let i = 0; i < 10; i++) { ... }` | 范围循环；Auto 使用 `0..n` 不含上界 |
| `for item in list { ... }` | `for item in &list { ... }` | `for item in list: ...` | （需要迭代器宏） | `for (const item of list) { ... }` | 基于迭代器的循环 |
| `on Some(v) { print(v) } on None { print("none") }` | `match opt { Some(v) => ..., None => ... }` | `match opt: case Some(v): ... case None: ...` | （无直接等价写法） | （无直接等价写法） | `on` 是 Auto 的模式匹配构造 |

---

## C.4 类型与结构体

自定义数据类型使用 `type` 关键字。方法通过 `ext` 附加到类型上。

*另见：[第 6 章 —— 类型与 `let`][ch06]、[第 8 章 —— 面向对象重塑][ch08]*

| Auto | Rust | Python | C | TypeScript | 说明 |
|------|------|--------|---|------------|------|
| `type Point { x Float, y Float }` | `struct Point { x: f64, y: f64 }` | `@dataclass\nclass Point:\n  x: float\n  y: float` | `typedef struct { double x; double y; } Point;` | `interface Point { x: number; y: number; }` | Auto `type` 是乘积类型（结构体） |
| `Point { x: 1.0, y: 2.0 }` | `Point { x: 1.0, y: 2.0 }` | `Point(x=1.0, y=2.0)` | `(Point){ .x = 1.0, .y = 2.0 }` | `{ x: 1.0, y: 2.0 } as Point` | 构造器使用命名字段 |
| `p.x` | `p.x` | `p.x` | `p.x` | `p.x` | 字段访问在各语言中写法一致 |
| `ext fn area(self Point) Float { self.x * self.y }` | `impl Point { fn area(&self) -> f64 { self.x * self.y } }` | `def area(self) -> float: return self.x * self.y` | `double point_area(Point* p) { return p->x * p->y; }` | `function area(this: Point): number { ... }` | `ext` 将方法附加到类型上 |
| `type Pair<T> { first T, second T }` | `struct Pair<T> { first: T, second: T }` | `from typing import Generic, TypeVar`（类） | （无泛型；使用 `void*` 或宏） | `interface Pair<T> { first: T; second: T; }` | 泛型类型 |

---

## C.5 枚举

Auto 枚举可以在每个变体中携带数据，类似于 Rust 的 `enum`。使用 `on` 进行模式匹配来处理每个变体。

*另见：[第 7 章 —— 枚举与模式匹配][ch07]*

| Auto | Rust | Python | C | TypeScript | 说明 |
|------|------|--------|---|------------|------|
| `enum Direction { North, South, East, West }` | `enum Direction { North, South, East, West }` | `class Direction(Enum): NORTH = 0; ...` | `enum { NORTH, SOUTH, EAST, WEST };` | `enum Direction { North, South, East, West }` | 简单的 C 风格枚举 |
| `enum Option<T> { Some(T), None }` | `enum Option<T> { Some(T), None }` | `from typing import Optional`（内置） | （无直接等价写法） | `type Option<T> = T \| null;` | 携带数据的枚举（代数数据类型） |
| `enum Result<T> { Ok(T), Err(String) }` | `enum Result<T, E> { Ok(T), Err(E) }` | （使用异常或自定义联合类型） | （无直接等价写法） | `type Result<T> = { ok: true, value: T } \| { ok: false, error: string };` | 携带错误的枚举 |
| `var d = Direction.North` | `let d = Direction::North;` | `d = Direction.NORTH` | `enum Direction d = NORTH;` | `const d = Direction.North;` | Auto 中用 `.` 访问变体，Rust 中用 `::` |
| `on d { is North { ... } is South { ... } }` | `match d { Direction::North => { ... }, Direction::South => { ... } }` | `match d: case Direction.NORTH: ...` | `switch (d) { case NORTH: ... }` | `switch (d) { case Direction.North: ... }` | 使用 `on` 和 `is` 进行模式匹配 |

---

## C.6 错误处理

Auto 使用 `?T` 表示可选值，使用 `!T` 表示可能失败的操作，灵感来自 Rust 但语法更加精简。

*另见：[第 9 章 —— 错误处理][ch09]*

| Auto | Rust | Python | C | TypeScript | 说明 |
|------|------|--------|---|------------|------|
| `?Int`（可选值） | `Option<i32>` | `Optional[int]` | （无等价写法；使用哨兵值） | `number \| null` | `?T` 是 `Some(T) \| None` 的语法糖 |
| `!Int`（可失败结果） | `Result<i32, String>` | （使用异常） | 返回 `int` 搭配错误码 | `Result<number, string>`（自定义） | `!T` 是 `Ok(T) \| Err(String)` 的语法糖 |
| `!x`（解包） | `x.unwrap()` | `x`（为 None 时抛出异常） | （调用者必须检查） | `x!`（非空断言） | 如果为 `None`/`Err` 则 panic；用于测试或不变量已保证的场景 |
| `var v = !result` | `let v = result.unwrap();` | `v = result` | `v = result; // 但愿没问题` | `const v = result!;` | 解包断言成功；失败时崩溃 |
| `fn read() !String { ... }` | `fn read() -> Result<String, io::Error> { ... }` | `def read() -> str: ...`（抛出异常） | `int read(char* buf, int len);`（错误码） | `function read(): Result<string, Error> { ... }` | 返回位置使用 `!T` 表示可失败 |
| `try { expr } catch e { ... }` | （无 try/catch；对 `Result` 使用 `match`） | `try: ... except Exception as e: ...` | （无 try/catch） | `try { ... } catch (e) { ... }` | Auto 提供 `try/catch` 用于与基于异常的系统互操作 |

---

## C.7 集合

Auto 内置 `List`、`Map` 和 `Set` 类型，支持字面量语法。

*另见：[第 4 章 —— 集合与节点][ch04]、[第 21 章 —— 标准库导览][ch21]*

| Auto | Rust | Python | C | TypeScript | 说明 |
|------|------|--------|---|------------|------|
| `[1, 2, 3]` | `vec![1, 2, 3]` | `[1, 2, 3]` | `int arr[] = {1, 2, 3};` | `[1, 2, 3]` | 列表字面量 |
| `var list: List<Int> = []` | `let list: Vec<i32> = vec![];` | `list: list[int] = []` | `int* list = malloc(0);` | `const list: number[] = [];` | 空的带类型列表 |
| `list.push(4)` | `list.push(4);` | `list.append(4)` | （手动重新分配） | `list.push(4);` | 向列表末尾追加元素 |
| `list.len()` | `list.len()` | `len(list)` | （手动跟踪大小） | `list.length` | 列表长度 |
| `{"name": "Alice", "age": 30}` | `HashMap::from([("name", "Alice"), ("age", 30)])` | `{"name": "Alice", "age": 30}` | （无内置映射） | `const m = new Map([["name", "Alice"], ["age", 30]]);` | 映射字面量 |
| `map["name"]` | `map.get("name")` | `map["name"]` | （无内置映射） | `m.get("name")` | 映射访问 |
| `{"a", "b", "c"}` | `HashSet::from(["a", "b", "c"])` | `{"a", "b", "c"}` | （无内置集合） | `new Set(["a", "b", "c"])` | 集合字面量 |

---

## C.8 字符串操作

Auto 字符串支持使用 `{}` 在字符串字面量中进行插值。

*另见：[第 2 章 —— 变量与运算符][ch02]、[第 21 章 —— 标准库导览][ch21]*

| Auto | Rust | Python | C | TypeScript | 说明 |
|------|------|--------|---|------------|------|
| `format!("Hello, {name}!")` | `format!("Hello, {}!", name)` | `f"Hello, {name}!"` | `sprintf(buf, "Hello, %s!", name);` | `` `Hello, ${name}!` `` | 字符串插值 |
| `"Hello, " + name` | `format!("Hello, {}", name)` / `"Hello, ".to_string() + &name` | `"Hello, " + name` | `strcat(buf, name)` | `` `Hello, ${name}` `` | 字符串拼接 |
| `name.len()` | `name.len()` | `len(name)` | `strlen(name)` | `name.length` | 字符串长度 |
| `name.upper()` | `name.to_uppercase()` | `name.upper()` | （无内置方法） | `name.toUpperCase()` | 转换为大写 |
| `name.contains("li")` | `name.contains("li")` | `"li" in name` | `strstr(name, "li") != NULL` | `name.includes("li")` | 子串搜索 |
| `name.split(",")` | `name.split(",")` | `name.split(",")` | `strtok(name, ",")` | `name.split(",")` | 分割为列表 |

---

## C.9 并发

Auto 的并发模型基于 Actor 和消息传递构建，而非共享内存线程。这是 AIOS 层。

*另见：[第 15 章 —— Actor 并发][ch15]、[第 16 章 —— 异步与 `~T`][ch16]*

| Auto | Rust | Python | C | TypeScript | 说明 |
|------|------|--------|---|------------|------|
| `spawn greeter` | `std::thread::spawn(\|\| greeter())` | `threading.Thread(target=greeter).start()` | `pthread_create(&t, NULL, greeter, NULL);` | `new Worker(greeter);` | 生成并发任务 |
| `send greeter "Hello"` | `tx.send("Hello".to_string())` | `queue.put("Hello")` | `write(pipe_fd, "Hello", 5);` | `worker.postMessage("Hello");` | 向任务发送消息 |
| `on msg String { print(msg) }` | `for msg in rx { println!("{}", msg); }` | `msg = queue.get()` | `read(pipe_fd, buf, sizeof(buf));` | `self.onmessage = (e) => { ... }` | 接收并模式匹配消息 |
| `~T`（异步类型） | `impl Future<Output = T>` | `Awaitable[T]`（通过 `asyncio`） | （无内置异步） | `Promise<T>` | Auto 的异步标记类型 |
| `await expr` | `expr.await` | `await expr` | （无内置异步） | `await expr` | 挂起直到异步结果就绪 |
| `var handle = spawn worker` | `let handle = JoinHandle::from(...)` | `t = Thread(target=worker)` | `pthread_t t;` | `const w = new Worker(worker);` | 捕获已生成任务的句柄 |

---

## C.10 属性与元数据

属性用于修改函数和类型的编译或处理方式。使用 `#[...]` 语法，借鉴自 Rust。

*另见：[第 18 章 —— 测试][ch18]、[第 20 章 —— 编译期与元编程][ch20]*

| Auto | Rust | Python | C | TypeScript | 说明 |
|------|------|--------|---|------------|------|
| `#[test]` | `#[test]` | `@pytest` / `@unittest` | （无内置；使用框架宏） | `@test`（Jest） | 将函数标记为测试 |
| `#[comptime]` | `const fn` | （无等价写法） | （无等价写法） | （无等价写法） | 在编译期求值函数 |
| `#[inline]` | `#[inline]` | （无等价写法） | `inline` | （无等价写法） | 提示编译器内联函数 |
| `#[deprecated]` | `#[deprecated]` | `@deprecated` | `__attribute__((deprecated))` | `@deprecated`（TSDoc） | 使用该项时发出警告 |
| `#[derive(Debug)]` | `#[derive(Debug)]` | `@dataclass` 搭配 `__repr__` | （无等价写法） | （无等价写法） | 自动生成常见 trait 实现 |
| `#[target(os = "linux")]` | `#[cfg(target_os = "linux")]` | `sys.platform == "linux"`（运行时） | `#ifdef __linux__` | （无等价写法） | 条件编译 |
