# Auto 编程语言

本仓库包含《Auto 编程语言》一书的源码。

主要内容采用 AutoDown 格式编写，
同时我们也提供了从 AutoDown 生成的 Markdown 格式版本。

## Rust 版本 — Auto 与 Rust 双语对照参考

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

## TypeScript 版本 — Auto 与 TypeScript 双语对照参考

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

## TypeScript 深入篇 — Auto 与 TypeScript 深度对照

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

## C 语言小书 — Auto 与 C 系统编程对照

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
