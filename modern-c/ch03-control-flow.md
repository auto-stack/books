# Control Flow

Programs execute statements in order, top to bottom. Control flow statements change that order: they let you choose between paths, repeat blocks, or select among many options. This chapter covers the three primary control flow mechanisms -- conditionals, iterations, and multiple selection -- in both C and Auto.

## 3.1 Conditional Execution

The most basic control flow construct is the conditional: do this, or do that, depending on a condition.

### C's if/else

In C, `if` evaluates an expression. If the result is nonzero, the first branch executes. Otherwise, the `else` branch (if present) executes:

```c
if (x > 0) {
    printf("positive\n");
} else if (x < 0) {
    printf("negative\n");
} else {
    printf("zero\n");
}
```

The braces around the body are optional for single-statement branches, but Modern C style always uses them. This prevents a class of bugs where a maintenance edit adds a second statement but forgets to add braces.

### Auto's if/else

Auto uses the same logical structure, but without parentheses around the condition:

```auto
if x > 0 {
    print("positive")
} else if x < 0 {
    print("negative")
} else {
    print("zero")
}
```

Auto requires braces for all branches. There is no "optional braces" rule. This eliminates the dangling-else ambiguity and the single-statement brace-forgetting bug entirely.

### Truth and Falsehood

In C, truth is simple: zero is false, everything else is true. This applies to all scalar types:

```c
if (42)        // true
if (0)         // false
if (3.14)      // true
if (0.0)       // false
if (ptr)       // true if ptr is not NULL
if (!ptr)      // true if ptr is NULL
```

Auto inherits the same model. A nonzero value is truthy; zero is falsy. The `bool` type provides explicit boolean values `true` and `false`, but any condition expression works as in C.

> **C Deep Dive:** In C, *every* scalar value has a truth interpretation: zero is false, nonzero is true. This means `if (ptr)`, `if (count)`, and `if (difference != 0)` are all valid conditions. Modern C's advice is explicit: "Don't compare to 0, false, or null." But this is a stylistic choice, and many C programmers prefer the explicit comparison for clarity. Auto does not change this -- the same truth model applies.

<Listing name="Conditional Execution" file="listings/ch03/listing-03-01">

This listing defines a `classify` function that returns a string based on whether a number is positive, negative, or zero. The main function tests it on an array of five values.

The a2c transpiler maps the Auto function to C as follows:

```c
const char* classify(int n) {
    if (n > 0) {
        return "positive";
    } else if (n < 0) {
        return "negative";
    } else {
        return "zero";
    }
}
```

Notice how Auto's implicit return (the last expression in each branch becomes the return value) maps to C's explicit `return` statements. Each branch is a string literal, so the transpiler inserts `return` before each one.

> **Takeaway:** Conditionals choose between paths. C requires parentheses around conditions; Auto does not. Both evaluate truth the same way: nonzero is true, zero is false.

## 3.2 Iterations

Iteration lets you repeat a block of code. C provides three loop constructs; Auto provides two.

### For Loops

C's `for` loop has three components: initialization, condition, and increment:

```c
for (int i = 0; i < 10; i++) {
    printf("%d\n", i);
}
```

Auto replaces this with a range-based form:

```auto
for i in 0..10 {
    print(i)
}
```

The range `0..10` means "from 0 up to but not including 10." The a2c transpiler generates `for (int i = 0; i < 10; i++)`.

You can also use a starting value other than zero:

```auto
for i in 5..15 {
    // i goes from 5 to 14
}
```

This becomes `for (int i = 5; i < 15; i++)`.

### While Loops

Both C and Auto have `while` loops:

```c
// C
while (countdown > 0) {
    countdown = countdown - 1;
}
```

```auto
// Auto
while countdown > 0 {
    countdown = countdown - 1
}
```

The semantics are identical: check the condition, execute the body, repeat.

`while` is the right choice when you do not know the number of iterations in advance -- for example, waiting for user input, reading until end-of-file, or converging on a solution.

### Loop Variables and Scope

In C, a variable declared in the `for` initializer is scoped to the loop:

```c
for (int i = 0; i < 10; i++) {
    // i is visible here
}
// i is NOT visible here
```

Auto's range-based `for` works the same way. The loop variable `i` is created for the loop and is not accessible after it:

```auto
for i in 0..10 {
    // i is visible here
}
// i is NOT visible here
```

<Listing name="Iterations" file="listings/ch03/listing-03-02">

This listing demonstrates three iteration patterns:

1. **Counting up:** Sum the numbers 0 through 10 using a `for` loop with a range.
2. **Countdown:** Decrement a variable using a `while` loop until it reaches zero.
3. **Fibonacci:** Generate the first 10 Fibonacci numbers using a `for` loop with mutable state.

The Fibonacci example is particularly instructive. It uses `var` for `a` and `b` because they change each iteration, and `let` for `temp` because it is only used as a temporary within the loop body.

> **C Deep Dive:** C also has a `do...while` loop that checks the condition *after* the body executes, guaranteeing at least one iteration. Auto does not provide `do...while` because in practice, a regular `while` loop with the condition checked first covers most use cases, and the rare exceptions can be restructured. The `do...while` loop is also one of the few places in C where a semicolon appears after a closing brace: `do { ... } while (cond);`.

> **Takeaway:** Auto's `for i in 0..n` replaces C's `for (int i = 0; i < n; i++)`. Auto's `while` matches C's `while` directly. Both are zero-overhead abstractions over the same machine code.

## 3.3 Multiple Selection

When you need to choose among many options based on a single value, `switch` (in C) or `is` (in Auto) is cleaner than a chain of `if/else if` blocks.

### C's switch

C's `switch` statement jumps to a matching `case` label:

```c
switch (day) {
    case 1: printf("Monday\n"); break;
    case 2: printf("Tuesday\n"); break;
    case 3: printf("Wednesday\n"); break;
    case 4: printf("Thursday\n"); break;
    case 5: printf("Friday\n"); break;
    case 6: printf("Weekend\n"); break;
    case 7: printf("Weekend\n"); break;
    default: printf("Invalid\n"); break;
}
```

Each case ends with `break`. Without `break`, execution falls through to the next case. This fall-through behavior is one of C's most criticized features.

### Auto's is

Auto's `is` construct provides pattern matching without fall-through:

```auto
is day {
    1 => "Monday"
    2 => "Tuesday"
    3 => "Wednesday"
    4 => "Thursday"
    5 => "Friday"
    6 => "Weekend"
    7 => "Weekend"
    else => "Invalid"
}
```

Each arm is an independent expression. There is no fall-through. The a2c transpiler generates a `switch` with a `break` (or `return`) for each case.

### Why is Is Better Than switch

The `is` construct fixes three problems with C's `switch`:

1. **No fall-through.** You cannot forget a `break` because there is no `break` to forget.
2. **Expression semantics.** The entire `is` block is an expression that produces a value. You can assign it: `let result str = is day { ... }`.
3. **Exhaustiveness.** The `else =>` arm is required, forcing you to handle the default case explicitly.

> **C Deep Dive:** C's `switch` has *fall-through*: execution continues from the matched case into the next case unless a `break` statement is encountered. This is one of C's most notorious features. Forgetting a `break` is a classic bug. Modern C style often annotates intentional fall-through with `/* fall through */` comments or the `[[fallthrough]]` attribute (C23).

<Listing name="Multiple Selection" file="listings/ch03/listing-03-03">

The listing maps day numbers to day names using `is`. The transpiler converts it to a clean `switch` statement:

```c
const char* day_type(int day) {
    switch (day) {
        case 1: return "Monday";
        case 2: return "Tuesday";
        case 3: return "Wednesday";
        case 4: return "Thursday";
        case 5: return "Friday";
        case 6: return "Weekend";
        case 7: return "Weekend";
        default: return "Invalid";
    }
}
```

Notice:

- Each case has an explicit `return` -- no fall-through possible.
- The `else` arm maps to `default`.
- The generated C is idiomatic and safe.

> **Takeaway:** Use `is` for multi-way dispatch. It eliminates fall-through bugs by design and produces clean `switch` statements in the output.

## Quick Reference

| Construct | C | Auto |
|---|---|---|
| Conditional | `if (cond) { } else { }` | `if cond { } else { }` |
| Else-if chain | `else if (cond)` | `else if cond` |
| Required braces | No (but recommended) | Yes (mandatory) |
| For loop | `for (int i = 0; i < n; i++)` | `for i in 0..n` |
| While loop | `while (cond) { }` | `while cond { }` |
| Do-while | `do { } while (cond);` | (not provided) |
| Switch | `switch (x) { case ... }` | `is x { ... }` |
| Default case | `default:` | `else =>` |
| Fall-through | Possible (requires `break`) | Not possible |
| Truth values | Nonzero = true | Nonzero = true |
