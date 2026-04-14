# Chapter 4: Expressions

> Level 1 — Acquaintance
>
> How C and Auto compose values through operators and evaluation.

Expressions are the workhorses of any program. Every computation — from adding two
numbers to deciding which branch to take — ultimately reduces to evaluating an
expression. C offers a rich set of operators; Auto keeps the same power but packages
it in a safer, more readable form.

---

## 4.1 Operands and Operators

An **operand** is a value that an operator acts upon. An **operator** specifies what
to do with its operand(s). C classifies operators by how many operands they take:

| Arity       | C example | Meaning              |
|-------------|-----------|----------------------|
| Unary       | `-x`      | Negation             |
| Binary      | `a + b`   | Addition             |
| Ternary     | `a ? b : c` | Conditional choice |

Auto uses the same classification but replaces the ternary `?:` with an `if/else`
expression syntax. The operator table below maps the most common C operators to their
Auto equivalents.

| Category         | C operator | Auto equivalent      | Notes                        |
|------------------|------------|----------------------|------------------------------|
| Arithmetic       | `+ - * / %` | `+ - * / %`        | Identical                    |
| Increment/Decr.  | `++ --`    | `x = x + 1`         | No side-effect operators     |
| Compound assign  | `+= -= *=` | `x = x + y`         | Explicit assignment          |
| Comparison       | `== != < > <= >=` | `== != < > <= >=` | Identical               |
| Logical          | `&& \|\| !` | `and or not`        | Word forms in Auto           |
| Ternary          | `a ? b : c` | `if a { b } else { c }` | Expression form         |
| Bitwise          | `& \| ^ ~ << >>` | same operators | Available in both            |

> **Takeaway:** Auto removes operators that modify objects in-place (`++`, `--`, `+=`)
> and replaces them with plain assignment. This makes every expression's effect
> explicit.

<Listing path="listings/ch04/listing-04-01" title="Arithmetic operators" />

---

## 4.2 Arithmetic

The five arithmetic operators are the same in C and Auto:

```
+  addition        -  subtraction
*  multiplication  /  division       %  remainder (modulo)
```

**Integer division** truncates toward zero in both languages. `17 / 5` yields `3`,
not `3.4`. The remainder operator `%` gives the leftover: `17 % 5` yields `2`.

Auto's `print` command handles output formatting automatically, unlike C's `printf`
which requires format specifiers like `%d` and `%f`.

```c
// C
printf("a + b = %d\n", a + b);

// Auto
print("a + b =", a + b)
```

---

## 4.3 Operators That Modify Objects

C provides operators that combine an operation with assignment:

```c
count++;        // count = count + 1
count += 3;     // count = count + 3
total -= discount;  // total = total - discount
```

Auto does **not** have `++`, `--`, or compound assignment operators. Instead you
write the full assignment:

```auto
count = count + 1
count = count + 3
total = total - discount
```

This is a deliberate design choice. In C, the increment operator `++` can appear as
a prefix or suffix, and the expression's *value* depends on which form you use:

```c
int a = 5;
int b = a++;   // b = 5, a becomes 6 (postfix)
int c = ++a;   // c = 7, a becomes 7 (prefix)
```

This dual nature — producing a value *and* modifying an object in the same
expression — is a common source of bugs. Auto eliminates the problem by separating
the read from the write.

> **Takeaway:** If you need to increment, write `x = x + 1`. It says exactly what
> it does, with no ambiguity about order of evaluation.

---

## 4.4 Boolean Context

In C, any scalar value can be tested in a boolean context:

- **Zero** (integer `0`, floating-point `0.0`, null pointer `NULL`) is **false**.
- **Everything else** is **true**.

```c
if (x) { /* x is non-zero */ }
if (!y) { /* y is zero */ }
```

Auto introduces a proper `bool` type with values `true` and `false`. The truth test
is the same — zero-like values are falsy — but Auto makes the type explicit:

```auto
let flag bool = true
if flag {
    print("flag is set")
}
```

<Listing path="listings/ch04/listing-04-02" title="Boolean values and ternary replacement" />

> **Takeaway (C Deep Dive):** Never compare explicitly against `0` or `1` for boolean
> tests. Write `if (ptr)` not `if (ptr != NULL)`, and `if (!done)` not
> `if (done == 0)`. The implicit boolean test is idiomatic C and reads more naturally.

---

## 4.5 Ternary Operator

C's conditional expression uses the `? :` operator:

```c
int max = (a > b) ? a : b;
const char *label = (x > 0) ? "positive" : "non-positive";
```

Auto replaces this with an `if/else` expression that returns a value:

```auto
let max int = if a > b { a } else { b }
let label str = if x > 0 { "positive" } else { "non-positive" }
```

The Auto form is more verbose but clearer: the two branches are visually separated
by braces, and there is no cryptic `? :` punctuation to decipher.

> **Takeaway:** The ternary operator is the *only* ternary operator in C. Auto
> generalizes the concept: any `if/else` block can be used as an expression when
> it appears in a value position.

---

## 4.6 Evaluation Order

> **C Deep Dive:** Evaluation order is one of the trickiest aspects of C. The
> language standard distinguishes between *precedence* (which operator binds
> tighter) and *sequencing* (which operand is evaluated first).

**Precedence** determines grouping: `a + b * c` is parsed as `a + (b * c)` because
`*` has higher precedence than `+`. This is the same in both languages.

**Sequencing** determines *when* side effects happen. In C, the order in which
operands are evaluated is largely **unspecified**. Consider:

```c
int a = 3;
int b = a++ + a++;   // UNDEFINED BEHAVIOR
```

Two modifications of `a` occur without an intervening *sequence point*. The compiler
is free to evaluate the left `a++` first, the right `a++` first, or anything in
between. The result is unpredictable.

Auto avoids this class of bugs entirely because it has no side-effect operators.
You cannot modify a variable as part of a sub-expression. The closest Auto code
requires separate statements:

```auto
var a int = 3
let tmp1 int = a
a = a + 1
let tmp2 int = a
a = a + 1
let b int = tmp1 + tmp2
```

**Sequence points in C** occur at:
- The `&&` and `||` operators (left operand fully evaluated first)
- The `?:` operator (condition evaluated, then exactly one branch)
- The comma operator (left operand evaluated and discarded)
- The end of a full expression (`;`)
- Function call entry and return

> **Takeaway:** In C, never modify the same variable twice between sequence points.
> In Auto, you literally cannot — the language prevents it.

---

## Quick Reference

| Concept            | C syntax            | Auto syntax                  |
|--------------------|---------------------|------------------------------|
| Addition           | `a + b`             | `a + b`                      |
| Integer division   | `a / b`             | `a / b`                      |
| Remainder          | `a % b`             | `a % b`                      |
| Increment          | `x++` or `++x`      | `x = x + 1`                  |
| Compound assign    | `x += 5`            | `x = x + 5`                  |
| Boolean test       | `if (x)`            | `if x`                       |
| Logical NOT        | `!x`                | `not x` or `!x`              |
| Ternary            | `c ? a : b`         | `if c { a } else { b }`      |
| Comparison         | `a == b`, `a != b`  | `a == b`, `a != b`           |

---

*Next: [Chapter 5 — Basic Values & Data](ch05-basic-values.md)*
