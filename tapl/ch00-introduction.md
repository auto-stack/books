# Introduction

Welcome to *The Auto Programming Language*.

Auto is a programming language designed for the AI era. It gives you the speed of a systems language, the clarity of a scripting language, and the concurrency model of an operating system — all in one coherent design. Whether you are writing a quick script, a high-performance server, or code that an AI agent generates on your behalf, Auto is built to make that work natural and reliable.

This book will teach you Auto from the ground up. No prior experience with the language is assumed. By the end, you will understand not just the syntax, but the philosophy behind it — and you will have built real projects along the way.

## What Is Auto?

Auto is a modern programming language with three foundational ideas:

- **Tasks** — lightweight, isolated units of work that communicate through messages. Think of them as processes in an operating system, but at the language level.
- **Mailboxes** — typed message queues that connect tasks. Every piece of data that flows between concurrent units passes through a mailbox, making communication explicit and safe.
- **AutoVM** — a virtual machine that runs Auto code with fast startup, hot-reloading, and a read-eval-print loop (REPL) for interactive development.

These three concepts form the core of what we call **AIOS** — the Auto Intelligent Operating System. Auto does not just give you a language; it gives you a programming environment that works the way an operating system works: with processes, message passing, and a runtime that manages everything beneath.

If that sounds ambitious, it is. But Auto is also a language you can learn in an afternoon. The AIOS architecture only appears when you need it. For your first program, you just write code.

## Language as AIOS

Most programming languages treat concurrency as an afterthought — something you bolt on with libraries and frameworks. Auto takes a different approach. It treats the programming environment itself as an operating system.

An operating system has processes, inter-process communication, and a kernel that manages resources. Auto has tasks, mailboxes, and the AutoVM. The parallel is deliberate. When you write Auto code, you are not just writing functions that call each other. You are defining tasks that communicate through typed channels, running inside a virtual machine that handles scheduling, memory, and safety.

This is the **microkernel perspective**: a small, trustworthy core (the AutoVM) that provides essential services, with everything else — including concurrency, error handling, and even type checking — built as composable layers on top.

The benefit is profound. When your programming language works like an operating system, concurrency stops being scary. Message passing stops being an optimization trick. And the boundary between "my code" and "the runtime" becomes clear and well-defined.

## Dual Mode: VM and AOT

Auto gives you two ways to run your code, and they share the same semantics.

**AutoVM** is the development mode. You start the VM, load your code, and iterate. Change a function, hit save, see the result. The REPL lets you experiment with expressions interactively. Errors appear immediately, with clear messages that point to the problem. AutoVM is designed for the feedback loop — the cycle of writing, running, and refining that makes programming feel alive.

**AOT** (Ahead-of-Time) is the production mode. When you are ready to ship, you compile your Auto program to a native binary. No virtual machine, no runtime overhead. The same code that ran in the VM now runs as a zero-cost executable, competitive with hand-written C or Rust. The compiler applies optimizations that would be impossible in an interpreted language, because it has the full picture of your program at compile time.

Same language. Same semantics. Two radically different execution modes, each optimized for its purpose. You develop in the VM. You ship as AOT. The transition is seamless.

## AI-Native Design

Auto is designed for a world where much of the code you interact with is written — or at least suggested — by AI. This is not an afterthought. It is a first-class design goal.

What does it mean for a language to be AI-native? Three things:

1. **High signal-to-noise ratio.** Every token in an Auto program carries meaning. There is little boilerplate, few mandatory annotations, and no ceremonial syntax. When an AI generates Auto code, each token it produces is more likely to matter — which means each token is more likely to be correct.

2. **Predictable semantics.** Auto avoids surprising corner cases. The language behaves the way you expect, consistently. This makes it easier for AI models to generate correct code, because there are fewer hidden traps to fall into.

3. **Gradual complexity.** Auto starts simple and adds power as you need it. You can write a working program with just variables, functions, and control flow. Types, generics, actors, and comptime metaprogramming are there when you are ready for them — but they never get in your way at the start.

If you are a human writing Auto, these properties mean less code to read, write, and debug. If you are an AI generating Auto, they mean more correct output per token. Either way, you win.

## How This Book Works

This book teaches Auto through a **five-language format**. Every code listing shows the Auto version alongside equivalent code in Rust, Python, C, and TypeScript. If you already know one of those languages, the comparison will be your anchor. If you do not, do not worry — the Auto code stands on its own, and the surrounding text explains everything.

The book is organized into three phases:

- **Phase 1: Auto as Script** (Chapters 1–5). You learn the basics — variables, functions, control flow, collections — and run everything in AutoVM. No types, no complexity. Just code that works.
- **Phase 2: Auto as System** (Chapters 6–14). You add types, enums, error handling, memory management, and generics. This is where Auto shows its systems-language DNA.
- **Phase 3: Auto as AIOS** (Chapters 15–22). You unlock the full power of Auto's actor model, async programming, comptime metaprogramming, and the standard library. This is where Auto becomes an operating system for your code.

Each phase builds on the one before it. By the time you reach Phase 3, you will have the foundation to understand why Auto's concurrency model works the way it does — and you will have built real projects to prove it.

## Who This Book Is For

This book is for two kinds of readers.

**Beginners** who want to learn programming through Auto. Phase 1 is written with you in mind. It introduces programming concepts — variables, functions, loops — using Auto's clean syntax, without overwhelming you with type theory or memory management. If you have never written a line of code, start here.

**Experienced developers** coming from Rust, Python, C, or TypeScript. You will find the five-language format especially useful: every new concept is shown in a language you already know, so you can map your existing mental model onto Auto's way of doing things. You may want to skim Phase 1 and slow down in Phase 2, where Auto's type system and memory model start to diverge from what you are used to.

You do not need to know any particular language to read this book. You do need a general understanding of what programming is. If the phrase "variable assignment" means nothing to you, consider reading a general introduction to programming first, then come back.

## Conventions Used in This Book

The following conventions appear throughout:

- **Terminal commands** are prefixed with `$`. Everything after the `$` is what you type; everything before it is the shell prompt.

  ```
  $ auto run hello.auto
  ```

- **Code listings** show Auto first, then comparisons in other languages. A listing might look like this:

  ```
  // Auto
  fn greet(name) {
      print("Hello, {name}!")
  }
  ```

  Followed by equivalent code in Rust, Python, C, and TypeScript.

- **Bold** is used for new terms when they are first introduced.
- *Italics* are used for emphasis and for file names.

Now, let us begin. Turn the page to Chapter 1, where you will install Auto, write your first program, and see the language in action.
