# The Basics

For most programming languages, code has to be *compiled* or *interpreted* before it
can run. In a statically typed language like Auto, the compiler checks your code for
type errors before it ever executes. Auto's `a2ts` transpiler goes one step further:
it produces TypeScript output that can be checked by `tsc` as well, giving you two
layers of type safety.

This chapter covers the core features of Auto that map directly to TypeScript
fundamentals. If you have written TypeScript before, most of these concepts will
feel familiar -- Auto just uses a leaner syntax to express them.

## Static Type-Checking

Auto is a statically typed language. That means the compiler knows the types of every
variable and expression at compile time, and it will reject code that mixes
incompatible types. For example, passing a `number` where a `string` is expected will
cause a compile error, just as it would in TypeScript.

The difference is that Auto checks these errors during transpilation with `a2ts`,
and the resulting TypeScript code preserves the types so `tsc` can catch anything
the Auto compiler missed. This dual-checking strategy means you get fast, clear
errors from `a2ts` and the full power of the TypeScript compiler as a safety net.

## Non-exception Failures

Type errors are not the only kind of error Auto catches at compile time. Typos in
property names, calling a function with the wrong number of arguments, and
forgetting to handle a `null` value are all caught before your code runs. In
JavaScript, these mistakes would surface only at runtime -- often as confusing
`undefined is not a function` errors. Auto eliminates an entire class of bugs that
TypeScript developers encounter every day.

## Types for Tooling

Because Auto has a static type system, editors can provide real-time feedback as
you type: autocomplete suggestions, inline error diagnostics, and automatic
refactoring support. This is the same tooling experience you get with TypeScript
today, and it works out of the box with the Auto language server.

## Hello, World

Every programming book starts with "Hello, World." Here is what it looks like in
Auto and the TypeScript that `a2ts` produces:

<Listing number="01-01" file="main">

```auto
fn main() {
    print("Hello, world!")
}
```

```typescript
/**
 * AutoLang TypeScript Runtime
 */
const print = console.log.bind(console);

function range(start: number, end: number, eq: boolean = false): number[] {
    const res: number[] = [];
    if (eq) {
        for (let i = start; i <= end; i++) res.push(i);
    } else {
        for (let i = start; i < end; i++) res.push(i);
    }
    return res;
}


function main(): void {
    console.log("Hello, world!");
}

main();
```

</Listing>

A few things to notice. Auto uses `fn` to declare a function and `print()` instead
of `console.log()`. There are no semicolons. The `a2ts` transpiler generates a
standard `function` with a `void` return type, calls `console.log` instead of
`print`, and appends a `main()` call at the bottom so the program actually runs.

## Explicit Types

Auto lets you annotate parameters and return types directly in the function
signature, using space-separated syntax instead of TypeScript's colon-separated
annotations:

<Listing number="01-02" file="main">

```auto
fn greet(person str, date Date) {
    print(f"Hello ${person}, today is ${date.toDateString()}!")
}
```

```typescript
/**
 * AutoLang TypeScript Runtime
 */
const print = console.log.bind(console);

function range(start: number, end: number, eq: boolean = false): number[] {
    const res: number[] = [];
    if (eq) {
        for (let i = start; i <= end; i++) res.push(i);
    } else {
        for (let i = start; i < end; i++) res.push(i);
    }
    return res;
}

function greet(person: string, date: Date): void {
    console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}
```

</Listing>

In Auto, each parameter has its type listed after the name, separated by a space:
`person str` means "a parameter named `person` of type `str`." The `a2ts`
transpiler converts this to TypeScript's `person: string` syntax. Return types use
the same space-separated convention -- if we wanted to return a `str`, we would
write `fn greet() str { ... }`.

String interpolation in Auto uses `f"..."` with `${expr}` placeholders, which maps
directly to TypeScript's template literal syntax.

## Type Inference

You do not always have to write type annotations. Auto can infer the type of a
variable from its initializer, just like TypeScript:

<Listing number="01-03" file="main">

```auto
fn main() {
    let msg = "hello there!"
    print(msg)
}
```

```typescript
/**
 * AutoLang TypeScript Runtime
 */
const print = console.log.bind(console);

function range(start: number, end: number, eq: boolean = false): number[] {
    const res: number[] = [];
    if (eq) {
        for (let i = start; i <= end; i++) res.push(i);
    } else {
        for (let i = start; i < end; i++) res.push(i);
    }
    return res;
}

function main(): void {
    const msg = "hello there!";
    console.log(msg);
}

main();
```

</Listing>

The variable `msg` is initialized with a string literal, so Auto infers its type as
`str`. The `a2ts` transpiler emits `const` because Auto's `let` is immutable by
default. If you need a mutable variable, you would use `var` in Auto, which
transpiles to `let` in TypeScript.

## Erased Types

Auto types exist only at compile time. When `a2ts` transpiles your code to
TypeScript, the type annotations are preserved in the TypeScript output for `tsc`
to check, but they have no effect at runtime. This is the same model TypeScript
uses: types are erased when TypeScript is compiled to JavaScript. In Auto's case,
the types are erased one step earlier, during the `a2ts` to TypeScript transpilation
-- but the generated TypeScript retains them for the downstream `tsc` check.

## Strictness

Auto is strict by default. There is no `strict` flag to toggle -- you get full
type checking from the moment you start writing code. This means `noImplicitAny`
and `strictNullChecks` are always enabled. In TypeScript, these are opt-in
compiler options that many projects enable via `tsconfig.json`. Auto bakes them
into the language because experience shows that strict mode catches the most common
and damaging bugs.

If you are coming from a TypeScript project that does not use strict mode, you may
see more compile errors at first. This is intentional -- Auto would rather surface
a bug at compile time than let it slip through to runtime.

## Quick Reference

The table below summarizes the core syntax differences between Auto and TypeScript
covered in this chapter:

| Concept | Auto | TypeScript |
|---------|------|-----------|
| Immutable variable | `let x = 5` | `const x = 5` |
| Mutable variable | `var x = 5` | `let x = 5` |
| Type annotation | `x int` | `x: number` |
| Function | `fn add(a int, b int) int` | `function add(a: number, b: number): number` |
| Print | `print("msg")` | `console.log("msg")` |
| String interpolation | `f"text ${x}"` | `` `text ${x}` `` |
