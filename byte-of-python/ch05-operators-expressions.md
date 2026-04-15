# Operators and Expressions

Most statements (logical lines) that you write will contain _expressions_. A simple example of an expression is `2 + 3`. An expression can be broken down into operators and operands.

_Operators_ are functionality that do something and can be represented by symbols such as `+` or by special keywords. Operators require some data to operate on and such data is called _operands_. In this case, `2` and `3` are the operands.

## Operators

We will briefly take a look at the operators and their usage.

Here is a quick overview of the available operators:

### Arithmetic Operators

- `+` (plus)
    - Adds two objects
    - `3 + 5` gives `8`. `"a" + "b"` gives `"ab"`.

- `-` (minus)
    - Gives the subtraction of one number from the other; if the first operand is absent it is assumed to be zero.
    - `-5.2` gives a negative number and `50 - 24` gives `26`.

- `*` (multiply)
    - Gives the multiplication of the two numbers or returns the string repeated that many times.
    - `2 * 3` gives `6`. `"la" * 3` gives `"lalala"`.

- `**` (power)
    - Returns x to the power of y
    - `3 ** 4` gives `81` (i.e. `3 * 3 * 3 * 3`)

- `/` (divide)
    - Divide x by y
    - `13 / 3` gives `4.333333333333333`

- `//` (divide and floor)
    - Divide x by y and round the answer _down_ to the nearest integer value. Note that if one of the values is a float, you'll get back a float.
    - `13 // 3` gives `4`
    - `-13 // 3` gives `-5`

- `%` (modulo)
    - Returns the remainder of the division
    - `13 % 3` gives `1`. `-25.5 % 2.25` gives `1.5`.

### Comparison Operators

- `<` (less than)
    - Returns whether x is less than y. All comparison operators return `true` or `false`.
    - `5 < 3` gives `false` and `3 < 5` gives `true`.
    - Comparisons can be chained arbitrarily: `3 < 5 < 7` gives `true`.

- `>` (greater than)
    - Returns whether x is greater than y
    - `5 > 3` returns `true`.

- `<=` (less than or equal to)
    - Returns whether x is less than or equal to y
    - `x = 3; y = 6; x <= y` returns `true`

- `>=` (greater than or equal to)
    - Returns whether x is greater than or equal to y
    - `x = 4; y = 3; x >= 3` returns `true`

- `==` (equal to)
    - Compares if the objects are equal
    - `x = 2; y = 2; x == y` returns `true`
    - `x = "str"; y = "stR"; x == y` returns `false`
    - `x = "str"; y = "str"; x == y` returns `true`

- `!=` (not equal to)
    - Compares if the objects are not equal
    - `x = 2; y = 3; x != y` returns `true`

> **Note for Python Programmers:**
>
> Auto uses lowercase `true` and `false` for boolean values, while Python uses `True` and `False`. The `a2p` transpiler converts `true` to `True` and `false` to `False` automatically.

### Boolean Operators

- `!` (boolean NOT)
    - If x is `true`, it returns `false`. If x is `false`, it returns `true`.
    - `x = true; !x` returns `false`.
    - In the transpiled Python code, this becomes `not x`.

- `&&` (boolean AND)
    - `x && y` returns `false` if x is `false`, else it returns evaluation of y.
    - `x = false; y = true; x && y` returns `false` since x is false. This uses short-circuit evaluation.
    - In the transpiled Python code, this becomes `x and y`.

- `||` (boolean OR)
    - If x is `true`, it returns `true`, else it returns evaluation of y.
    - `x = true; y = false; x || y` returns `true`. Short-circuit evaluation applies here as well.
    - In the transpiled Python code, this becomes `x or y`.

> **Note for Python Programmers:**
>
> Auto uses `!`, `&&`, and `||` for boolean operations, while Python uses `not`, `and`, and `or`. The `a2p` transpiler converts these automatically. This is similar to the syntax used in languages like JavaScript, Rust, and C.

### Bitwise Operators

- `&` (bit-wise AND)
    - Bit-wise AND of the numbers: if both bits are `1`, the result is `1`. Otherwise, it's `0`.
    - `5 & 3` gives `1` (`0101 & 0011` gives `0001`)

- `|` (bit-wise OR)
    - Bitwise OR of the numbers: if both bits are `0`, the result is `0`. Otherwise, it's `1`.
    - `5 | 3` gives `7` (`0101 | 0011` gives `0111`)

- `^` (bit-wise XOR)
    - Bitwise XOR of the numbers: if both bits (`1 or 0`) are the same, the result is `0`. Otherwise, it's `1`.
    - `5 ^ 3` gives `6` (`0101 ^ 0011` gives `0110`)

- `~` (bit-wise invert)
    - The bit-wise inversion of x is -(x+1)
    - `~5` gives `-6`.

- `<<` (left shift)
    - Shifts the bits of the number to the left by the number of bits specified.
    - `2 << 2` gives `8`. `2` is represented by `10` in bits.
    - Left shifting by 2 bits gives `1000` which represents the decimal `8`.

- `>>` (right shift)
    - Shifts the bits of the number to the right by the number of bits specified.
    - `11 >> 1` gives `5`.
    - `11` is represented in bits by `1011` which when right shifted by 1 bit gives `101` which is the decimal `5`.

### Assignment Operators

You can combine an arithmetic operator with assignment for a convenient shortcut:

- `=` -- assign a value
- `+=` -- add and assign (`a += 1` is the same as `a = a + 1`)
- `-=` -- subtract and assign
- `*=` -- multiply and assign
- `/=` -- divide and assign
- `//=` -- floor divide and assign
- `%=` -- modulo and assign
- `**=` -- power and assign

For example:

```auto
let a = 2
a *= 3
```

Notice that `var = var operation expression` becomes `var operation= expression`.

## Operator Precedence

If you had an expression such as `2 + 3 * 4`, is the addition done first or the multiplication? Our high school maths tells us that the multiplication should be done first. This means that the multiplication operator has higher precedence than the addition operator.

The following table gives the precedence table for Auto, from the lowest precedence (least binding) to the highest precedence (most binding). This means that in a given expression, Auto will first evaluate the operators and expressions lower in the table before the ones listed higher in the table.

It is far better to use parentheses to group operators and operands appropriately in order to explicitly specify the precedence. This makes the program more readable. See [Changing the Order of Evaluation](#changing-the-order-of-evaluation) below for details.

| Precedence | Operator | Description |
|---|---|---|
| Lowest | `\|\|` | Boolean OR |
| | `&&` | Boolean AND |
| | `!` | Boolean NOT |
| | `<`, `<=`, `>`, `>=`, `==`, `!=` | Comparisons |
| | `\|` | Bitwise OR |
| | `^` | Bitwise XOR |
| | `&` | Bitwise AND |
| | `<<`, `>>` | Shifts |
| | `+`, `-` | Addition and subtraction |
| | `*`, `/`, `//`, `%` | Multiplication, Division, Floor Division and Remainder |
| | `+x`, `-x`, `~x` | Positive, Negative, bitwise NOT |
| | `**` | Exponentiation |
| Highest | `x[index]`, `x.attr`, `x(args)` | Subscription, attribute reference, call |

Operators that have not yet been covered will be explained in later chapters.

Operators with the _same precedence_ are listed in the same row in the above table. For example, `+` and `-` have the same precedence.

> **Note for Python Programmers:**
>
> The operator precedence in Auto is the same as in Python. The boolean operators `&&`/`||`/`!` in Auto have the same precedence as `and`/`or`/`not` in Python.

## Changing the Order of Evaluation

To make the expressions more readable, we can use parentheses. For example, `2 + (3 * 4)` is definitely easier to understand than `2 + 3 * 4` which requires knowledge of the operator precedences. As with everything else, the parentheses should be used reasonably (do not overdo it) and should not be redundant, as in `(2 + (3 * 4))`.

There is an additional advantage to using parentheses -- it helps us to change the order of evaluation. For example, if you want addition to be evaluated before multiplication in an expression, then you can write something like `(2 + 3) * 4`.

Let's see this in action:

<Listing number="5-1" file-name="expression.auto" caption="Operator precedence demonstration">

```auto
fn main() {
    // Operator precedence demonstration
    let result = 2 + 3 * 4
    print(result)

    // Parentheses change the order
    let result2 = (2 + 3) * 4
    print(result2)

    // Mixed operations
    let a = 2 + 3 * 4 - 10 / 2
    print(a)

    // Power has higher precedence than multiplication
    let b = 2 * 3 ** 2
    print(b)

    // Boolean operators and comparison
    let x = 5
    let y = 10
    let z = x > 3 && y < 20
    print(z)

    let w = !(x == 5) || y > 15
    print(w)
}
```

```python
def main():
    # Operator precedence demonstration
    result = 2 + 3 * 4
    print(result)

    # Parentheses change the order
    result2 = (2 + 3) * 4
    print(result2)

    # Mixed operations
    a = 2 + 3 * 4 - 10 / 2
    print(a)

    # Power has higher precedence than multiplication
    b = 2 * 3 ** 2
    print(b)

    # Boolean operators and comparison
    x = 5
    y = 10
    z = x > 3 and y < 20
    print(z)

    w = not (x == 5) or y > 15
    print(w)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The first expression `2 + 3 * 4` gives `14` because multiplication has higher precedence than addition, so `3 * 4` is evaluated first (giving `12`), then `2 + 12` gives `14`.

The second expression `(2 + 3) * 4` gives `20` because the parentheses force the addition to be evaluated first: `2 + 3` gives `5`, then `5 * 4` gives `20`.

The mixed operations example `2 + 3 * 4 - 10 / 2` follows the precedence rules: multiplication and division first (`3 * 4 = 12`, `10 / 2 = 5.0`), then addition and subtraction from left to right (`2 + 12 - 5.0 = 9.0`).

For the power example, `3 ** 2` is evaluated first (giving `9`), then `2 * 9` gives `18`.

The boolean examples show how `&&` (and) and `||` (or) combine with comparison operators. Notice that in the transpiled Python code, `&&` becomes `and`, `||` becomes `or`, and `!` becomes `not`.

## Associativity

Operators are usually associated from left to right. This means that operators with the same precedence are evaluated in a left to right manner. For example, `2 + 3 + 4` is evaluated as `(2 + 3) + 4`.

## Expressions

Let's put everything together and calculate the area and perimeter of a rectangle, as well as the area of a circle:

<Listing number="5-2" file-name="area.auto" caption="Calculating area using arithmetic expressions">

```auto
fn main() {
    // Calculate rectangle area and perimeter
    let length = 5
    let breadth = 2

    let area = length * breadth
    print(f"Area is $area")

    let perimeter = 2 * (length + breadth)
    print(f"Perimeter is $perimeter")

    // Calculate circle area
    let radius = 5.0
    let pi = 3.14159
    let circle_area = pi * radius ** 2
    print(f"Circle area is $circle_area")

    // Using compound assignment
    let total = 10
    total += 5
    print(total)
    total -= 3
    print(total)
    total *= 2
    print(total)
}
```

```python
def main():
    # Calculate rectangle area and perimeter
    length = 5
    breadth = 2

    area = length * breadth
    print(f"Area is {area}")

    perimeter = 2 * (length + breadth)
    print(f"Perimeter is {perimeter}")

    # Calculate circle area
    radius = 5.0
    pi = 3.14159
    circle_area = pi * radius ** 2
    print(f"Circle area is {circle_area}")

    # Using compound assignment
    total = 10
    total += 5
    print(total)
    total -= 3
    print(total)
    total *= 2
    print(total)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The length and breadth of the rectangle are stored in variables by the same name. We use these to calculate the area and perimeter of the rectangle with the help of expressions. We store the result of the expression `length * breadth` in the variable `area` and then print it using an f-string with `$area` interpolation. In the second case, we use the value of the expression `2 * (length + breadth)` and store it in `perimeter`.

For the circle area, we use the `**` (power) operator to calculate `radius ** 2` (radius squared), then multiply by `pi`. The result uses `radius = 5.0` (a float) so the circle area is also a float.

Finally, we demonstrate the compound assignment operators (`+=`, `-=`, `*=`). These are shortcuts that combine an arithmetic operation with assignment. `total += 5` is equivalent to `total = total + 5`, and so on.

## Summary

We have seen how to use operators, operands and expressions -- these are the basic building blocks of any program. In this chapter, we covered:

- **Arithmetic operators**: `+`, `-`, `*`, `**`, `/`, `//`, `%`
- **Comparison operators**: `<`, `>`, `<=`, `>=`, `==`, `!=`
- **Boolean operators**: `!` (not), `&&` (and), `||` (or)
- **Bitwise operators**: `&`, `|`, `^`, `~`, `<<`, `>>`
- **Assignment operators**: `=`, `+=`, `-=`, `*=`, `/=`, `//=`, `%=`, `**=`
- **Operator precedence** determines the order in which operations are performed
- **Parentheses** can be used to explicitly change the order of evaluation
- **Associativity** means operators of the same precedence are evaluated left to right

Next, we will see how to make use of these in our programs using control flow statements.
