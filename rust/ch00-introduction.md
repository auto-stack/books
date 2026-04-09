# Introduction

Welcome to *The Auto Programming Language*, an introductory book about Auto.
Auto is a systems programming language designed for the AI era. It helps you
write fast, reliable software with minimal ceremony. Where many languages force
you to choose between high-level ergonomics and low-level control, Auto
eliminates that trade-off—giving you both.

## Who Auto Is For

Auto is designed for a wide range of developers. Let's look at the most
important groups.

### Teams of Developers

Auto is a productive tool for teams of all sizes. Like Rust, its compiler
catches subtle bugs—including concurrency bugs—at compile time. But Auto goes
further: its implicit ownership model (`AutoFree`) and flow-sensitive typing
mean less annotation overhead and fewer compiler fights. The compiler works
*with* your team, not against it.

Auto comes with modern developer tools:

- **automan**, the package manager and build tool, makes managing dependencies
  simple and consistent.
- **autoc**, the compiler, provides clear error messages that guide you toward
  working code.
- **autovm**, the virtual machine runtime, enables hot-reloading and
  interactive development.

### Students and Learners

Auto is for anyone interested in systems programming concepts. Its syntax is
minimal and regular, making it an excellent vehicle for learning about memory
management, concurrency, and type systems—without the annotation burden of
more explicit languages.

### AI-Assisted Developers

Auto is designed from the ground up to work *with* AI code generators. Its
minimal syntax, predictable semantics, and compile-time safety guarantees mean
that AI-generated code is more likely to be correct on the first try. If
you use AI tools to write code, Auto is designed to be the language those
tools are happiest generating.

### People Who Value Speed and Stability

Auto is for people who crave speed and stability. By speed, we mean both
runtime performance and developer velocity. Auto's compiler checks ensure that
refactoring is safe. Its zero-cost abstractions mean that elegant, high-level
code compiles down to the same machine code you'd write by hand.

## Who This Book Is For

This book assumes you've written code in another programming language, but
makes no assumptions about which one. Whether you come from Python, JavaScript,
Rust, C++, or anywhere else, the material is designed to be broadly accessible.

We don't spend time explaining what programming *is*. If you're entirely new
to programming, you'd be better served by a general introduction to
programming first.

## How to Use This Book

This book assumes you're reading it in sequence from front to back. Later
chapters build on concepts from earlier ones.

You'll find two kinds of chapters: **concept chapters** and **project
chapters**. Concept chapters teach you about an aspect of Auto. Project
chapters walk you through building small programs. Chapter 2, Chapter 12, and
Chapter 21 are project chapters; the rest are concept chapters.

**Chapter 1** explains how to install Auto, write a "Hello, world!" program,
and use automan. **Chapter 2** is a hands-on introduction where you build a
number-guessing game.

In **Chapter 3**, you'll learn about variables, data types, functions, and
control flow. **Chapter 4** covers Auto's memory model—ownership, move
semantics, and how AutoFree replaces explicit lifetime annotations. **Chapter
5** discusses the `type` keyword and methods. **Chapter 6** covers enums,
pattern matching with the `is` keyword, and the `?T` optional type.

In **Chapter 7**, you'll learn about Auto's module system. **Chapter 8**
discusses common collections: `List`, `HashMap`, and `HashSet`. **Chapter 9**
explores error handling with `!T` and the `!` throw operator.

**Chapter 10** digs into generics, the `spec` system (Auto's take on traits),
and how AutoFree handles lifetimes implicitly. **Chapter 11** covers testing.
In **Chapter 12**, we build a command-line text search tool.

**Chapter 13** explores closures and iterators. **Chapter 14** examines
automan in depth. **Chapter 15** discusses Auto's reference and pointer
types.

In **Chapter 16**, we walk through the Actor concurrency model with `task` and
`mailbox`. **Chapter 17** covers async programming with `~T` futures and the
`on` block.

**Chapter 18** looks at how Auto's `is`/`has`/`spec` system relates to
object-oriented programming. **Chapter 19** is a reference on pattern
matching. **Chapter 20** covers advanced topics: the `sys` keyword (unsafe
operations), comptime with `#[]`, and more.

In **Chapter 21**, we'll build a multithreaded web server using Auto's Actor
model.

Finally, the appendixes contain reference material: Auto's keywords,
operators, and development tools.

There is no wrong way to read this book. If you want to skip ahead, go for it!
You can always jump back if something doesn't make sense.

## A Note on Code Examples

The code examples in this book show both **Auto** and **Rust** versions side
by side. The Auto version can be transpiled to the Rust version using the `a2r`
tool. This lets you leverage your existing Rust knowledge while learning Auto's
syntax and idioms.

An important part of learning Auto is learning how to read compiler error
messages. We'll show many examples that don't compile, along with the error
messages the compiler produces. If you enter and run a random example, it may
not compile—make sure you read the surrounding text to understand the context.

## Source Code

The source files for this book can be found in the project repository.
