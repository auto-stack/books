# 更多特性

到目前为止，我们已经涵盖了 Auto 中大部分常用特性。在本章中，我们将介绍更多特性，使我们对 Auto 的了解更加全面。

由于 Auto 转译为 Python，我们还会突出介绍 Python 中可用但在 Auto 中工作方式不同（或不可用）的特性。这些部分用"Python 程序员注意"提示框标记。

## 元组解包

你是否曾希望从函数中返回两个不同的值？在 Auto 中，你可以使用元组来实现。元组是一组值的序列，你可以将它们"解包"为单独的变量。

将此程序保存为 `tuple_swap.auto`：

<Listing number="15-1" file-name="tuple_swap.auto" caption="元组解包和交换">

```auto
fn main() {
    let a = 5
    let b = 8
    print(f"Before: a=$a, b=$b")

    // 使用临时变量交换
    let temp = a
    a = b
    b = temp
    print(f"After: a=$a, b=$b")

    // 元组解构
    let (x, y) = (10, 20)
    print(f"x=$x, y=$y")

    // 从函数返回多个值
    let (error_num, error_msg) = get_error_details()
    print(f"Error $error_num: $error_msg")
}

fn get_error_details() -> (int, str) {
    (2, "details")
}
```

```python
def main():
    a = 5
    b = 8
    print(f"Before: a={a}, b={b}")

    # 使用临时变量交换
    temp = a
    a = b
    b = temp
    print(f"After: a={a}, b={b}")

    # 元组解构
    x, y = (10, 20)
    print(f"x={x}, y={y}")

    # 从函数返回多个值
    error_num, error_msg = get_error_details()
    print(f"Error {error_num}: {error_msg}")


def get_error_details():
    return (2, "details")


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ auto run tuple_swap.auto
Before: a=5, b=8
After: a=8, b=5
x=10, y=20
Error 2: details
```

**工作原理**

`get_error_details` 函数返回一个元组 `(2, "details")`。然后我们可以使用 `let (error_num, error_msg) = ...` 语法将这个元组解包为单独的变量。这被称为*元组解构*。

注意 Auto 使用 `let` 声明变量，所以我们不能用 `let` 简单地重新赋值 `a` 和 `b`。相反，我们使用临时变量来交换值。在 Auto 中，一旦变量用 `let` 声明，就可以在不需要 `let` 的情况下重新赋值。

> **Python 程序员注意：**
>
> 在 Python 中，交换两个变量最快的方法是 `a, b = b, a`，这利用了元组打包和解包在单条语句中完成。Auto 不支持这种简写语法，因此你必须使用临时变量来交换。

## 特殊方法

Auto 类型中有一些方法具有特殊含义，如 `init` 和 `drop`。Python 使用"双下划线"方法（如 `__init__` 和 `__str__`）来自定义类的行为。Auto 采用了不同的方式，使用更具可读性的命名方法。

将此程序保存为 `special_methods.auto`：

<Listing number="15-2" file-name="special_methods.auto" caption="特殊方法（toString/compare）">

```auto
type Student {
    name: str
    age: int

    fn init(&self, name: str, age: int) {
        .name = name
        .age = age
    }

    fn to_string(&self) -> str {
        f"Student($.name, $.age)"
    }
}

fn main() {
    let s1 = Student{"Alice", 20}
    let s2 = Student{"Bob", 22}

    print(s1.to_string())
    print(s2.to_string())
}
```

```python
class Student:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __str__(self) -> str:
        return f"Student({self.name}, {self.age})"

    def __lt__(self, other: "Student") -> bool:
        return self.age < other.age


def main():
    s1 = Student("Alice", 20)
    s2 = Student("Bob", 22)

    print(s1)
    print(s2)


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ auto run special_methods.auto
Student(Alice, 20)
Student(Bob, 22)
```

**工作原理**

在 Auto 中，我们在 `Student` 类型上定义了 `to_string` 方法，以提供人类可读的字符串表示。这需要通过 `.to_string()` 显式调用。

在 Python 中，`__str__` 方法会被 `print()` 和 `str()` 自动调用。Python 还支持许多其他特殊方法，如 `__lt__`（用于 `<` 运算符）、`__getitem__`（用于索引）和 `__len__`（用于 `len()` 函数）。

> **Python 程序员注意：**
>
> Python 使用"双下划线"方法（`__str__`、`__lt__`、`__getitem__`、`__len__` 等）来自定义类的行为。Auto 不使用双下划线方法。取而代之的是：
> - `__init__` 变为 `fn init(&self, ...)`
> - `__str__` 变为 `fn to_string(&self) -> str`（需要显式调用）
> - `__lt__` 和其他比较运算符在 Auto 中不支持作为方法重载
> - `__getitem__` 和 `__len__` 在 Auto 中不支持作为方法重载
>
> Auto 的方法优先使用显式方法调用而非运算符重载，使代码更易于阅读和理解。

## Lambda 函数

Python 中的 *lambda* 是一种创建小型匿名函数对象的方式。Lambda 接收一个参数后跟一个表达式，该表达式成为函数体。

Auto **没有** lambda 表达式。相反，Auto 鼓励你使用命名函数，这样更具可读性且更容易调试。

将此程序保存为 `lambda.auto`：

<Listing number="15-3" file-name="lambda.auto" caption="命名函数 vs Python lambda">

```auto
fn sort_by_y(points: list) -> list {
    // Auto 使用命名函数代替 lambda
    fn compare_y(a: dict, b: dict) -> bool {
        a["y"] < b["y"]
    }

    let mut result = points
    result.sort(key = fn(item) { item["y"] })
    return result
}

fn main() {
    let points = [{"x": 2, "y": 3}, {"x": 4, "y": 1}]
    let sorted = sort_by_y(points)
    print(sorted)
}
```

```python
def sort_by_y(points):
    # Python 可以使用 lambda 来编写简洁的单行表达式
    points.sort(key=lambda i: i["y"])
    return points


def main():
    points = [{"x": 2, "y": 3}, {"x": 4, "y": 1}]
    sorted_points = sort_by_y(points)
    print(sorted_points)


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ auto run lambda.auto
[{'y': 1, 'x': 4}, {'y': 3, 'x': 2}]
```

**工作原理**

在 Python 版本中，我们使用 `lambda i: i["y"]` 创建一个匿名函数，从每个字典中提取 `"y"` 值。这个 lambda 被作为 `key` 参数传递给 `sort` 方法。

在 Auto 版本中，我们使用内联匿名函数表达式 `fn(item) { item["y"] }` 代替。虽然这比 Python 的 lambda 稍微冗长一些，但更加明确和可读。当逻辑更复杂时，Auto 也可以定义命名辅助函数（如示例中的 `compare_y`）。

> **Python 程序员注意：**
>
> Python 的 `lambda` 创建仅限于单个表达式的匿名函数。Auto 使用 `fn(params) { body }` 表示匿名函数表达式，支持多条语句。对于简单的情况，Auto 也支持直接传递命名函数引用。

## 列表推导式

列表推导式是 Python 的一个特性，用于从现有列表派生新列表。它们提供了一种简洁的方式来在单个表达式中应用转换和过滤。

Auto **没有**列表推导式。相反，Auto 使用标准的 `for` 循环，这种方式更加明确，也更容易阅读，特别是对于复杂的转换。

将此程序保存为 `list_comp.auto`：

<Listing number="15-4" file-name="list_comp.auto" caption="for 循环 vs Python 列表推导式">

```auto
fn main() {
    let list_one = [2, 3, 4]

    // Auto 使用 for 循环代替列表推导式
    let mut list_two: list = []
    for item in list_one {
        if item > 2 {
            list_two.append(2 * item)
        }
    }
    print(list_two)
}
```

```python
def main():
    list_one = [2, 3, 4]

    # Python 列表推导式：简洁且富有表现力
    list_two = [2 * i for i in list_one if i > 2]
    print(list_two)


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ auto run list_comp.auto
[6, 8]
```

**工作原理**

Python 版本使用列表推导式 `[2 * i for i in list_one if i > 2]` 来创建新列表。这个单行表达式读作："对于 list_one 中的每个元素，如果该元素大于 2，将其乘以 2 并添加到新列表中。"

Auto 版本使用 `for` 循环实现相同的结果。我们声明一个空列表 `list_two`，遍历 `list_one`，用 `if` 语句检查条件，并追加转换后的值。虽然这需要更多的代码行，但每一步都清晰明确。

> **Python 程序员注意：**
>
> Python 列表推导式如 `[expr for x in iterable if condition]` 在 Auto 中没有直接等价物。请使用 `for` 循环配合 `if` 条件和 `.append()` 来代替。虽然稍微冗长一些，但 Auto 的方法同样高效，对初学者来说可能更容易阅读。

## 装饰器

Python 中的装饰器是应用包装函数的快捷方式。它们使用 `@decorator_name` 语法来"包装"函数，添加额外行为，如日志记录、重试或访问控制。

Auto **没有** `@decorator` 语法。相反，Auto 通过显式函数组合来实现相同的效果——你只需调用包装函数并将原始函数作为参数传递。

将此程序保存为 `decorator.auto`：

<Listing number="15-5" file-name="decorator.auto" caption="函数组合 vs Python 装饰器">

```auto
use logging

fn main() {
    // Auto: 显式函数组合
    let safe_save = with_retry(save_to_database)

    safe_save("hello")
}

fn with_retry(fn_to_wrap: fn) -> fn {
    fn(arg: str) {
        let max_attempts = 3
        for attempt in 1..=max_attempts {
            fn_to_wrap(arg)
        }
    }
}

fn save_to_database(arg: str) {
    print(f"Saving: $arg")
}
```

```python
import logging

logging.basicConfig()


def retry(f):
    def wrapper_function(*args, **kwargs):
        MAX_ATTEMPTS = 5
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                return f(*args, **kwargs)
            except Exception:
                logging.exception(
                    "Attempt %s/%s failed : %s",
                    attempt,
                    MAX_ATTEMPTS,
                    (args, kwargs),
                )
        logging.critical(
            "All %s attempts failed : %s", MAX_ATTEMPTS, (args, kwargs)
        )

    return wrapper_function


counter = 0


@retry
def save_to_database(arg):
    print("Write to a database or make a network call or etc.")
    print("This will be automatically retried if exception is thrown.")
    global counter
    counter += 1
    if counter < 2:
        raise ValueError(arg)


if __name__ == "__main__":
    save_to_database("Some bad value")
```

</Listing>

输出：

```
$ auto run decorator.auto
Saving: hello
Saving: hello
Saving: hello
```

**工作原理**

在 Python 版本中，`@retry` 装饰器包装了 `save_to_database` 函数。当调用 `save_to_database` 时，`retry` 包装器会拦截调用，如果抛出异常，则重试最多 5 次，每次之间有递增的延迟。

在 Auto 版本中，我们通过显式调用 `with_retry(save_to_database)` 来实现相同的模式，该调用返回一个新函数 `safe_save`。这个新函数用重试逻辑包装了原始函数。结果在功能上是等价的，只是更加显式。

> **Python 程序员注意：**
>
> Python 的 `@decorator` 语法是 `function = decorator(function)` 的语法糖。Auto 不支持这种语法。要在 Auto 中实现相同的效果，请显式调用包装函数：`let wrapped = wrapper(original_fn)`。高阶函数（接受或返回其他函数的函数）的概念在两种语言中是相同的。

## `assert` 语句

`assert` 语句用于断言某件事为真。例如，如果你非常确定你正在使用的列表中至少有一个元素，并想检查这一点，那么 `assert` 语句非常合适。当 assert 语句失败时，会引发 `AssertionError`。

由于 Auto 转译为 Python，`assert` 语句在两种语言中的工作方式完全相同。

```
>>> let mylist = ["item"]
>>> assert mylist.len() >= 1
>>> mylist.pop()
'item'
>>> assert mylist.len() >= 1
Traceback (most recent call last):
  ...
AssertionError
```

`assert` 语句应谨慎使用。大多数情况下，最好捕获异常，要么处理问题，要么向用户显示错误消息然后退出。

> **Python 程序员注意：**
>
> `assert` 语句在 Auto 和 Python 中的工作方式相同。Auto 使用 `mylist.len()` 代替 Python 的 `len(mylist)`，而 `mylist.pop()` 在两种语言中都是方法调用。

## 小结

我们在本章中涵盖了更多特性：

- **元组解包** -- 从函数返回和解构多个值
- **特殊方法** -- Auto 的命名方法（`init`、`to_string`）与 Python 的双下划线方法（`__init__`、`__str__`）的区别
- **Lambda 函数** -- Auto 使用命名函数或内联 `fn` 表达式代替 Python 的 `lambda`
- **列表推导式** -- Auto 使用 `for` 循环代替 Python 的简洁列表推导式语法
- **装饰器** -- Auto 使用显式函数组合代替 Python 的 `@decorator` 语法
- **`assert` 语句** -- 在 Auto 和 Python 中的工作方式相同

虽然 Auto 不支持 Python 的一些高级语法糖，但它提供了清晰、可读的替代方案来实现相同的结果。这种权衡是用稍微冗长的代码换取更大的清晰度和一致性。
