# Compiler Architecture

This chapter explains how compilers work by walking through the pipeline that
both TypeScript and Auto share. Rather than treating the compiler as a black
box, we will open it up and examine each stage: from raw source text all the
way to emitted output. Understanding this pipeline is essential for
comprehending error messages, debugging type issues, and knowing what happens
"under the hood" when you press compile.

## The Compilation Pipeline

Both TypeScript and Auto compilers follow the same general pipeline. Each stage
has a **single responsibility** and communicates with the next through
well-defined data structures:

```
┌──────────┐    ┌────────┐    ┌───────┐    ┌───────┐    ┌─────────┐    ┌─────────┐
│  Source   │───▶│Scanner │───▶│Tokens │───▶│Parser │───▶│  AST    │───▶│ Binder  │
│  Code     │    │ (Lexer)│    │       │    │       │    │         │    │         │
└──────────┘    └────────┘    └───────┘    └───────┘    └─────────┘    └─────────┘
                                                                      │
                                                                      ▼
┌─────────┐    ┌─────────┐    ┌───────┐    ┌───────┐    ┌─────────┐  ┌─────────┐
│  Output  │◀───│ Emitter │◀───│ Types │◀───│Checker│◀───│ Symbols │◀─┘         │
│  (JS/TS) │    │         │    │       │    │       │    │         │            │
└─────────┘    └─────────┘    └───────┘    └───────┘    └─────────┘            │
                                                                          ┌─────┴──────┐
                                                                          │   Binder   │
                                                                          └────────────┘
```

In short: **Source Code** becomes **Tokens**, which become an **AST**, which
produces **Symbols**, which are checked to produce **Types**, which are emitted
as **Output**.

Each stage is independent and can be tested in isolation. This modularity is
what makes it possible to build language servers, formatters, and linters that
reuse parts of the pipeline without running the full compiler.

## Scanner (Lexer)

The **scanner** (also called the **lexer**) converts raw source text into a
stream of **tokens**. A token is the smallest meaningful unit of source code.
Each token carries two pieces of information:

- **Kind** — what type of token it is (keyword, identifier, literal, operator,
  punctuation)
- **Position** — where it appears in the source file (line, column, offset)

TypeScript's scanner is accessible via `ts.createScanner()`, which returns
`SyntaxKind` enum values for each token. Auto's scanner follows the same design,
producing Auto-specific token types.

Consider this simple declaration:

```
let x = 42
```

The scanner produces the following token stream:

```
[LetKeyword, Identifier("x"), EqualsToken, IntLiteral(42), EndOfFileToken]
```

Notice that whitespace is **discarded** — the scanner strips spaces, newlines,
and comments (unless configured to preserve them for tools like formatters).
The scanner performs no semantic analysis. It does not know (or care) whether
`x` has been declared. Its job is purely **lexical**: recognizing the shape of
tokens in the text.

**Scanner errors** are the most basic compiler errors. They include
unrecognized characters and unterminated string literals. If you have ever seen
an error like "Unexpected character" in your editor, that came from the scanner
stage.

## Parser

The **parser** converts the token stream into an **Abstract Syntax Tree (AST)**.
An AST is a hierarchical, tree-shaped representation of the program's structure.
Each node in the tree has:

- **Kind** — what grammatical construct it represents (function, variable, call
  expression, etc.)
- **Position** — where it appears in the source (inherited from tokens)
- **Children** — nested nodes that form the subtree

TypeScript's AST uses the `SyntaxKind` enum to identify node types, with over
500 distinct values covering every possible JavaScript and TypeScript construct.
Auto uses a similar AST structure with Auto-specific node types.

The parser is **recursive descent** — each grammar rule is implemented as a
function that calls other functions. For example, `parseFunctionDeclaration()`
calls `parseIdentifier()`, then `parseParameterList()`, then `parseBlock()`.

Parsing our `let x = 42` example produces:

```
VariableDeclaration
├── IdentifierToken  "let"
├── Identifier       "x"
├── EqualsToken      "="
└── IntLiteral       42
```

**Parser errors** include syntax errors: missing semicolons, mismatched
brackets, and invalid token sequences. These are the "Expected X, got Y"
messages you see in editors.

## Binder

The **binder** walks the AST and creates **Symbols** — the semantic building
blocks of the program. This is where the compiler transitions from **syntax**
(what the code looks like) to **semantics** (what the code means).

A **Symbol** connects a name to its declaration. When the parser encounters
`let x = 42`, it creates a `VariableDeclaration` node. The binder then creates
a `Symbol` for `x` and stores a reference to that node. Later, when the parser
encounters `x` used in an expression, the binder resolves it to the same
`Symbol`.

```
AST (syntax)                    Symbols (semantics)
─────────────                   ──────────────────
let x = 42        ──────────▶   Symbol("x") → VariableDeclaration
x + 1             ──────────▶   Symbol("x") → resolved to same declaration
```

Without the binder, the AST is just a tree of tokens. The binder adds
**meaning** by establishing the relationships between declarations and their
uses. This is how the compiler knows that `x` in `x + 1` refers to the `x`
declared on line 3, not some other `x`.

In TypeScript, the binder is not called directly — it is driven by the checker
on demand. This lazy approach means that only the parts of the program that are
actually type-checked get bound.

## Type Checker

The **type checker** is the largest and most complex component in both
compilers. TypeScript's checker alone is over 23,000 lines of code. Its
responsibilities include:

- **Type checking** all expressions and statements for correctness
- **Type inference** — determining the type of `let x = 42` without an explicit
  annotation
- **Resolving generics** — substituting type parameters with concrete types
- **Generating diagnostics** — producing the error and warning messages you see
  in your editor

The checker consumes two inputs:

```
AST (from parser)  +  Symbols (from binder)  →  Types + Diagnostics
```

A key design decision in TypeScript is **lazy type resolution**. Types are not
checked eagerly — they are resolved on demand. When the language server needs
the type of a particular expression (for hover information, for example), the
checker resolves just enough to answer that query. This is what makes TypeScript
responsive even on large codebases.

Auto's type checker follows a similar model but enforces **stricter rules**:
there is no `any` type, no implicit `undefined`, and generics are checked at
definition time rather than use time. This means Auto can catch more errors at
compile time, at the cost of slightly more verbose type annotations.

## Emitter

The **emitter** takes the validated AST and type information and produces the
final output. This is the stage that actually generates the code your program
will run.

TypeScript has **two** emitters:

| Emitter | Input | Output |
|---------|-------|--------|
| JavaScript emitter | TypeScript AST | JavaScript (`.js`) |
| Declaration emitter | TypeScript AST | Type declarations (`.d.ts`) |

Auto's emitter targets TypeScript as its primary output, which can then be
compiled to JavaScript by the TypeScript compiler. For native targets, Auto
also has a Rust emitter:

| Emitter | Input | Output |
|---------|-------|--------|
| TypeScript emitter | Auto AST | TypeScript (`.ts`) |
| Rust emitter | Auto AST | Rust (`.rs`) |

The emitter **preserves comments and formatting** where possible, so that the
output remains readable. It also generates **source maps** — files that map each
position in the output back to the corresponding position in the original
source. Source maps are what make it possible to set breakpoints and read stack
traces in your original TypeScript or Auto code, even though the browser is
running JavaScript.

## Auto vs TypeScript Compiler

While both compilers share the same pipeline architecture, there are important
differences in how each stage works:

```
TypeScript Pipeline:
  Source → Scanner → Tokens → Parser → AST → Binder → Symbols
  → Checker → Types → JS Emitter → .js
                        └──────→ .d.ts Emitter → .d.ts

Auto Pipeline:
  Source → Scanner → Tokens → Parser → AST → Binder → Symbols
  → Checker → Types → TS Emitter → .ts → (tsc) → .js
                        └──────→ Rust Emitter → .rs
```

Key architectural differences:

- **Output target**: Auto compiles to TypeScript (then JS), not directly to JS.
  This means Auto can emit type annotations that TypeScript preserves.

- **Stricter checking**: Auto has no `any` type, no bivariance in generic
  constraints, and no implicit `undefined`. The checker rejects more programs
  at compile time.

- **Pattern matching**: Auto's `is` keyword adds **exhaustiveness checking** to
  the type checker. When you write a `match` on a tagged union, the checker
  verifies that every variant is handled.

- **Has composition**: Auto's `has` keyword composes types together. This is
  resolved at compile time by the binder, which expands `has` into the
  equivalent structural type.

- **Error propagation**: Auto's `?` operator for error propagation is
  transformed by the emitter into `try`/`catch` blocks in the output
  TypeScript. This means error handling in Auto is ergonomic at the source
  level but compiles to standard JavaScript error handling.

<Listing name="pipeline" file="listings/ch15-pipeline">

```auto
// Auto — this file demonstrates the compilation pipeline
// The Auto compiler transforms this source through these stages:
//
// 1. SCANNER:  Converts text to tokens
//    "fn add(a int, b int) int { a + b }"
//    → [FnKeyword, Identifier("add"), LParen, Identifier("a"),
//       IntKeyword, Comma, Identifier("b"), IntKeyword, RParen,
//       IntKeyword, LBrace, Identifier("a"), Plus, Identifier("b"), RBrace]
//
// 2. PARSER:   Converts tokens to AST
//    → FunctionDecl(name: "add", params: [Param("a", int), Param("b", int)],
//                    return_type: int, body: BinaryExpr(Ident("a"), Plus, Ident("b")))
//
// 3. BINDER:   Creates symbols from AST declarations
//    → Symbol("add"), Symbol("a"), Symbol("b")
//
// 4. CHECKER:  Validates types and resolves generics
//    → int + int = int ✓ (return type matches annotation)
//
// 5. EMITTER:  Generates TypeScript output
//    → function add(a: number, b: number): number { return a + b; }

fn add(a int, b int) int {
    a + b
}

fn main() {
    print("add(3, 4) = {add(3, 4)}")
}
```

</Listing>

The same function written in TypeScript goes through a parallel pipeline:

```typescript
// TypeScript — the TypeScript compiler pipeline
// This file demonstrates the TypeScript compilation stages:
//
// 1. SCANNER:  Converts text to tokens
//    "function add(a: number, b: number): number { return a + b; }"
//    → [FunctionKeyword, Identifier("add"), LParen, Identifier("a"),
//       Colon, NumberKeyword, Comma, Identifier("b"), Colon,
//       NumberKeyword, RParen, Colon, NumberKeyword, LBrace,
//       ReturnKeyword, Identifier("a"), Plus, Identifier("b"), Semicolon, RBrace]
//
// 2. PARSER:   Converts tokens to AST
//    → FunctionDeclaration(name: "add", params: [...], returnType: NumberKeyword,
//                          body: Block(ReturnStatement(BinaryExpression(...))))
//
// 3. BINDER:   Creates symbols for all declarations
//    → Symbol("add", flags: Function), Symbol("a"), Symbol("b")
//
// 4. CHECKER:  Type checks and validates
//    → number + number = number ✓
//
// 5. EMITTER:  Generates JavaScript output
//    → function add(a, b) { return a + b; }

function add(a: number, b: number): number {
    return a + b;
}

console.log("add(3, 4) = " + add(3, 4));
```

Notice how much more verbose the TypeScript token stream is. Each type annotation
(`: number`) generates three tokens (identifier, colon, keyword). Auto's
space-separated annotations are more concise at the token level.

## Quick Reference

| Concept | TypeScript | Auto |
|---------|-----------|------|
| Scanner API | `ts.createScanner()` | Internal scanner module |
| AST node identification | `SyntaxKind` enum (500+ values) | `SyntaxKind` enum (Auto-specific) |
| Parser strategy | Recursive descent | Recursive descent |
| Symbol creation | Binder (driven by checker) | Binder (same lazy approach) |
| Type checker size | ~23,000 lines | Smaller (stricter, fewer escapes) |
| Primary output | `.js` + `.d.ts` | `.ts` (then `.js` via tsc) |
| Secondary output | Source maps | Source maps + optional `.rs` |
| Error propagation | `try`/`catch` | `?` operator (emitted as `try`/`catch`) |
| Pattern matching exhaustiveness | Not checked | Checked by the type checker |
| Type system strictness | Configurable (`strict` flag) | Always strict (no `any`) |
| Lazy type resolution | Yes | Yes |
