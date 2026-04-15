# About Auto

Auto is one of those rare languages which can claim to be both _simple_ and _powerful_. You will find yourself pleasantly surprised to see how easy it is to concentrate on the solution to the problem rather than the syntax and structure of the language you are programming in.

The official introduction to Auto is:

> Auto is an easy to learn, powerful programming language. It has minimal, regular syntax and a clean approach to object-oriented programming. Auto's transpiled nature and static typing, together with its ability to target multiple backends, make it an ideal language for writing portable, high-performance applications in many domains.

I will discuss most of these features in more detail in the next section.

## Story Behind the Name

Auto is a programming language designed for the AI era. Its name reflects the goal of making programming feel _automatic_ — so intuitive that the code almost writes itself. Built with Rust, Auto combines the safety and performance of a systems language with the simplicity and ergonomics that modern developers expect.

The language was created to bridge the gap between human intent and machine execution. In an age where AI assistants help us write code, Auto's minimal syntax and predictable semantics make it the natural choice for human-AI collaboration.

## Features of Auto

### Simple

Auto is a simple and minimalistic language. Reading a good Auto program feels almost like reading English, although very strict English! This pseudo-code nature of Auto is one of its greatest strengths. It allows you to concentrate on the solution to the problem rather than the language itself.

### Easy to Learn

As you will see, Auto is extremely easy to get started with. Auto has an extraordinarily simple syntax, as already mentioned. The small surface area of the language means you spend less time memorizing rules and more time solving problems.

### Free and Open Source

Auto is an example of a _FLOSS_ (Free/Libre and Open Source Software). In simple terms, you can freely distribute copies of this software, read its source code, make changes to it, and use pieces of it in new free programs. FLOSS is based on the concept of a community which shares knowledge. This is one of the reasons why Auto is so good — it has been created and is constantly improved by a community who just want to see a better Auto.

### High-level Language

When you write programs in Auto, you never need to bother about the low-level details such as managing the memory used by your program. Auto's `AutoFree` system handles memory management implicitly, freeing you from manual allocation and deallocation.

### Portable

One of Auto's greatest strengths is its portability across programming environments. Auto code can be transpiled to multiple target languages — Python, Rust, TypeScript, and C — using transpilers like `a2p`, `a2r`, `a2ts`, and `a2c`. This means your Auto program can run anywhere these target languages run, without any changes to your Auto source code.

You can use Auto on GNU/Linux, Windows, macOS, and more — wherever the target language runtime or compiler is available.

### Transpiled

This requires a bit of explanation.

Unlike traditional compiled or interpreted languages, Auto uses a _transpilation_ approach. When you write an Auto program, the `autoc` compiler transpiles it into a target language of your choice. For example, using the `a2p` transpiler, your Auto code is converted into idiomatic Python code, which is then executed by the Python runtime.

This approach gives you the best of both worlds: you write code in Auto's clean, minimal syntax, but you get the performance and ecosystem benefits of the target language. No need to worry about linking libraries or managing binary compatibility — the target language's toolchain handles all of that.

### Object Oriented

Auto supports procedure-oriented programming as well as object-oriented programming (OOP). In _procedure-oriented_ languages, the program is built around procedures or functions which are nothing but reusable pieces of programs. In _object-oriented_ languages, the program is built around objects which combine data and functionality. Auto provides OOP through the `type` keyword, offering a powerful yet simple way to define types with fields and methods.

### Extensible

If you need a critical piece of code to run very fast, or want to leverage existing libraries in the target language, Auto makes it easy to interoperate with native code. Since Auto transpiles to well-known languages, you can call into any library available in those ecosystems directly.

### Embeddable

You can embed Auto code within other projects and applications. Auto modules can be used as part of larger codebases, giving your program's users the ability to extend functionality through Auto scripts.

### Extensive Libraries

Because Auto transpiles to Python, Rust, TypeScript, and C, you have access to an enormous ecosystem of libraries:

- **Python's PyPI** — hundreds of thousands of packages for web development, data science, machine learning, and more
- **Rust's crates.io** — high-quality crates for systems programming, web servers, and CLI tools
- **npm** — the JavaScript/TypeScript package ecosystem
- **C libraries** — decades of battle-tested systems libraries

This is Auto's _Unlimited Batteries Included_ philosophy — you are never limited by what comes in a standard library. If a library exists in any of the target languages, you can use it from Auto.

### Summary

Auto is indeed an exciting and powerful language. It has the right combination of simplicity, portability, and ecosystem access that makes writing programs in Auto both fun and easy. Whether you are a beginner writing your first program or an experienced developer building complex systems, Auto has something to offer you.
