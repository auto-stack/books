# The Auto Programming Language

This repository contains the source of "The Auto Programming Language" book,
plus five bilingual (EN/CN) reference books that show how Auto maps to other languages.

The main source is in AutoDown format,
we also provide a Markdown format generated from AutoDown.

## Book Collection

This repository contains the original **"The Auto Programming Language"** book,
plus **seven** companion reference books that show how Auto maps to other languages.
Every book provides paired **English** (`.md`) and **Chinese** (`.cn.md`) chapters
with runnable code listings.

| # | Book | Directory | Source | Chapters | Transpiler | Focus |
|---|------|-----------|--------|----------|------------|-------|
| 1 | [The Auto Programming Language](#the-auto-programming-language) | [`tapl/`](tapl/) | Original | 22 (ch00-21) + 4 appendices | All 5 languages | The definitive guide to Auto: scripting → systems → AIOS |
| 2 | [Auto vs The Rust Programming Language](#auto-vs-the-rust-programming-language) | [`rust/`](rust/) | [*The Rust Programming Language*](https://doc.rust-lang.org/book/) | 22 (ch00-21 + appendix) | `a2r` → Rust | Systems programming, ownership, actors, async |
| 3 | [Auto vs TypeScript Handbook](#auto-vs-typescript-handbook) | [`typescript/`](typescript/) | [*TypeScript Handbook*](https://www.typescriptlang.org/docs/handbook/) · [GitHub](https://github.com/microsoft/TypeScript-New-Handbook) | 10 (ch00-09) | `a2ts` → TypeScript | Web development, types, classes, modules |
| 4 | [Auto vs TypeScript DeepDive](#auto-vs-typescript-deepdive) | [`typescript-deepdive/`](typescript-deepdive/) | [*TypeScript Deep Dive*](https://basarat.gitbook.io/typescript/) · [GitHub](https://github.com/basarat/typescript-book) | 16 (ch00-15) | `a2ts` → TypeScript | Advanced type system, generics, pattern matching |
| 5 | [Auto vs Little Book of C](#auto-vs-the-little-book-of-c) | [`little-c/`](little-c/) | [*The Little Book of C*](https://little-book-of-c.github.io/) · [GitHub](https://github.com/little-book-of/c) | 10 (ch00-09) | `a2c` → C | Intro to C: memory, pointers, structs, I/O |
| 6 | [Auto vs Modern C](#auto-vs-modern-c) | [`modern-c/`](modern-c/) | [*Modern C* by Jens Gustedt](https://gustedt.gitlabpages.inria.fr/modern-c/) | 22 (ch00-21) | `a2c` → C | Rigorous C: memory model, threads, atomics |
| 7 | [A Byte of Auto (Python)](#a-byte-of-auto-python) | [`byte-of-python/`](byte-of-python/) | [*A Byte of Python*](https://python.swaroopch.com/) · [GitHub](https://github.com/swaroopch/byte-of-python) | 17 (ch00-16) | `a2p` → Python | Python basics: functions, OOP, exceptions, stdlib |
| 8 | [Think Python 3e — Auto Edition](#think-python-3e--auto-edition) | [`think-python/`](think-python/) | [*Think Python, 3rd Edition*](https://greenteapress.com/wp/think-python-3rd-edition/) (Allen B. Downey) | 20 (ch00-19) | `a2p` → Python | Programming thinking: recursion, OOP, data structures, text analysis |

**Total: 143 chapters, ~148 code listings with transpiler output, all EN + CN.**

## The Auto Programming Language

The [`tapl/`](tapl/) directory contains the original "The Auto Programming Language" book — the
definitive guide to Auto, written from scratch. Every code example is shown in **five languages**
(Auto, Rust, Python, C, TypeScript) so developers from any background can learn by comparison.

The book is organized in three progressive phases:

- **Phase 1 — Auto as Script** (Ch 1–5): Variables, functions, control flow, collections, guessing game project
- **Phase 2 — Auto as System** (Ch 6–14): Types, enums, OOP, error handling, modules, references, memory, generics, file processor project
- **Phase 3 — Auto as AIOS** (Ch 15–22): Actor concurrency, async, smart casts, testing, closures, comptime, stdlib, chat server project

Each chapter is provided in **English** (`.md`) and **Chinese** (`.cn.md`):

| Ch | Phase | English | Chinese |
|----|-------|---------|---------|
| 00 | — | [Introduction](tapl/ch00-introduction.md) | [简介](tapl/ch00-introduction.cn.md) |
| 01 | Script | [Getting Started](tapl/ch01-getting-started.md) | [入门](tapl/ch01-getting-started.cn.md) |
| 02 | Script | [Variables & Operators](tapl/ch02-variables-operators.md) | [变量与运算符](tapl/ch02-variables-operators.cn.md) |
| 03 | Script | [Functions & Control Flow](tapl/ch03-functions.md) | [函数与控制流](tapl/ch03-functions.cn.md) |
| 04 | Script | [Collections & Nodes](tapl/ch04-collections.md) | [集合与节点](tapl/ch04-collections.cn.md) |
| 05 | Script | [Project: Guessing Game](tapl/ch05-guessing-game.md) | [项目：猜数游戏](tapl/ch05-guessing-game.cn.md) |
| 06 | System | [Types & `let`](tapl/ch06-types.md) | [类型与 `let`](tapl/ch06-types.cn.md) |
| 07 | System | [Enums & Pattern Matching](tapl/ch07-enums.md) | [枚举与模式匹配](tapl/ch07-enums.cn.md) |
| 08 | System | [OOP Reshaped](tapl/ch08-oop.md) | [重塑面向对象](tapl/ch08-oop.cn.md) |
| 09 | System | [Error Handling](tapl/ch09-error-handling.md) | [错误处理](tapl/ch09-error-handling.cn.md) |
| 10 | System | [Packages & Modules](tapl/ch10-modules.md) | [包与模块](tapl/ch10-modules.cn.md) |
| 11 | System | [References & Pointers](tapl/ch11-references.md) | [引用与指针](tapl/ch11-references.cn.md) |
| 12 | System | [Memory & Ownership](tapl/ch12-memory.md) | [内存与所有权](tapl/ch12-memory.cn.md) |
| 13 | System | [Generics](tapl/ch13-generics.md) | [泛型](tapl/ch13-generics.cn.md) |
| 14 | System | [Project: File Processor](tapl/ch14-file-processor.md) | [项目：文件处理器](tapl/ch14-file-processor.cn.md) |
| 15 | AIOS | [Actor Concurrency](tapl/ch15-actors.md) | [Actor 并发](tapl/ch15-actors.cn.md) |
| 16 | AIOS | [Async with `~T`](tapl/ch16-async.md) | [异步编程 `~T`](tapl/ch16-async.cn.md) |
| 17 | AIOS | [Smart Casts & Flow Typing](tapl/ch17-smart-casts.md) | [智能转型与流式类型](tapl/ch17-smart-casts.cn.md) |
| 18 | AIOS | [Testing](tapl/ch18-testing.md) | [测试](tapl/ch18-testing.cn.md) |
| 19 | AIOS | [Closures & Iterators](tapl/ch19-closures.md) | [闭包与迭代器](tapl/ch19-closures.cn.md) |
| 20 | AIOS | [Comptime & Metaprogramming](tapl/ch20-comptime.md) | [编译期计算与元编程](tapl/ch20-comptime.cn.md) |
| 21 | AIOS | [Standard Library Tour](tapl/ch21-stdlib.md) | [标准库概览](tapl/ch21-stdlib.cn.md) |
| 22 | AIOS | [Project: Multi-user Chat Server](tapl/ch22-chat-server.md) | [项目：多人聊天服务器](tapl/ch22-chat-server.cn.md) |

### Appendices

| Appendix | English | Chinese |
|----------|---------|---------|
| A | [Keyword Reference](tapl/appendix-a-keywords.md) | [关键字参考](tapl/appendix-a-keywords.cn.md) |
| B | [Operator Table](tapl/appendix-b-operators.md) | [运算符表](tapl/appendix-b-operators.cn.md) |
| C | [Transpiler Quick-Ref](tapl/appendix-c-transpiler-quick-ref.md) | [转译器速查](tapl/appendix-c-transpiler-quick-ref.cn.md) |
| D | [Standard Library Index](tapl/appendix-d-stdlib-index.md) | [标准库索引](tapl/appendix-d-stdlib-index.cn.md) |

### Key Concept Mappings (Auto vs All 5 Languages)

| Auto | Rust | Python | C | TypeScript | Description |
|------|------|--------|---|-----------|-------------|
| `type` | `struct` | `@dataclass` | `struct` | `interface`/`class` | Data type definition |
| `enum` | `enum` | `Union` | `enum` + tag | `type` union | Sum type |
| `spec` | `trait` | `Protocol`/`ABC` | vtable | `interface` | Behavioral contract |
| `is` | `match` | `match`/`isinstance` | `switch` | `switch` | Pattern matching |
| `ext` | `impl` | methods on class | functions | methods | Extension methods |
| `has` | composition | composition | nested struct | composition | Auto-delegation |
| `?T` | `Option<T>` | `T \| None` | tagged ptr | `T \| null` | Optional value |
| `!T` | `Result<T,E>` | `raise`/`try` | error codes | `try`/`catch` | Error result |
| `spawn`/`send` | `thread::spawn`/`mpsc` | `Thread`/`Queue` | `pthread`/pipe | `Worker`/`postMessage` | Actor concurrency |
| `~T` | `async fn` | `async def` | callbacks | `Promise<T>` | Async blueprint |
| `#[comptime]` | `const fn`/macros | decorators | preprocessor | decorators | Compile-time eval |
| `automan` | `cargo` | `pip`/`poetry` | `make`/`cmake` | `npm`/`pnpm` | Package manager |

## Auto vs The Rust Programming Language

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

## Auto vs TypeScript Handbook

The [`typescript/`](typescript/) directory contains a complete adaptation of the "TypeScript Handbook v2" book
for the Auto programming language, with paired Auto/TypeScript code examples in every chapter.

Each chapter is provided in **English** (`.md`) and **Chinese** (`.cn.md`):

| Ch | English | Chinese |
|----|---------|---------|
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

### Key Concept Mappings

| TypeScript | Auto | Description |
|-----------|------|-------------|
| `class` | `type` | Data structure definition |
| `interface` | `spec` | Behavioral contract |
| `implements` | `as` | Interface implementation |
| `extends` | `is` | Inheritance |
| `class X extends Y` | — | Use `is` or `has` composition |
| `(x: number) => number` | `fn(int)int` | Function type (annotation) |
| `(x, y) => x + y` | `(x, y) => x + y` | Closure (value) |
| `readonly` | — | Use `let` for immutable variables |
| `keyof` / `typeof` / mapped types | — | TypeScript-only advanced types |
| `import` / `export` | `use` / `mod` | Module system |

## Auto vs TypeScript DeepDive

The [`typescript-deepdive/`](typescript-deepdive/) directory contains an in-depth exploration of TypeScript's type system
adapted for Auto, covering advanced patterns like discriminated unions, generics, and mapped types.

Each chapter is provided in **English** (`.md`) and **Chinese** (`.cn.md`):

| Ch | English | Chinese |
|----|---------|---------|
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

## Auto vs The Little Book of C

The [`little-c/`](little-c/) directory contains an adaptation of "The Little Book of C"
for Auto programmers targeting C via the a2c transpiler. Covers memory, pointers,
structs, I/O, system programming, debugging, and real-world project building.

Each chapter is provided in **English** (`.md`) and **Chinese** (`.cn.md`):

| Ch | English | Chinese |
|----|---------|---------|
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

### Key Concept Mappings (Auto → C)

| Auto | C | Description |
|------|---|-------------|
| `fn main()` | `int main(void)` | Entry point |
| `print("text")` | `printf("%s\n", "text")` | Print output |
| `type Point { x int, y int }` | `struct Point { int x; int y; };` | Struct definition |
| `enum Color { RED, GREEN, BLUE }` | `enum Color { COLOR_RED, ... };` | Enum definition |
| `is x { ... }` | `switch (x) { ... }` | Pattern matching / switch |
| `spec Drawable { fn draw() }` | vtable struct | Interface / vtable |
| `let x int = 5` | `const int x = 5;` | Immutable binding |
| `var x int = 5` | `int x = 5;` | Mutable variable |
| `for i in 0..10 { }` | `for (int i=0; i<10; i++) { }` | Counted loop |
| `auto a2c` / `auto b` | `gcc` / `make` | Build commands |

## Auto vs Modern C

The [`modern-c/`](modern-c/) directory contains a rigorous adaptation of "Modern C" (Jens Gustedt)
for Auto programmers. Covers the full C language across 4 levels: Encounter, Acquaintance,
Cognition, Experience — including the abstract state machine, memory model, type-generic
programming, threads, and atomics.

Each chapter is provided in **English** (`.md`) and **Chinese** (`.cn.md`):

| Ch | Level | English | Chinese |
|----|-------|---------|---------|
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

### Key Concept Mappings (Auto → Modern C)

| Auto | Modern C | Description |
|------|----------|-------------|
| `type` | `struct` + `typedef` | Data structure definition |
| `spec` | function pointer / vtable | Behavioral interface |
| `enum` | tagged union | Sum type / data enum |
| `is` | `switch` / `_Generic` | Pattern matching |
| `let`/`var` | `const`/mutable | Immutable/mutable binding |
| `var x = expr` | `auto x = expr` (C23) | Type inference |
| `fn` | function definition | Functions |
| `mod`/`use` | `#include` / headers | Module system |
| `#[]` comptime | preprocessor macros | Compile-time metaprogramming |
| actors | `thrd_*` / `mtx_*` | Concurrency model |
| `!T` error type | `errno` / `setjmp` | Error handling |
| AutoFree | `malloc`/`free` | Memory management |

## A Byte of Auto (Python)

The [`byte-of-python/`](byte-of-python/) directory contains an adaptation of "A Byte of Python" (Swaroop C H)
for the Auto programming language, with paired Auto/Python code examples in every chapter.
This is a beginner-friendly introduction to programming through Auto, which transpiles to Python.

Each chapter is provided in **English** (`.md`) and **Chinese** (`.cn.md`):

| Ch | English | Chinese |
|----|---------|---------|
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

### Key Concept Mappings (Auto → Python)

| Auto | Python | Description |
|------|--------|-------------|
| `fn main()` | `def main():` + `if __name__` | Entry point |
| `let x = 5` | `x = 5` | Variable declaration |
| `let mut x = 5` | `x = 5` | Mutable variable |
| `// comment` | `# comment` | Comments |
| `f"$name"` | `f"{name}"` | F-string interpolation |
| `type Name { ... }` | `class Name:` / `@dataclass` | Class/struct definition |
| `fn init(&self, ...)` | `def __init__(self, ...)` | Constructor |
| `.field` | `self.field` | Member access |
| `type Sub: Super {}` | `class Sub(Super):` | Inheritance |
| `for cond { ... }` | `while cond:` | While loop |
| `for i in 0..10 {}` | `for i in range(0, 10):` | For loop |
| `true`/`false` | `True`/`False` | Boolean values |
| `&&`/`||`/`!` | `and`/`or`/`not` | Logical operators |
| `List` | `list` | Ordered mutable collection |
| `HashMap` | `dict` | Key-value mapping |
| `HashSet` | `set` | Unique value collection |

## Think Python 3e — Auto Edition

The [`think-python/`](think-python/) directory contains an adaptation of "Think Python, 3rd Edition" (Allen B. Downey)
for the Auto programming language, with paired Auto/Python code examples in every chapter.
This book teaches programming as a way of thinking, covering recursion, object-oriented programming,
data structures, and text analysis through Auto code that transpiles to Python.

Each chapter is provided in **English** (`.md`) and **Chinese** (`.cn.md`):

| Ch | English | Chinese |
|----|---------|---------|
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

### Key Concept Mappings (Auto → Python)

| Auto | Python | Description |
|------|--------|-------------|
| `type Name { ... }` | `class Name:` | Class/struct definition |
| `fn init(&self, ...)` | `def __init__(self, ...)` | Constructor |
| `fn to_string(&self)` | `def __str__(self)` | String representation |
| `fn __add__(&self, other)` | `def __add__(self, other)` | Operator overloading |
| `type Sub: Super {}` | `class Sub(Super):` | Inheritance |
| `HashSet<T>` | `set` | Unique value collection |
| `HashMap<K, V>` | `dict` | Key-value mapping |
| `if cond { a } else { b }` | `a if cond else b` | Conditional expression |