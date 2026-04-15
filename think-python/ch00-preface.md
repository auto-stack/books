# Preface

This book is based on [*Think Python*, 3rd edition](https://greenteapress.com/wp/think-python-3rd-edition) by Allen B. Downey, adapted to teach programming using the **Auto** language.

## Who Is This Book For

If you want to learn to program, you have come to the right place.
Auto is an excellent programming language for beginners -- its minimal, regular syntax lets you focus on learning programming concepts rather than wrestling with complex language rules.

This book is primarily for people who have never programmed before, and for people who have some experience in another programming language and want to learn Auto.
If you have substantial experience in Auto already, you might find the first few chapters too slow.

One of the challenges of learning to program is that you have to learn *two* languages at once: the programming language itself, and the vocabulary we use to talk about programs.
If you learn only the programming language, you are likely to have problems when you need to interpret an error message, read documentation, or communicate with other programmers.
This book defines each term when it first appears and includes a glossary at the end of every chapter.

## Goals of the Book

The first goal of this book is to teach you how to program in Auto.
But learning to program means learning a new way of thinking, so the second goal is to help you think like a computer scientist.
This way of thinking combines some of the best features of mathematics, engineering, and natural science.
Like mathematicians, computer scientists use formal languages to denote ideas -- specifically, computations.
Like engineers, they design things, assembling components into systems and evaluating trade-offs among alternatives.
Like scientists, they observe the behavior of complex systems, form hypotheses, and test predictions.

I tried to be concise.
The less mental effort it takes to read the book, the more capacity you will have for programming.
But you can't learn to program just by reading a book -- you have to practice.
For that reason, this book includes exercises at the end of every chapter where you can apply what you have learned.

## Navigating the Book

Each chapter in this book builds on the previous ones, so you should read them in order and take time to work on the exercises before you move on.

The first six chapters introduce basic elements like arithmetic, conditionals, and loops.
They also introduce the most important concept in programming -- functions -- and a powerful way to use them: recursion.

Later chapters introduce strings, lists, dictionaries, tuples, and other data structures.
You will also learn about object-oriented programming, files and databases, and more advanced topics.

The goal of this book is not to cover the entire Auto language.
Rather, it focuses on a subset of the language that provides the greatest capability with the fewest concepts.

## What's New in the Auto Edition

This edition adapts *Think Python* to teach programming using **Auto**, a modern language designed for the AI era.
The key differences from the original Python-based book are:

- **Syntax**: Auto uses `let` for variable declarations, `fn` for functions, and `{}` for code blocks, giving it a clean and consistent structure.
- **Type system**: Auto is statically typed with type inference, which helps catch errors early.
- **Transpilation**: Auto code can be transpiled to Python, Rust, TypeScript, and C using tools like `a2p`, `a2r`, `a2ts`, and `a2c`.
- **Dual code blocks**: Every listing in this book shows both the Auto source code and the equivalent Python output produced by the `a2p` transpiler, so you can see exactly how Auto maps to a language you may already know.

The conceptual content -- problem-solving strategies, debugging techniques, and programming vocabulary -- remains the same.
The goal is to help you learn to think like a computer scientist, using Auto as the vehicle.

## Getting Started

To run the programs in this book, you need the Auto toolchain.

1. **Install Auto**: Download the toolchain from <https://auto.dev> and follow the installation instructions for your platform.

2. **Verify the installation**: Open a terminal and run `autoc --version` to confirm it is installed correctly.

3. **Run a program**: Write your Auto code in a file with the `.at` extension, then compile and run it:
   ```
   autoc your_file.at
   ```

4. **Transpile to Python**: Use the `a2p` transpiler to convert Auto code to Python:
   ```
   a2p your_file.at
   ```

Every listing in this book includes both the Auto source code (`.at`) and the expected Python output (`main.expected.py`), so you can see the direct mapping between Auto and Python.

## Something To Think About

> The only way to learn a new programming language is by writing programs in it. -- Dennis Ritchie

> Everyone knows that debugging is twice as hard as writing a program in the first place. So if you are as clever as you can be when you write it, how will you ever debug it? -- Brian Kernighan
