# Auto 相关书籍

本仓库包含《Auto 编程语言》一书的源码，
以及五本双语（英/中）参考书，展示 Auto 如何映射到其他编程语言。

主要内容采用 AutoDown 格式编写，
同时我们也提供了从 AutoDown 生成的 Markdown 格式版本。

## 书籍集合

本仓库包含原创的**《Auto 编程语言》**主书，以及**七本**配套参考书，
展示 Auto 如何映射到其他编程语言。每本书都提供配对的**英文**（`.md`）和**中文**（`.cn.md`）章节，并附带可运行的代码示例。

| # | 书籍 | 目录 | 原著 | 章节数 | 转译器 | 重点 |
|---|------|------|------|--------|--------|------|
| 1 | [《Auto 编程语言》](#auto-编程语言) | [`tapl/`](tapl/) | 原创 | 22（ch00-21）+ 4 个附录 | 全部 5 种语言 | Auto 权威指南：脚本 → 系统 → AIOS |
| 2 | [Auto版《Rust程序设计语言》](#auto版rust程序设计语言) | [`rust/`](rust/) | [*Rust 程序设计语言*](https://doc.rust-lang.org/book/) | 22（ch00-21 + 附录）| `a2r` → Rust | 系统编程、所有权、Actor、异步 |
| 3 | [Auto版《TypeScript Handbook》](#auto版typescript-handbook) | [`typescript/`](typescript/) | [*TypeScript Handbook*](https://www.typescriptlang.org/docs/handbook/) · [GitHub](https://github.com/microsoft/TypeScript-New-Handbook) | 10（ch00-09）| `a2ts` → TypeScript | Web 开发、类型、类、模块 |
| 4 | [Auto版《TypeScript DeepDive》](#auto版typescript-deepdive) | [`typescript-deepdive/`](typescript-deepdive/) | [*TypeScript Deep Dive*](https://basarat.gitbook.io/typescript/) · [GitHub](https://github.com/basarat/typescript-book) | 16（ch00-15）| `a2ts` → TypeScript | 高级类型系统、泛型、模式匹配 |
| 5 | [Auto版《Little Book of C》](#auto版little-book-of-c) | [`little-c/`](little-c/) | [*C 语言小书*](https://little-book-of-c.github.io/) · [GitHub](https://github.com/little-book-of/c) | 10（ch00-09）| `a2c` → C | C 入门：内存、指针、结构体、I/O |
| 6 | [Auto版《Modern C》](#auto版modern-c) | [`modern-c/`](modern-c/) | [*Modern C*（Jens Gustedt）](https://gustedt.gitlabpages.inria.fr/modern-c/) | 22（ch00-21）| `a2c` → C | 严谨 C：内存模型、线程、原子操作 |
| 7 | [Auto版《A Byte of Python》](#auto版a-byte-of-python) | [`byte-of-python/`](byte-of-python/) | [*A Byte of Python*](https://python.swaroopch.com/) · [GitHub](https://github.com/swaroopch/byte-of-python) | 17（ch00-16）| `a2p` → Python | Python 入门：函数、面向对象、异常、标准库 |
| 8 | [Auto版《Think Python》](#auto版think-python) | [`think-python/`](think-python/) | [*Think Python, 3rd Edition*](https://greenteapress.com/wp/think-python-3rd-edition/)（Allen B. Downey） | 20（ch00-19）| `a2p` → Python | 编程思维：递归、面向对象、数据结构、文本分析 |

**共计：143 个章节、约 148 个代码示例（含转译器输出），全部提供英中双语版本。**

## Auto 编程语言

[`tapl/`](tapl/) 目录包含原创的《Auto 编程语言》一书——Auto 语言的权威指南。
每个代码示例均展示**五种语言**（Auto、Rust、Python、C、TypeScript），
让来自不同语言背景的开发者都能通过对比学习。

全书分为三个渐进式阶段：

- **第一阶段——Auto 作为脚本**（第 1–5 章）：变量、函数、控制流、集合、猜数游戏项目
- **第二阶段——Auto 作为系统**（第 6–14 章）：类型、枚举、面向对象、错误处理、模块、引用、内存、泛型、文件处理器项目
- **第三阶段——Auto 作为 AIOS**（第 15–22 章）：Actor 并发、异步、智能转型、测试、闭包、编译期计算、标准库、聊天服务器项目

每个章节提供**英文**（`.md`）和**中文**（`.cn.md`）两个版本：

| 章 | 阶段 | 英文版 | 中文版 |
|----|------|-------|--------|
| 00 | — | [Introduction](tapl/ch00-introduction.md) | [简介](tapl/ch00-introduction.cn.md) |
| 01 | 脚本 | [Getting Started](tapl/ch01-getting-started.md) | [入门](tapl/ch01-getting-started.cn.md) |
| 02 | 脚本 | [Variables & Operators](tapl/ch02-variables-operators.md) | [变量与运算符](tapl/ch02-variables-operators.cn.md) |
| 03 | 脚本 | [Functions & Control Flow](tapl/ch03-functions.md) | [函数与控制流](tapl/ch03-functions.cn.md) |
| 04 | 脚本 | [Collections & Nodes](tapl/ch04-collections.md) | [集合与节点](tapl/ch04-collections.cn.md) |
| 05 | 脚本 | [Project: Guessing Game](tapl/ch05-guessing-game.md) | [项目：猜数游戏](tapl/ch05-guessing-game.cn.md) |
| 06 | 系统 | [Types & `let`](tapl/ch06-types.md) | [类型与 `let`](tapl/ch06-types.cn.md) |
| 07 | 系统 | [Enums & Pattern Matching](tapl/ch07-enums.md) | [枚举与模式匹配](tapl/ch07-enums.cn.md) |
| 08 | 系统 | [OOP Reshaped](tapl/ch08-oop.md) | [重塑面向对象](tapl/ch08-oop.cn.md) |
| 09 | 系统 | [Error Handling](tapl/ch09-error-handling.md) | [错误处理](tapl/ch09-error-handling.cn.md) |
| 10 | 系统 | [Packages & Modules](tapl/ch10-modules.md) | [包与模块](tapl/ch10-modules.cn.md) |
| 11 | 系统 | [References & Pointers](tapl/ch11-references.md) | [引用与指针](tapl/ch11-references.cn.md) |
| 12 | 系统 | [Memory & Ownership](tapl/ch12-memory.md) | [内存与所有权](tapl/ch12-memory.cn.md) |
| 13 | 系统 | [Generics](tapl/ch13-generics.md) | [泛型](tapl/ch13-generics.cn.md) |
| 14 | 系统 | [Project: File Processor](tapl/ch14-file-processor.md) | [项目：文件处理器](tapl/ch14-file-processor.cn.md) |
| 15 | AIOS | [Actor Concurrency](tapl/ch15-actors.md) | [Actor 并发](tapl/ch15-actors.cn.md) |
| 16 | AIOS | [Async with `~T`](tapl/ch16-async.md) | [异步编程 `~T`](tapl/ch16-async.cn.md) |
| 17 | AIOS | [Smart Casts & Flow Typing](tapl/ch17-smart-casts.md) | [智能转型与流式类型](tapl/ch17-smart-casts.cn.md) |
| 18 | AIOS | [Testing](tapl/ch18-testing.md) | [测试](tapl/ch18-testing.cn.md) |
| 19 | AIOS | [Closures & Iterators](tapl/ch19-closures.md) | [闭包与迭代器](tapl/ch19-closures.cn.md) |
| 20 | AIOS | [Comptime & Metaprogramming](tapl/ch20-comptime.md) | [编译期计算与元编程](tapl/ch20-comptime.cn.md) |
| 21 | AIOS | [Standard Library Tour](tapl/ch21-stdlib.md) | [标准库概览](tapl/ch21-stdlib.cn.md) |
| 22 | AIOS | [Project: Multi-user Chat Server](tapl/ch22-chat-server.md) | [项目：多人聊天服务器](tapl/ch22-chat-server.cn.md) |

### 附录

| 附录 | 英文版 | 中文版 |
|------|-------|--------|
| A | [Keyword Reference](tapl/appendix-a-keywords.md) | [关键字参考](tapl/appendix-a-keywords.cn.md) |
| B | [Operator Table](tapl/appendix-b-operators.md) | [运算符表](tapl/appendix-b-operators.cn.md) |
| C | [Transpiler Quick-Ref](tapl/appendix-c-transpiler-quick-ref.md) | [转译器速查](tapl/appendix-c-transpiler-quick-ref.cn.md) |
| D | [Standard Library Index](tapl/appendix-d-stdlib-index.md) | [标准库索引](tapl/appendix-d-stdlib-index.cn.md) |

### 核心概念映射（Auto vs 五种语言）

| Auto | Rust | Python | C | TypeScript | 说明 |
|------|------|--------|---|-----------|------|
| `type` | `struct` | `@dataclass` | `struct` | `interface`/`class` | 数据类型定义 |
| `enum` | `enum` | `Union` | `enum` + tag | `type` union | 和类型 |
| `spec` | `trait` | `Protocol`/`ABC` | vtable | `interface` | 行为契约 |
| `is` | `match` | `match`/`isinstance` | `switch` | `switch` | 模式匹配 |
| `ext` | `impl` | 类方法 | 函数 | 方法 | 扩展方法 |
| `has` | 组合 | 组合 | 嵌套结构体 | 组合 | 自动委托 |
| `?T` | `Option<T>` | `T \| None` | 标记指针 | `T \| null` | 可选值 |
| `!T` | `Result<T,E>` | `raise`/`try` | 错误码 | `try`/`catch` | 错误结果 |
| `spawn`/`send` | `thread::spawn`/`mpsc` | `Thread`/`Queue` | `pthread`/pipe | `Worker`/`postMessage` | Actor 并发 |
| `~T` | `async fn` | `async def` | 回调 | `Promise<T>` | 异步蓝图 |
| `#[comptime]` | `const fn`/宏 | 装饰器 | 预处理器 | 装饰器 | 编译期计算 |
| `automan` | `cargo` | `pip`/`poetry` | `make`/`cmake` | `npm`/`pnpm` | 包管理器 |

## Auto版《Rust程序设计语言》

[`rust/`](rust/) 目录包含了对《Rust 程序设计语言》一书的完整改编，
为 Auto 编程语言量身定制，每章都包含配对的 Auto/Rust 代码示例。

每个章节提供**英文**（`.md`）和**中文**（`.cn.md`）两个版本：

| 章 | 英文版 | 中文版 |
|----|-------|--------|
| 00 | [Introduction](rust/ch00-introduction.md) | [简介](rust/ch00-introduction.cn.md) |
| 01 | [Getting Started](rust/ch01-getting-started.md) | [入门指南](rust/ch01-getting-started.cn.md) |
| 02 | [Guessing Game](rust/ch02-guessing-game.md) | [猜数游戏](rust/ch02-guessing-game.cn.md) |
| 03 | [Common Concepts](rust/ch03-common-concepts.md) | [通用概念](rust/ch03-common-concepts.cn.md) |
| 04 | [Memory Model](rust/ch04-ownership.md) | [内存模型](rust/ch04-ownership.cn.md) |
| 05 | [Types](rust/ch05-structs.md) | [类型](rust/ch05-structs.cn.md) |
| 06 | [Enums & Matching](rust/ch06-enums.md) | [枚举与匹配](rust/ch06-enums.cn.md) |
| 07 | [Packages & Modules](rust/ch07-packages.md) | [包与模块](rust/ch07-packages.cn.md) |
| 08 | [Collections](rust/ch08-collections.md) | [集合](rust/ch08-collections.cn.md) |
| 09 | [Error Handling](rust/ch09-error-handling.md) | [错误处理](rust/ch09-error-handling.cn.md) |
| 10 | [Generics, Specs, AutoFree](rust/ch10-generics.md) | [泛型、规范与 AutoFree](rust/ch10-generics.cn.md) |
| 11 | [Testing](rust/ch11-testing.md) | [测试](rust/ch11-testing.cn.md) |
| 12 | [I/O Project](rust/ch12-io-project.md) | [I/O 项目](rust/ch12-io-project.cn.md) |
| 13 | [Closures & Iterators](rust/ch13-functional-features.md) | [闭包与迭代器](rust/ch13-functional-features.cn.md) |
| 14 | [More About automan](rust/ch14-automan.md) | [automan 进阶](rust/ch14-automan.cn.md) |
| 15 | [References & Pointers](rust/ch15-references.md) | [引用与指针](rust/ch15-references.cn.md) |
| 16 | [Actor Concurrency](rust/ch16-concurrency.md) | [Actor 并发](rust/ch16-concurrency.cn.md) |
| 17 | [Async with ~T](rust/ch17-async.md) | [异步编程 ~T](rust/ch17-async.cn.md) |
| 18 | [OOP Patterns](rust/ch18-oop.md) | [面向对象模式](rust/ch18-oop.cn.md) |
| 19 | [Patterns & Matching](rust/ch19-patterns.md) | [模式与匹配](rust/ch19-patterns.cn.md) |
| 20 | [Advanced Features](rust/ch20-advanced.md) | [高级特性](rust/ch20-advanced.cn.md) |
| 21 | [Web Server Project](rust/ch21-web-server.md) | [Web 服务器项目](rust/ch21-web-server.cn.md) |
| 附录 | [Appendix](rust/appendix-reference.md) | [附录](rust/appendix-reference.cn.md) |

### 核心概念映射

| Rust | Auto | 说明 |
|------|------|------|
| `struct` | `type` | 数据类型定义 |
| `impl` | `ext` | 方法挂载 |
| `trait` | `spec` | 共享行为接口 |
| `match` | `is` | 模式匹配 |
| `Option<T>` | `?T` | 可选值 |
| `Result<T,E>` | `!T` | 错误传播 |
| `async`/`await` | `~T`/`on` | 异步蓝图 |
| `unsafe` | `sys` | 系统级代码 |
| `macro_rules!` | `#[]` comptime | 编译期元编程 |
| 线程 | Actor | 并发模型 |
| `Cargo` | `automan` | 包管理器 |

## Auto版《TypeScript Handbook》

[`typescript/`](typescript/) 目录包含了对《TypeScript Handbook v2》一书的完整改编，
为 Auto 编程语言量身定制，每章都包含配对的 Auto/TypeScript 代码示例。

每个章节提供**英文**（`.md`）和**中文**（`.cn.md`）两个版本：

| 章 | 英文版 | 中文版 |
|----|-------|--------|
| 00 | [Introduction](typescript/ch00-introduction.md) | [简介](typescript/ch00-introduction.cn.md) |
| 01 | [Basics](typescript/ch01-basics.md) | [基础](typescript/ch01-basics.cn.md) |
| 02 | [Everyday Types](typescript/ch02-everyday-types.md) | [常用类型](typescript/ch02-everyday-types.cn.md) |
| 03 | [Narrowing](typescript/ch03-narrowing.md) | [类型收窄](typescript/ch03-narrowing.cn.md) |
| 04 | [More on Functions](typescript/ch04-functions.md) | [函数进阶](typescript/ch04-functions.cn.md) |
| 05 | [Object Types](typescript/ch05-object-types.md) | [对象类型](typescript/ch05-object-types.cn.md) |
| 06 | [Creating Types from Types](typescript/ch06-creating-types.md) | [从类型创建类型](typescript/ch06-creating-types.cn.md) |
| 07 | [Type Operators](typescript/ch07-type-operators.md) | [类型运算符](typescript/ch07-type-operators.cn.md) |
| 08 | [Classes](typescript/ch08-classes.md) | [类](typescript/ch08-classes.cn.md) |
| 09 | [Modules](typescript/ch09-modules.md) | [模块](typescript/ch09-modules.cn.md) |

### 核心概念映射

| TypeScript | Auto | 说明 |
|-----------|------|------|
| `class` | `type` | 数据结构定义 |
| `interface` | `spec` | 行为契约 |
| `implements` | `as` | 接口实现 |
| `extends` | `is` | 继承 |
| `class X extends Y` | — | 使用 `is` 或 `has` 组合 |
| `(x: number) => number` | `fn(int)int` | 函数类型（注解） |
| `(x, y) => x + y` | `(x, y) => x + y` | 闭包（值） |
| `readonly` | — | 使用 `let` 声明不可变变量 |
| `keyof` / `typeof` / 映射类型 | — | TypeScript 独有高级类型 |
| `import` / `export` | `use` / `mod` | 模块系统 |

## Auto版《TypeScript DeepDive》

[`typescript-deepdive/`](typescript-deepdive/) 目录包含了对 TypeScript 类型系统的深入探索，
适配为 Auto 版本，涵盖高级模式如可辨识联合、泛型和映射类型。

每个章节提供**英文**（`.md`）和**中文**（`.cn.md`）两个版本：

| 章 | 英文版 | 中文版 |
|----|-------|--------|
| 00 | [Introduction](typescript-deepdive/ch00-introduction.md) | [简介](typescript-deepdive/ch00-introduction.cn.md) |
| 01 | [Type Basics](typescript-deepdive/ch01-type-basics.md) | [类型基础](typescript-deepdive/ch01-type-basics.cn.md) |
| 02 | [Functions](typescript-deepdive/ch02-functions.md) | [函数](typescript-deepdive/ch02-functions.cn.md) |
| 03 | [Literal Types](typescript-deepdive/ch03-literal-types.md) | [字面量类型](typescript-deepdive/ch03-literal-types.cn.md) |
| 04 | [Primitives](typescript-deepdive/ch04-primitives.md) | [原始类型](typescript-deepdive/ch04-primitives.cn.md) |
| 05 | [Spec Implementation](typescript-deepdive/ch05-spec-implementation.md) | [规范实现](typescript-deepdive/ch05-spec-implementation.cn.md) |
| 06 | [Enums & Unions](typescript-deepdive/ch06-enums-unions.md) | [枚举与联合](typescript-deepdive/ch06-enums-unions.cn.md) |
| 07 | [Generics](typescript-deepdive/ch07-generics.md) | [泛型](typescript-deepdive/ch07-generics.cn.md) |
| 08 | [Advanced Types](typescript-deepdive/ch08-advanced-types.md) | [高级类型](typescript-deepdive/ch08-advanced-types.cn.md) |
| 09 | [Pattern Matching](typescript-deepdive/ch09-pattern-matching.md) | [模式匹配](typescript-deepdive/ch09-pattern-matching.cn.md) |
| 10 | [Error Handling](typescript-deepdive/ch10-error-handling.md) | [错误处理](typescript-deepdive/ch10-error-handling.cn.md) |
| 11 | [Composition](typescript-deepdive/ch11-composition.md) | [组合](typescript-deepdive/ch11-composition.cn.md) |
| 12 | [Collections](typescript-deepdive/ch12-collections.md) | [集合](typescript-deepdive/ch12-collections.cn.md) |
| 13 | [Common Errors](typescript-deepdive/ch13-common-errors.md) | [常见错误](typescript-deepdive/ch13-common-errors.cn.md) |
| 14 | [Async Patterns](typescript-deepdive/ch14-async-patterns.md) | [异步模式](typescript-deepdive/ch14-async-patterns.cn.md) |
| 15 | [Compiler API](typescript-deepdive/ch15-compiler.md) | [编译器 API](typescript-deepdive/ch15-compiler.cn.md) |

## Auto版《Little Book of C》

[`little-c/`](little-c/) 目录包含了对《C 语言小书》的 Auto 适配版本，
面向通过 a2c 转译器以 C 为目标的 Auto 程序员。涵盖内存、指针、结构体、I/O、
系统编程、调试以及真实项目构建。

每个章节提供**英文**（`.md`）和**中文**（`.cn.md`）两个版本：

| 章 | 英文版 | 中文版 |
|----|-------|--------|
| 00 | [Getting Started](little-c/ch00-getting-started.md) | [入门指南](little-c/ch00-getting-started.cn.md) |
| 01 | [Language Basics](little-c/ch01-language-basics.md) | [语言基础](little-c/ch01-language-basics.cn.md) |
| 02 | [Working with Memory](little-c/ch02-memory.md) | [内存管理](little-c/ch02-memory.cn.md) |
| 03 | [Structuring Data](little-c/ch03-structuring-data.md) | [数据结构](little-c/ch03-structuring-data.cn.md) |
| 04 | [I/O and Files](little-c/ch04-io-files.md) | [输入输出与文件](little-c/ch04-io-files.cn.md) |
| 05 | [Compilation & Build](little-c/ch05-compilation.md) | [编译与构建](little-c/ch05-compilation.cn.md) |
| 06 | [System Programming](little-c/ch06-system-programming.md) | [系统编程](little-c/ch06-system-programming.cn.md) |
| 07 | [Debugging & Testing](little-c/ch07-debugging.md) | [调试与测试](little-c/ch07-debugging.cn.md) |
| 08 | [Portable & Modern C](little-c/ch08-portable-modern.md) | [可移植与现代 C](little-c/ch08-portable-modern.cn.md) |
| 09 | [Building Real Projects](little-c/ch09-real-projects.md) | [构建真实项目](little-c/ch09-real-projects.cn.md) |

### 核心概念映射（Auto → C）

| Auto | C | 说明 |
|------|---|------|
| `fn main()` | `int main(void)` | 入口函数 |
| `print("text")` | `printf("%s\n", "text")` | 输出打印 |
| `type Point { x int, y int }` | `struct Point { int x; int y; };` | 结构体定义 |
| `enum Color { RED, GREEN, BLUE }` | `enum Color { COLOR_RED, ... };` | 枚举定义 |
| `is x { ... }` | `switch (x) { ... }` | 模式匹配 / switch |
| `spec Drawable { fn draw() }` | vtable 结构体 | 接口 / 虚表 |
| `let x int = 5` | `const int x = 5;` | 不可变绑定 |
| `var x int = 5` | `int x = 5;` | 可变变量 |
| `for i in 0..10 { }` | `for (int i=0; i<10; i++) { }` | 计数循环 |
| `auto a2c` / `auto b` | `gcc` / `make` | 构建命令 |

## Auto版《Modern C》

[`modern-c/`](modern-c/) 目录包含了对《Modern C》（Jens Gustedt 著）的严谨 Auto 适配版本。
覆盖完整 C 语言的四个层次：Encounter、Acquaintance、Cognition、Experience — 包括抽象状态机、
内存模型、类型泛型编程、线程和原子操作。

每个章节提供**英文**（`.md`）和**中文**（`.cn.md`）两个版本：

| 章 | 层级 | 英文版 | 中文版 |
|----|------|-------|--------|
| 00 | — | [Introduction](modern-c/ch00-introduction.md) | [简介](modern-c/ch00-introduction.cn.md) |
| 01 | Encounter | [Getting Started](modern-c/ch01-getting-started.md) | [入门](modern-c/ch01-getting-started.cn.md) |
| 02 | Encounter | [Program Structure](modern-c/ch02-program-structure.md) | [程序结构](modern-c/ch02-program-structure.cn.md) |
| 03 | Acquaintance | [Control Flow](modern-c/ch03-control-flow.md) | [控制流](modern-c/ch03-control-flow.cn.md) |
| 04 | Acquaintance | [Expressions](modern-c/ch04-expressions.md) | [表达式](modern-c/ch04-expressions.cn.md) |
| 05 | Acquaintance | [Basic Values & Data](modern-c/ch05-basic-values.md) | [基本值与数据](modern-c/ch05-basic-values.cn.md) |
| 06 | Acquaintance | [Derived Data Types](modern-c/ch06-derived-types.md) | [派生数据类型](modern-c/ch06-derived-types.cn.md) |
| 07 | Acquaintance | [Functions](modern-c/ch07-functions.md) | [函数](modern-c/ch07-functions.cn.md) |
| 08 | Acquaintance | [C Library Functions](modern-c/ch08-c-library.md) | [C 库函数](modern-c/ch08-c-library.cn.md) |
| 09 | Cognition | [Style](modern-c/ch09-style.md) | [代码风格](modern-c/ch09-style.cn.md) |
| 10 | Cognition | [Organization](modern-c/ch10-organization.md) | [组织与文档](modern-c/ch10-organization.cn.md) |
| 11 | Cognition | [Pointers](modern-c/ch11-pointers.md) | [指针](modern-c/ch11-pointers.cn.md) |
| 12 | Cognition | [Memory Model](modern-c/ch12-memory-model.md) | [内存模型](modern-c/ch12-memory-model.cn.md) |
| 13 | Cognition | [Storage](modern-c/ch13-storage.md) | [存储](modern-c/ch13-storage.cn.md) |
| 14 | Cognition | [I/O Processing](modern-c/ch14-io-processing.md) | [I/O 处理](modern-c/ch14-io-processing.cn.md) |
| 15 | Cognition | [Program Failure](modern-c/ch15-program-failure.md) | [程序故障](modern-c/ch15-program-failure.cn.md) |
| 16 | Experience | [Performance](modern-c/ch16-performance.md) | [性能](modern-c/ch16-performance.cn.md) |
| 17 | Experience | [Function-like Macros](modern-c/ch17-macros.md) | [函数式宏](modern-c/ch17-macros.cn.md) |
| 18 | Experience | [Type-generic Programming](modern-c/ch18-type-generic.md) | [类型泛型编程](modern-c/ch18-type-generic.cn.md) |
| 19 | Experience | [Control Flow Variations](modern-c/ch19-control-flow-variations.md) | [控制流变体](modern-c/ch19-control-flow-variations.cn.md) |
| 20 | Experience | [Threads](modern-c/ch20-threads.md) | [线程](modern-c/ch20-threads.cn.md) |
| 21 | Experience | [Atomics & Memory Consistency](modern-c/ch21-atomics.md) | [原子操作与内存一致性](modern-c/ch21-atomics.cn.md) |

### 核心概念映射（Auto → Modern C）

| Auto | Modern C | 说明 |
|------|----------|------|
| `type` | `struct` + `typedef` | 数据结构定义 |
| `spec` | 函数指针 / vtable | 行为接口 |
| `enum` | 标记联合 | 和类型 / 数据枚举 |
| `is` | `switch` / `_Generic` | 模式匹配 |
| `let`/`var` | `const`/可变 | 不可变/可变绑定 |
| `var x = expr` | `auto x = expr` (C23) | 类型推断 |
| `fn` | 函数定义 | 函数 |
| `mod`/`use` | `#include` / 头文件 | 模块系统 |
| `#[]` comptime | 预处理器宏 | 编译期元编程 |
| Actor | `thrd_*` / `mtx_*` | 并发模型 |
| `!T` 错误类型 | `errno` / `setjmp` | 错误处理 |
| AutoFree | `malloc`/`free` | 内存管理 |

## Auto版《A Byte of Python》

[`byte-of-python/`](byte-of-python/) 目录包含了对《A Byte of Python》（Swaroop C H 著）的完整 Auto 适配版本，
通过 a2p 转译器将 Auto 代码转译为 Python，每章都包含配对的 Auto/Python 代码示例。
这是一本面向初学者的 Auto 编程入门教程。

每个章节提供**英文**（`.md`）和**中文**（`.cn.md`）两个版本：

| 章 | 英文版 | 中文版 |
|----|-------|--------|
| 00 | [Preface](byte-of-python/ch00-preface.md) | [序言](byte-of-python/ch00-preface.cn.md) |
| 01 | [About Auto](byte-of-python/ch01-about-python.md) | [关于 Auto](byte-of-python/ch01-about-python.cn.md) |
| 02 | [Installation](byte-of-python/ch02-installation.md) | [安装](byte-of-python/ch02-installation.cn.md) |
| 03 | [First Steps](byte-of-python/ch03-first-steps.md) | [第一步](byte-of-python/ch03-first-steps.cn.md) |
| 04 | [Basics](byte-of-python/ch04-basics.md) | [基础](byte-of-python/ch04-basics.cn.md) |
| 05 | [Operators and Expressions](byte-of-python/ch05-operators-expressions.md) | [运算符与表达式](byte-of-python/ch05-operators-expressions.cn.md) |
| 06 | [Control Flow](byte-of-python/ch06-control-flow.md) | [控制流](byte-of-python/ch06-control-flow.cn.md) |
| 07 | [Functions](byte-of-python/ch07-functions.md) | [函数](byte-of-python/ch07-functions.cn.md) |
| 08 | [Modules](byte-of-python/ch08-modules.md) | [模块](byte-of-python/ch08-modules.cn.md) |
| 09 | [Data Structures](byte-of-python/ch09-data-structures.md) | [数据结构](byte-of-python/ch09-data-structures.cn.md) |
| 10 | [Problem Solving](byte-of-python/ch10-problem-solving.md) | [问题解决](byte-of-python/ch10-problem-solving.cn.md) |
| 11 | [OOP](byte-of-python/ch11-oop.md) | [面向对象编程](byte-of-python/ch11-oop.cn.md) |
| 12 | [Input and Output](byte-of-python/ch12-input-output.md) | [输入与输出](byte-of-python/ch12-input-output.cn.md) |
| 13 | [Exceptions](byte-of-python/ch13-exceptions.md) | [异常](byte-of-python/ch13-exceptions.cn.md) |
| 14 | [Standard Library](byte-of-python/ch14-stdlib.md) | [标准库](byte-of-python/ch14-stdlib.cn.md) |
| 15 | [More](byte-of-python/ch15-more.md) | [更多](byte-of-python/ch15-more.cn.md) |
| 16 | [What Next](byte-of-python/ch16-what-next.md) | [下一步](byte-of-python/ch16-what-next.cn.md) |

### 核心概念映射（Auto → Python）

| Auto | Python | 说明 |
|------|--------|------|
| `fn main()` | `def main():` + `if __name__` | 入口函数 |
| `let x = 5` | `x = 5` | 变量声明 |
| `let mut x = 5` | `x = 5` | 可变变量 |
| `// 注释` | `# 注释` | 注释 |
| `f"$name"` | `f"{name}"` | f-string 插值 |
| `type Name { ... }` | `class Name:` / `@dataclass` | 类/结构体定义 |
| `fn init(&self, ...)` | `def __init__(self, ...)` | 构造函数 |
| `.field` | `self.field` | 成员访问 |
| `type Sub: Super {}` | `class Sub(Super):` | 继承 |
| `for cond { ... }` | `while cond:` | while 循环 |
| `for i in 0..10 {}` | `for i in range(0, 10):` | for 循环 |
| `true`/`false` | `True`/`False` | 布尔值 |
| `&&`/`||`/`!` | `and`/`or`/`not` | 逻辑运算符 |
| `List` | `list` | 有序可变集合 |
| `HashMap` | `dict` | 键值映射 |
| `HashSet` | `set` | 唯一值集合 |

## Auto版《Think Python》

[`think-python/`](think-python/) 目录包含了对《Think Python, 3rd Edition》（Allen B. Downey 著）的完整 Auto 适配版本，
通过 a2p 转译器将 Auto 代码转译为 Python，每章都包含配对的 Auto/Python 代码示例。
本书以编程思维为核心，涵盖递归、面向对象编程、数据结构和文本分析。

每个章节提供**英文**（`.md`）和**中文**（`.cn.md`）两个版本：

| 章 | 英文版 | 中文版 |
|----|-------|--------|
| 00 | [Preface](think-python/ch00-preface.md) | [序言](think-python/ch00-preface.cn.md) |
| 01 | [Programming as a Way of Thinking](think-python/ch01-thinking.md) | [编程是一种思维方式](think-python/ch01-thinking.cn.md) |
| 02 | [Variables and Statements](think-python/ch02-variables.md) | [变量与语句](think-python/ch02-variables.cn.md) |
| 03 | [Functions](think-python/ch03-functions.md) | [函数](think-python/ch03-functions.cn.md) |
| 04 | [Functions and Interfaces](think-python/ch04-interfaces.md) | [函数与接口](think-python/ch04-interfaces.cn.md) |
| 05 | [Conditionals and Recursion](think-python/ch05-conditionals.md) | [条件与递归](think-python/ch05-conditionals.cn.md) |
| 06 | [Return Values](think-python/ch06-return-values.md) | [返回值](think-python/ch06-return-values.cn.md) |
| 07 | [Iteration and Search](think-python/ch07-iteration.md) | [迭代与搜索](think-python/ch07-iteration.cn.md) |
| 08 | [Strings and Regular Expressions](think-python/ch08-strings.md) | [字符串与正则表达式](think-python/ch08-strings.cn.md) |
| 09 | [Lists](think-python/ch09-lists.md) | [列表](think-python/ch09-lists.cn.md) |
| 10 | [Dictionaries](think-python/ch10-dictionaries.md) | [字典](think-python/ch10-dictionaries.cn.md) |
| 11 | [Tuples](think-python/ch11-tuples.md) | [元组](think-python/ch11-tuples.cn.md) |
| 12 | [Text Analysis and Generation](think-python/ch12-text-analysis.md) | [文本分析与生成](think-python/ch12-text-analysis.cn.md) |
| 13 | [Files and Databases](think-python/ch13-files-databases.md) | [文件与数据库](think-python/ch13-files-databases.cn.md) |
| 14 | [Classes and Functions](think-python/ch14-classes-functions.md) | [类与函数](think-python/ch14-classes-functions.cn.md) |
| 15 | [Classes and Methods](think-python/ch15-classes-methods.md) | [类与方法](think-python/ch15-classes-methods.cn.md) |
| 16 | [Classes and Objects](think-python/ch16-classes-objects.md) | [类与对象](think-python/ch16-classes-objects.cn.md) |
| 17 | [Inheritance](think-python/ch17-inheritance.md) | [继承](think-python/ch17-inheritance.cn.md) |
| 18 | [Python Extras](think-python/ch18-extras.md) | [Python 附加特性](think-python/ch18-extras.cn.md) |
| 19 | [Final Thoughts](think-python/ch19-final-thoughts.md) | [最后的话](think-python/ch19-final-thoughts.cn.md) |

### 核心概念映射（Auto → Python）

| Auto | Python | 说明 |
|------|--------|------|
| `type Name { ... }` | `class Name:` | 类/结构体定义 |
| `fn init(&self, ...)` | `def __init__(self, ...)` | 构造函数 |
| `fn to_string(&self)` | `def __str__(self)` | 字符串表示 |
| `fn __add__(&self, other)` | `def __add__(self, other)` | 运算符重载 |
| `type Sub: Super {}` | `class Sub(Super):` | 继承 |
| `HashSet<T>` | `set` | 唯一值集合 |
| `HashMap<K, V>` | `dict` | 键值映射 |
| `if cond { a } else { b }` | `a if cond else b` | 条件表达式 |
