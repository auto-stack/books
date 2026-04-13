# The Auto Programming Language

This repository contains the source of "The Auto Programming Language" book.

The main source is in AutoDown format,
we also provide a Markdown format generated from AutoDown.

## Rust Version — Auto vs Rust Bilingual Reference

The [`rust/`](rust/) directory contains a complete adaptation of "The Rust Programming Language" book
for the Auto programming language, with paired Auto/Rust code examples in every chapter.

Each chapter is provided in **English** (`.md`) and **Chinese** (`.cn.md`):

| Ch | English | Chinese |
|----|---------|---------|
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
| App | [Appendix](rust/appendix-reference.md) | [附录](rust/appendix-reference.cn.md) |

### Key Concept Mappings

| Rust | Auto | Description |
|------|------|-------------|
| `struct` | `type` | Data type definition |
| `impl` | `ext` | Method attachment |
| `trait` | `spec` | Shared behavior interface |
| `match` | `is` | Pattern matching |
| `Option<T>` | `?T` | Optional value |
| `Result<T,E>` | `!T` | Error propagation |
| `async`/`await` | `~T`/`on` | Async blueprints |
| `unsafe` | `sys` | System-level code |
| `macro_rules!` | `#[]` comptime | Compile-time metaprogramming |
| threads | actors | Concurrency model |
| `Cargo` | `automan` | Package manager |




