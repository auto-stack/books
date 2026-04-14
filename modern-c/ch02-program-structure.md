# Program Structure

A C program is built from tokens, organized into declarations and statements, and compiled in a specific order. Auto simplifies this structure but preserves the same logical organization. This chapter walks through the grammar, declarations, definitions, and statements of both languages.

## 2.1 Grammar

C programs are made of *tokens*: identifiers, keywords, literals, operators, and punctuation. The C standard defines a precise grammar that determines which sequences of tokens form valid programs.

Here are the basic token categories in C:

- **Keywords:** `int`, `double`, `if`, `for`, `while`, `return`, `struct`, `switch`, `case`, `break`, `default`, `void`, `const`, ...
- **Identifiers:** names you choose -- `main`, `count`, `my_function`, `Point`
- **Literals:** `42`, `3.14`, `"hello"`, `true`
- **Operators:** `+`, `-`, `*`, `/`, `=`, `==`, `<`, `>`, `&&`, `||`, ...
- **Punctuation:** `(`, `)`, `{`, `}`, `;`, `,`

C's grammar is type-first. When you declare something, the type comes before the name:

```c
int x = 5;
double pi = 3.14159;
const char* greeting = "hello";
```

Auto's grammar is simpler. Types appear *after* names, and fewer keywords are needed:

```auto
let x int = 5
let pi float = 3.14159
let greeting str = "hello"
```

### Translation Units and Scope

A C program consists of one or more *translation units* -- source files that are compiled independently and then linked together. Each translation unit is processed in phases: preprocessing, tokenization, parsing, and code generation.

Auto follows the same model. Each `.at` file is a translation unit. The a2c transpiler processes each one independently, producing a `.c` file that is then compiled by the C compiler.

C has four scopes for identifiers:

- **Block scope:** visible within `{ ... }` (the most common).
- **File scope:** visible throughout the translation unit.
- **Function scope:** only for labels (rarely used).
- **Function prototype scope:** only within a function declaration.

Auto has two practical scopes: function scope (inside `fn`) and module scope (at the top level). The mapping is straightforward.

> **Takeaway:** C's grammar puts types first; Auto's grammar puts names first. Both carry the same information, but Auto's order reads more naturally in English: "let x be an int equal to 5."

## 2.2 Declarations

A *declaration* in C introduces a name and associates it with a type. The most common form is a variable declaration:

```c
int age = 25;
double height = 1.75;
char initial = 'A';
bool active = true;
```

In Auto, the `let` keyword introduces an immutable binding, and `var` introduces a mutable one:

```auto
let age int = 25       // immutable
let height float = 1.75
var count int = 0      // mutable
```

### Type Inference

Auto supports a limited form of type inference with `var`:

```auto
var x = 5              // inferred as int
var pi = 3.14159       // inferred as float
var name = "hello"     // inferred as str
```

The a2c transpiler infers the type from the initializer and generates the appropriate C type. C's `auto` keyword (added in C23) provides similar functionality, but Auto's `var` works across all target C standards because the inference happens at transpile time.

<Listing name="Declarations and Definitions" file="listings/ch02/listing-02-01">

The listing above shows all four basic types in action. Notice how Auto maps to C:

| Auto | C |
|---|---|
| `str` | `const char*` |
| `int` | `int` |
| `float` | `double` |
| `bool` | `bool` (with `<stdbool.h>`) |

### const and let

C's `const` qualifier marks a variable as read-only after initialization:

```c
const int x = 5;      // Cannot be modified
x = 10;               // Compilation error
```

Auto's `let` provides the same guarantee by convention -- `let` bindings cannot be reassigned. The a2c transpiler does not generate `const` for `let` bindings (since C `const` has different semantics in some contexts), but the intent is documented in the source.

> **C Deep Dive:** C distinguishes between *declarations* (announcing a name and its type) and *definitions* (allocating storage). In most cases a declaration is also a definition. The keyword `extern` can create a declaration that is not a definition, referring to a variable defined elsewhere. Auto has no equivalent of `extern` -- all bindings are definitions.

> **Takeaway:** Use `let` for values that do not change and `var` for values that do. The a2c transpiler maps both to C variable declarations, but the distinction documents your intent.

## 2.3 Definitions

In C, a *definition* creates an entity. Variables are defined when storage is allocated. Functions are defined when their body is provided.

```c
// Variable definition
int counter = 0;

// Function definition
int square(int x) {
    return x * x;
}
```

In Auto, the same concepts apply with cleaner syntax:

```auto
// Variable definition
var counter int = 0

// Function definition
fn square(x int) int {
    x * x
}
```

Notice the differences:

- Auto functions omit `return` for the last expression -- its value is the return value.
- Auto uses `fn` instead of the C return-type-first syntax.
- Parameters follow the name:type convention.

### Objects and Values

C uses the term *object* for a region of memory that holds a value. An object has:

- A *type* (what kind of value it holds).
- A *lifetime* (when the memory is valid).
- A *storage duration* (automatic, static, allocated, or thread).

Auto uses the same model under the hood. When you write `let x int = 5`, the a2c transpiler creates an `int` object with automatic storage duration. The value `5` is stored in that object.

> **C Deep Dive:** C has a concept of *tentative definitions* -- a file-scope declaration without an initializer may or may not be a definition depending on context. This is a source of subtle bugs. Auto avoids this entirely: every `let` or `var` at any scope is a full definition.

> **Takeaway:** Every Auto binding is a definition. There are no tentative or partial declarations.

## 2.4 Statements

A *statement* is an instruction that the program executes. C has several kinds:

- **Expression statements:** `x = 5;` -- an expression followed by a semicolon.
- **Iteration statements:** `for`, `while`, `do...while`.
- **Selection statements:** `if`, `switch`.
- **Jump statements:** `return`, `break`, `continue`, `goto`.

Auto provides the same categories with simpler syntax:

- **Expression statements:** `x = 5` -- no semicolon needed.
- **Iteration:** `for i in 0..n { }`, `while cond { }`.
- **Selection:** `if cond { }`, `is x { ... }`.
- **Jump:** `return` (often implicit).

<Listing name="Statements" file="listings/ch02/listing-02-02">

This listing demonstrates function definitions, variable mutation, a for loop, and function calls -- all the statement types from this chapter in one program.

The a2c transpiler converts each Auto statement to its C equivalent:

```auto
count = count + 1
```
becomes:
```c
count = count + 1;
```

And:

```auto
for i in 0..5 {
    count = count + 1
}
```
becomes:
```c
for (int i = 0; i < 5; i++) {
    count = count + 1;
}
```

### The Compound Statement

In C, a *compound statement* (or block) is a pair of braces enclosing zero or more declarations and statements:

```c
{
    int x = 5;
    x = x + 1;
    printf("%d\n", x);
}
```

Auto uses the same brace-delimited blocks:

```auto
{
    let x int = 5
    var y int = x + 1
    print(y)
}
```

The key difference: Auto does not require semicolons. Each statement occupies its own line (or is separated by newlines). This eliminates an entire class of syntax errors.

> **C Deep Dive:** In C, every statement must end with a semicolon (`;`). The semicolon is a statement terminator, not a separator. Forgetting it is one of the most common C compilation errors. Auto eliminates this entirely -- newlines serve as statement boundaries.

> **Takeaway:** Statements are the imperative building blocks. Auto simplifies their syntax while preserving C's execution model.

## Quick Reference

| Concept | C | Auto |
|---|---|---|
| Immutable binding | `const int x = 5;` | `let x int = 5` |
| Mutable binding | `int x = 5;` | `var x int = 5` |
| Type inference | `auto x = 5;` (C23) | `var x = 5` |
| String type | `const char*` | `str` |
| Float type | `double` | `float` |
| Boolean type | `bool` | `bool` |
| Function | `int f(int x) { return x; }` | `fn f(x int) int { x }` |
| Expression statement | `x = 5;` | `x = 5` |
| Compound statement | `{ ... }` | `{ ... }` |
| Semicolons | Required | Not used |
