# Functions and Interfaces

In this chapter we will use functions to draw text-based shapes, and demonstrate **interface design**, which is a way of designing functions that work together. Along the way we will learn about encapsulation, generalization, and refactoring -- three of the most important ideas in software development.

## Drawing with Characters

Instead of a graphical turtle, we will use characters like `*` and `#` to draw shapes in the terminal. This approach has an advantage: we can see the same design principles -- encapsulation, generalization, and refactoring -- without needing a graphics library.

For example, here is a simple "square" made of asterisks:

```
*****
*****
*****
*****
*****
```

We can draw this with a `for` loop that prints a row of characters repeatedly:

```auto
for i in 0..5 {
    print("*" * 5)
}
```

Before you go on, see if you can modify this program to draw a 3-by-7 rectangle.

## Encapsulation

Let's take the code that draws a repeated pattern and put it in a function.

<Listing number="4-1" file-name="encapsulation.auto" caption="Encapsulation: wrap repeated code in a function">

```auto
fn print_banner(text: str) {
    let border = "=" * (text.len() + 4)
    print(border)
    print("= $text =")
    print(border)
}

fn main() {
    // Before encapsulation: repeated code
    print("=========")
    print("= Hello =")
    print("=========")
    print()
    print("===========")
    print("= Welcome =")
    print("===========")
    print()
    print("========")
    print("= Bye =")
    print("========")

    print()

    // After encapsulation: call a function
    print_banner("Hello")
    print()
    print_banner("Welcome")
    print()
    print_banner("Bye")
}
```

```python
def print_banner(text):
    border = "=" * (len(text) + 4)
    print(border)
    print(f"= {text} =")
    print(border)


def main():
    # Before encapsulation: repeated code
    print("=========")
    print("= Hello =")
    print("=========")
    print()
    print("===========")
    print("= Welcome =")
    print("===========")
    print()
    print("========")
    print("= Bye =")
    print("========")

    print()

    # After encapsulation: call a function
    print_banner("Hello")
    print()
    print_banner("Welcome")
    print()
    print_banner("Bye")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The "before" section shows three blocks of code that each print a banner around a word. The three blocks are almost identical -- only the word changes. The "after" section defines `print_banner`, which takes `text` as a parameter and computes the border dynamically using `text.len() + 4`. Now we can call `print_banner` with any word and get a properly-sized banner.

Wrapping a piece of code up in a function is called **encapsulation**. One of the benefits of encapsulation is that it attaches a name to the code, which serves as a kind of documentation. Another advantage is that if you reuse the code, it is more concise to call a function twice than to copy and paste the body!

## Generalization

The next step is to add parameters to our drawing functions, making them more general.

<Listing number="4-2" file-name="generalization.auto" caption="Generalization: add parameters to make functions reusable">

```auto
// Draws a row of repeated characters
fn draw_row(ch: str, width: int) {
    print(ch * width)
}

// Draws a box of given width and height using a character
fn draw_box(ch: str, width: int, height: int) {
    draw_row(ch, width)
    for i in 0..(height - 2) {
        print("$ch" + " " * (width - 2) + "$ch")
    }
    if height > 1 {
        draw_row(ch, width)
    }
}

// Draws a centered box inside a wider line
fn draw_centered_box(ch: str, width: int, height: int, canvas_width: int) {
    let padding = (canvas_width - width) / 2
    for i in 0..height {
        print(" " * padding + draw_row_str(ch, width))
    }
}

// Helper: returns a row string without printing
fn draw_row_str(ch: str, width: int) -> str {
    ch * width
}

fn main() {
    // Simple row
    print("Simple row:")
    draw_row("*", 10)
    print()

    // Box
    print("Box 5x3:")
    draw_box("#", 5, 3)
    print()

    // Centered box on a wider canvas
    print("Centered box 7x3 on canvas of 15:")
    draw_centered_box("+", 7, 3, 15)
}
```

```python
def draw_row(ch, width):
    print(ch * width)


def draw_box(ch, width, height):
    draw_row(ch, width)
    for i in range(height - 2):
        print(f"{ch}" + " " * (width - 2) + f"{ch}")
    if height > 1:
        draw_row(ch, width)


def draw_centered_box(ch, width, height, canvas_width):
    padding = (canvas_width - width) // 2
    for i in range(height):
        print(" " * padding + draw_row_str(ch, width))


def draw_row_str(ch, width):
    return ch * width


def main():
    # Simple row
    print("Simple row:")
    draw_row("*", 10)
    print()

    # Box
    print("Box 5x3:")
    draw_box("#", 5, 3)
    print()

    # Centered box on a wider canvas
    print("Centered box 7x3 on canvas of 15:")
    draw_centered_box("+", 7, 3, 15)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`draw_row` takes a character `ch` and a `width`, and prints a single row. `draw_box` calls `draw_row` for the top and bottom edges, and prints a hollow middle with spaces. `draw_centered_box` adds a `canvas_width` parameter to center the box within a wider line.

Adding a parameter to a function is called **generalization** because it makes the function more general: with a fixed size, the function can only draw one shape; with parameters, it can draw many.

When a function has more than a few numeric arguments, it is easy to forget what they are, or what order they should be in. In Auto you can use named arguments to make calls clearer:

```auto
draw_centered_box(ch="+", width=7, height=3, canvas_width=15)
```

This use of the assignment operator, `=`, is a reminder about how arguments and parameters work -- when you call a function, the arguments are assigned to the parameters.

## Refactoring

Now suppose we want both filled and empty boxes. We could write two separate functions, but they would share a lot of the same logic. A better approach is to refactor.

<Listing number="4-3" file-name="refactoring.auto" caption="Refactoring: simplify and remove duplication">

```auto
// --- Before refactoring: duplicated logic ---

fn draw_filled_box(ch: str, width: int, height: int) {
    for i in 0..height {
        for j in 0..width {
            print(ch, terminator: "")
        }
        print()
    }
}

fn draw_empty_box(ch: str, width: int, height: int) {
    for i in 0..height {
        for j in 0..width {
            if i == 0 || i == height - 1 || j == 0 || j == width - 1 {
                print(ch, terminator: "")
            } else {
                print(" ", terminator: "")
            }
        }
        print()
    }
}

// --- After refactoring: shared helper ---

// Helper: returns a single row as a string
fn make_row(ch: str, fill: str, width: int, is_edge: bool) -> str {
    if is_edge {
        ch * width
    } else {
        "$ch" + fill * (width - 2) + "$ch"
    }
}

fn draw_box_v2(ch: str, width: int, height: int, filled: bool) {
    let fill = if filled { ch } else { " " }
    for i in 0..height {
        let is_edge = i == 0 || i == height - 1
        print(make_row(ch, fill, width, is_edge))
    }
}

fn main() {
    // Before refactoring: two separate functions
    print("Filled box 5x3:")
    draw_filled_box("*", 5, 3)
    print()

    print("Empty box 5x3:")
    draw_empty_box("#", 5, 3)
    print()

    // After refactoring: one function with a parameter
    print("Filled box 5x3 (v2):")
    draw_box_v2("*", 5, 3, true)
    print()

    print("Empty box 5x3 (v2):")
    draw_box_v2("#", 5, 3, false)
}
```

```python
def draw_filled_box(ch, width, height):
    for i in range(height):
        for j in range(width):
            print(ch, end="")
        print()


def draw_empty_box(ch, width, height):
    for i in range(height):
        for j in range(width):
            if i == 0 or i == height - 1 or j == 0 or j == width - 1:
                print(ch, end="")
            else:
                print(" ", end="")
        print()


def make_row(ch, fill, width, is_edge):
    if is_edge:
        return ch * width
    else:
        return f"{ch}" + fill * (width - 2) + f"{ch}"


def draw_box_v2(ch, width, height, filled):
    fill = ch if filled else " "
    for i in range(height):
        is_edge = i == 0 or i == height - 1
        print(make_row(ch, fill, width, is_edge))


def main():
    # Before refactoring: two separate functions
    print("Filled box 5x3:")
    draw_filled_box("*", 5, 3)
    print()

    print("Empty box 5x3:")
    draw_empty_box("#", 5, 3)
    print()

    # After refactoring: one function with a parameter
    print("Filled box 5x3 (v2):")
    draw_box_v2("*", 5, 3, True)
    print()

    print("Empty box 5x3 (v2):")
    draw_box_v2("#", 5, 3, False)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The "before" section has two functions: `draw_filled_box` uses nested `for` loops to print every cell as `ch`, while `draw_empty_box` uses a conditional to decide whether to print `ch` or a space. The two functions share the same outer loop structure.

The "after" section extracts a helper, `make_row`, that builds a single row as a string. `draw_box_v2` uses `make_row` and adds a `filled` parameter. If `filled` is `true`, the fill character is `ch` (same as the border); if `false`, the fill is a space. Now a single function handles both cases.

Changes like this, which improve the code without changing its behavior, are called **refactoring**. If we had planned ahead, we might have written `make_row` first and avoided refactoring, but often you don't know enough at the beginning of a project to design all the functions. Once you start coding, you understand the problem better. Sometimes refactoring is a sign that you have learned something.

## A Development Plan

A **development plan** is a process for writing programs. The process we used in this chapter is "encapsulation and generalization". The steps are:

1. Start by writing a small program with no function definitions.
2. Once you get the program working, identify a coherent piece of it, encapsulate the piece in a function and give it a name.
3. Generalize the function by adding appropriate parameters.
4. Repeat Steps 1 to 3 until you have a set of working functions.
5. Look for opportunities to improve the program by refactoring. For example, if you have similar code in several places, consider factoring it into an appropriately general function.

This process has some drawbacks -- we will see alternatives later -- but it can be useful if you don't know ahead of time how to divide the program into functions. This approach lets you design as you go along.

The design of a function has two parts:

* The **interface** is how the function is used, including its name, the parameters it takes and what the function is supposed to do.
* The **implementation** is how the function does what it's supposed to do.

For example, the "before" and "after" versions of `draw_box` have the same interface -- they take the same parameters and produce the same output -- but they have different implementations.

## Docstrings

A **docstring** is a comment at the beginning of a function that explains the interface ("doc" is short for "documentation"). Auto uses `//` for comments, and you can write multi-line docstrings using `//` on each line:

```auto
// Draws a row of repeated characters.
// ch: the character to repeat
// width: how many characters wide
fn draw_row(ch: str, width: int) {
    print(ch * width)
}
```

A docstring should:

* Explain concisely what the function does, without getting into the details of how it works,
* Explain what effect each parameter has on the behavior of the function, and
* Indicate what type each parameter should be, if it is not obvious.

Writing this kind of documentation is an important part of interface design. A well-designed interface should be simple to explain; if you have a hard time explaining one of your functions, maybe the interface could be improved.

## Stack Diagrams

When `draw_box` calls `draw_row`, we can use a stack diagram to show this sequence of function calls and the parameters for each one. Here is a text representation when `draw_box("#", 5, 3)` calls `draw_row("#", 5)`:

```
+-----------------------+
| main                  |
+-----------------------+
| draw_box              |
| ch -> "#"             |
| width -> 5            |
| height -> 3           |
+-----------------------+
| draw_row              |
| ch -> "#"             |
| width -> 5            |
+-----------------------+
```

Notice that the value of `ch` in `draw_row` is different from the value of `ch` in `draw_box` -- well, in this case they happen to be the same value, but the point is that parameters are local. You can use the same parameter name in different functions; it is a different variable in each function.

## Debugging

An interface is like a contract between a function and a caller. The caller agrees to provide certain arguments and the function agrees to do certain work.

For example, `draw_box` requires three arguments: `ch` should be a single character string; `width` should be a positive integer; and `height` should be a positive integer.

These requirements are called **preconditions** because they are supposed to be true before the function starts executing. Conversely, conditions at the end of the function are **postconditions**. Postconditions include the intended effect of the function (like printing a box) and any side effects.

Preconditions are the responsibility of the caller. If the caller violates a precondition and the function doesn't work correctly, the bug is in the caller, not the function.

If the preconditions are satisfied and the postconditions are not, the bug is in the function. If your pre- and postconditions are clear, they can help with debugging.

## Glossary

**interface design:**
A process for designing the interface of a function, which includes the parameters it should take.

**encapsulation:**
The process of transforming a sequence of statements into a function definition.

**generalization:**
The process of replacing something unnecessarily specific (like a number) with something appropriately general (like a variable or parameter).

**refactoring:**
The process of modifying a working program to improve function interfaces and other qualities of the code.

**development plan:**
A process for writing programs.

**docstring:**
A comment that appears at the top of a function definition to document the function's interface.

**precondition:**
A requirement that should be satisfied by the caller before a function starts.

**postcondition:**
A requirement that should be satisfied by the function before it ends.

## Exercises

### Exercise

Write a function called `rectangle` that draws a filled rectangle with given width and height using a specified character. For example, `rectangle("*", 8, 4)` should produce:

```
********
********
********
********
```

### Exercise

Write a function called `rhombus` that draws a rhombus (diamond shape) with a given size. For example, `rhombus("*", 3)` should produce:

```
  *
 ***
*****
 ***
  *
```

### Exercise

Write a more general function called `parallelogram` that draws a filled parallelogram with given width, height, and offset. Then rewrite `rectangle` to use `parallelogram` with an offset of `0`.

### Exercise

Write a function called `triangle` that draws an isosceles triangle with a given height using a specified character. For example, `triangle("*", 5)` should produce:

```
    *
   ***
  *****
 *******
*********
```
