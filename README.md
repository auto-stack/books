# The Auto Programming Language

This repository contains the source of "The Auto Programming Language" book,
plus five bilingual (EN/CN) reference books that show how Auto maps to other languages.

The main source is in AutoDown format,
we also provide a Markdown format generated from AutoDown.

## Book Collection

This repository contains **five** companion books, each adapting a well-known programming
book for the Auto language. Every book provides paired **English** (`.md`) and **Chinese**
(`.cn.md`) chapters with runnable code listings.

| # | Book | Directory | Source | Chapters | Transpiler | Focus |
|---|------|-----------|--------|----------|------------|-------|
| 1 | [Auto vs Rust](#rust-version--auto-vs-rust-bilingual-reference) | [`rust/`](rust/) | [*The Rust Programming Language*](https://doc.rust-lang.org/book/) | 22 (ch00-21 + appendix) | `a2r` → Rust | Systems programming, ownership, actors, async |
| 2 | [Auto vs TypeScript](#typescript-version--auto-vs-typescript-bilingual-reference) | [`typescript/`](typescript/) | [*TypeScript Handbook*](https://www.typescriptlang.org/docs/handbook/) · [GitHub](https://github.com/microsoft/TypeScript-New-Handbook) | 10 (ch00-09) | `a2ts` → TypeScript | Web development, types, classes, modules |
| 3 | [Auto vs TypeScript DeepDive](#typescript-deepdive--auto-vs-typescript-in-depth) | [`typescript-deepdive/`](typescript-deepdive/) | [*TypeScript Deep Dive*](https://basarat.gitbook.io/typescript/) · [GitHub](https://github.com/basarat/typescript-book) | 16 (ch00-15) | `a2ts` → TypeScript | Advanced type system, generics, pattern matching |
| 4 | [Auto vs Little C](#little-c--auto-vs-c-systems-programming) | [`little-c/`](little-c/) | [*The Little Book of C*](https://little-book-of-c.github.io/) · [GitHub](https://github.com/little-book-of/c) | 10 (ch00-09) | `a2c` → C | Intro to C: memory, pointers, structs, I/O |
| 5 | [Auto vs Modern C](#modern-c--auto-vs-modern-c-deep-reference) | [`modern-c/`](modern-c/) | [*Modern C* by Jens Gustedt](https://gustedt.gitlabpages.inria.fr/modern-c/) | 22 (ch00-21) | `a2c` → C | Rigorous C: memory model, threads, atomics |

**Total: 80 chapters, ~45 code listings with transpiler output, all EN + CN.**

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