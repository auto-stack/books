# Introduction

Welcome to *The Auto Programming Language -- TypeScript Edition*. This book
teaches Auto to developers who already know TypeScript or JavaScript. Auto
gives you TypeScript's type safety with far less syntax, and it transpiles to
TypeScript via the **a2ts** transpiler so you can integrate it into any existing
TypeScript project.

## What This Book Covers

This book follows the structure of the TypeScript Handbook, chapter by chapter.
Each topic shows side-by-side Auto and TypeScript code so you can see exactly
how Auto maps to the language you already know.

The chapters progress from basics to advanced topics:

- **Basics** -- variables, primitive types, and control flow.
- **Everyday Types** -- unions, intersections, and common type patterns.
- **Narrowing** -- how Auto handles type narrowing with the `is` keyword.
- **Functions** -- parameter types, return types, and overloads.
- **Object Types** -- the `type` keyword, methods, and properties.
- **Creating Types from Types** -- mapped types, conditional types, and generics.
- **Type Operators** -- `keyof`, `typeof`, and other utility types.
- **Classes** -- how Auto's `type` replaces TypeScript's `class`.
- **Modules** -- imports, exports, and project organization.
- **Understanding Errors** -- reading and fixing compiler messages.

## Auto for TypeScript Developers

If you know TypeScript, much of Auto will feel familiar. Here are the key
differences you will encounter throughout this book:

- `type` instead of `class` -- Auto uses `type` for all user-defined types.
- `spec` instead of `interface` -- Auto's `spec` defines structural contracts.
- `is` instead of `switch` / pattern matching -- Auto unifies conditional logic
  under the `is` keyword.
- `let` / `var` instead of `let` / `let mut` -- Auto's `let` is immutable by
  default; `var` is mutable.
- `print()` instead of `console.log()` -- shorter to type, same result.

## How to Use This Book

This book works best when read in order from start to finish. Later chapters
build on concepts introduced in earlier ones. If you are already comfortable
with a topic, feel free to skip ahead and jump back when needed.

## A Note on Code Examples

Every code example in this book shows both the Auto version and the equivalent
TypeScript version. The Auto code can be transpiled to TypeScript using the
`a2ts` tool, so you can verify the output yourself.

An important part of learning Auto is learning to read compiler error messages.
We include examples that intentionally do not compile, along with the error
messages they produce. If you run an isolated snippet and it fails, check the
surrounding text for context.

## Source Code

The source files for this book can be found in the project repository.
