# Python 附加特性

前面的章节介绍了 Python 的核心特性（以 Auto 语言表达）。但 Python 还有很多有用且值得了解的附加特性。本章介绍其中的一部分。

## 集合

**集合**（set）是一个无序且不包含重复元素的集合。Auto 通过标准库提供 `HashSet`。

<Listing number="18-1" file-name="hashset.auto" caption="创建和使用 HashSet">

```auto
use std::collections::HashSet

fn main() {
    // 从列表创建 HashSet
    let languages: HashSet<str> = ["Python", "Auto", "Java", "C++", "Python"]
    print(languages)
    // {"Python", "Auto", "Java", "C++"}

    // 添加元素
    languages.add("Rust")
    print(languages)
    // {"Python", "Auto", "Java", "C++", "Rust"}

    // 检查成员
    print("Auto" in languages)   // true
    print("Go" in languages)     // false

    // 删除元素
    languages.remove("C++")
    print(languages)
    // {"Python", "Auto", "Java", "Rust"}

    // 集合大小
    print(languages.len())       // 4

    // 集合运算
    let a: HashSet<int> = [1, 2, 3, 4]
    let b: HashSet<int> = [3, 4, 5, 6]

    // 并集
    print(a | b)   // {1, 2, 3, 4, 5, 6}

    // 交集
    print(a & b)   // {3, 4}

    // 差集
    print(a - b)   // {1, 2}

    // 对称差集
    print(a ^ b)   // {1, 2, 5, 6}
}
```

```python
from __future__ import annotations

def main():
    # 从列表创建集合
    languages = {"Python", "Auto", "Java", "C++", "Python"}
    print(languages)
    # {"Python", "Auto", "Java", "C++"}

    # 添加元素
    languages.add("Rust")
    print(languages)
    # {"Python", "Auto", "Java", "C++", "Rust"}

    # 检查成员
    print("Auto" in languages)   # True
    print("Go" in languages)     # False

    # 删除元素
    languages.remove("C++")
    print(languages)
    # {"Python", "Auto", "Java", "Rust"}

    # 集合大小
    print(len(languages))        # 4

    # 集合运算
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}

    # 并集
    print(a | b)   # {1, 2, 3, 4, 5, 6}

    # 交集
    print(a & b)   # {3, 4}

    # 差集
    print(a - b)   # {1, 2}

    # 对称差集
    print(a ^ b)   # {1, 2, 5, 6}


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

在 Auto 中，`HashSet` 从 `std::collections` 导入。你可以从列表字面量创建 `HashSet` —— 重复值会自动被去除。`add` 和 `remove` 方法原地修改集合。集合运算如并集（`|`）、交集（`&`）、差集（`-`）和对称差集（`^`）在 Auto 和 Python 中的使用方式完全相同。

> **Python 程序员注意：**
>
> Auto 使用带显式类型参数的 `HashSet<str>`，而 Python 使用内置的 `set` 类型。Auto 的 `HashSet` 需要从 `std::collections` 导入，但操作方式完全相同。

集合对于去除集合中的重复元素和高效检查成员关系非常有用。集合的 `in` 操作符通常比列表更快，因为集合内部使用哈希表实现。

## 计数器和 defaultdict

Python 的 `collections` 模块提供了 `Counter` 和 `defaultdict`，它们是字典的便捷封装。在 Auto 中，你可以使用普通字典和辅助函数达到相同的效果。

<Listing number="18-2" file-name="list_comprehensions.auto" caption="列表推导和计数模式">

```auto
fn main() {
    // 列表推导的等价写法：Auto 使用 for 循环
    let squares: [int] = []
    for i in 0..10 {
        squares.append(i * i)
    }
    print(squares)
    // [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

    // Python 列表推导：[i * i for i in range(10)]

    // 带过滤的 for 循环
    let even_squares: [int] = []
    for i in 0..10 {
        if i % 2 == 0 {
            even_squares.append(i * i)
        }
    }
    print(even_squares)
    // [0, 4, 16, 36, 64]

    // Python: [i * i for i in range(10) if i % 2 == 0]

    // 计数器模式：统计词频
    let words = ["the", "cat", "in", "the", "hat", "in", "the"]
    let mut counts: HashMap<str, int> = {}
    for word in words {
        counts[word] = counts.get(word, 0) + 1
    }
    print(counts)
    // {"the": 3, "cat": 1, "in": 2, "hat": 1}

    // Python: Counter(words)

    // 找出最常见的
    let mut max_word = ""
    let mut max_count = 0
    for (word, count) in counts {
        if count > max_count {
            max_word = word
            max_count = count
        }
    }
    print(f"Most common: '{max_word}' appears {max_count} times")
    // Most common: 'the' appears 3 times

    // 用字典分组（defaultdict 模式）
    let letters = "abracadabra"
    let mut positions: HashMap<str, [int]> = {}
    for (i, letter) in enumerate(letters) {
        if letter not in positions {
            positions[letter] = []
        }
        positions[letter].append(i)
    }
    print(positions)
    // {"a": [0, 3, 5, 7, 10], "b": [1, 8], "r": [2, 9], "c": [4], "d": [6]}
}
```

```python
def main():
    # 列表推导的等价写法：Auto 使用 for 循环
    squares = []
    for i in range(10):
        squares.append(i * i)
    print(squares)
    # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

    # 带过滤的 for 循环
    even_squares = []
    for i in range(10):
        if i % 2 == 0:
            even_squares.append(i * i)
    print(even_squares)
    # [0, 4, 16, 36, 64]

    # 计数器模式：统计词频
    words = ["the", "cat", "in", "the", "hat", "in", "the"]
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    print(counts)
    # {"the": 3, "cat": 1, "in": 2, "hat": 1}

    # 找出最常见的
    max_word = ""
    max_count = 0
    for word, count in counts.items():
        if count > max_count:
            max_word = word
            max_count = count
    print(f"Most common: '{max_word}' appears {max_count} times")
    # Most common: 'the' appears 3 times

    # 用字典分组（defaultdict 模式）
    letters = "abracadabra"
    positions = {}
    for i, letter in enumerate(letters):
        if letter not in positions:
            positions[letter] = []
        positions[letter].append(i)
    print(positions)
    # {"a": [0, 3, 5, 7, 10], "b": [1, 8], "r": [2, 9], "c": [4], "d": [6]}


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

Auto 没有列表推导式。取而代之的是使用显式的 `for` 循环配合 `append`。`a2p` 转译器生成的 Python 代码也使用 `for` 循环而非推导式，有些人可能觉得这样更易读。

对于计数，Auto 使用 `HashMap.get(key, default)` 模式，而非 Python 的 `Counter`。对于分组（`defaultdict` 模式），你需要先检查键是否存在，如果不存在则初始化。

> **Python 程序员注意：**
>
> Auto 显式使用 `HashMap` 而非 Python 的 `dict`。`a2p` 转译器将 Auto 的 `HashMap<K, V>` 转换为 Python 的 `dict`。虽然 Python 有 `Counter` 和 `defaultdict` 作为便捷工具，但 Auto 只需要多写几行显式代码就能达到相同效果。

## 条件表达式

Python 有**条件表达式**（也称为"三元运算符"），允许你在单个表达式中编写 `if`/`else`。Auto 支持相同的模式。

```auto
let x = 5
let label = if x < 10 { "low" } else { "high" }
print(label)  // low
```

Python 中的等价写法：

```python
x = 5
label = "low" if x < 10 else "high"
print(label)  # low
```

条件表达式通常比 `if` 语句更短，但不一定更容易阅读。当逻辑简单且表达式较短时，使用条件表达式比较合适。

## 命名元组

**命名元组**（named tuple）是一种每个元素都有名称的元组。当你想要一个带有命名属性的简单对象，但不需要类的完整功能时，命名元组非常有用。

在 Auto 中，你可以通过 `type` 定义来达到相同的效果，这更加明确并提供了相同的好处。

<Listing number="18-3" file-name="named_tuples.auto" caption="使用 Auto type 定义实现命名元组">

```auto
type Point {
    x: float,
    y: float,
}

fn main() {
    // 创建 Point（等价于命名元组）
    let p = Point(3.0, 4.0)
    print(p.x)  // 3.0
    print(p.y)  // 4.0

    // Point 可以通过字段进行比较
    let p2 = Point(1.0, 2.0)
    let p3 = Point(3.0, 4.0)
    print(p == p3)  // true
    print(p == p2)  // false

    // 你也可以转换为元组进行解包
    let (a, b) = (p.x, p.y)
    print(f"Unpacked: a={a}, b={b}")  // Unpacked: a=3.0, b=4.0

    // 计算距离
    let distance = (p.x ** 2 + p.y ** 2) ** 0.5
    print(f"Distance from origin: {distance}")  // Distance from origin: 5.0

    // 用作字典键（通过元组转换）
    let mut grid: HashMap<(float, float), str> = {}
    grid[(1.0, 2.0)] = "A"
    grid[(3.0, 4.0)] = "B"
    print(grid)  // {(1.0, 2.0): "A", (3.0, 4.0): "B"}

    // 更复杂的命名元组：表示日期
    type Date {
        year: int,
        month: int,
        day: int,
    }

    let birthday = Date(2000, 1, 15)
    print(f"Year: {birthday.year}, Month: {birthday.month}, Day: {birthday.day}")
    // Year: 2000, Month: 1, Day: 15

    // 比较日期（字典序比较）
    let today = Date(2025, 4, 15)
    print(today > birthday)  // true
}
```

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __gt__(self, other):
        if self.year != other.year:
            return self.year > other.year
        if self.month != other.month:
            return self.month > other.month
        return self.day > other.day


def main():
    p = Point(3.0, 4.0)
    print(p.x)  # 3.0
    print(p.y)  # 4.0

    p2 = Point(1.0, 2.0)
    p3 = Point(3.0, 4.0)
    print(p == p3)  # True
    print(p == p2)  # False

    a, b = p.x, p.y
    print(f"Unpacked: a={a}, b={b}")  # Unpacked: a=3.0, b=4.0

    distance = (p.x ** 2 + p.y ** 2) ** 0.5
    print(f"Distance from origin: {distance}")  # Distance from origin: 5.0

    grid = {}
    grid[(1.0, 2.0)] = "A"
    grid[(3.0, 4.0)] = "B"
    print(grid)  # {(1.0, 2.0): "A", (3.0, 4.0): "B"}

    birthday = Date(2000, 1, 15)
    print(f"Year: {birthday.year}, Month: {birthday.month}, Day: {birthday.day}")
    # Year: 2000, Month: 1, Day: 15

    today = Date(2025, 4, 15)
    print(today > birthday)  # True


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

在 Auto 中，`type` 定义起到与 Python 的 `namedtuple` 相同的作用。两者都提供带有命名属性的对象。Auto 的 `type` 更加灵活 —— 你可以添加方法、使用默认值，以及定义自定义行为。

`a2p` 转译器将 Auto 的 `type` 定义转换为 Python 类，并根据需要生成 `__init__`、`__eq__` 和比较方法。

> **Python 程序员注意：**
>
> Python 的 `namedtuple` 是轻量级且不可变的。Auto 的 `type` 也是轻量级的，但默认是可变的。如果你想要不可变性，请对字段使用 `let`。`a2p` 转译器生成的是 Python 类而非 `namedtuple` 实例，这让你对行为有更多控制。

## any 和 all

Python 提供了内置函数 `any` 和 `all`，它们接受一个可迭代的布尔值序列并返回单个布尔结果。

- `any` 如果**至少有一个**元素为真，则返回 `true`。
- `all` 如果**所有**元素都为真，则返回 `true`。

在 Auto 中，你可以从标准库使用这些函数，或者用循环自行实现逻辑。

<Listing number="18-4" file-name="conditional_expressions.auto" caption="条件表达式、any 和 all">

```auto
fn main() {
    // 条件表达式（三元运算符）
    let age = 20
    let category = if age < 13 { "child" } else if age < 18 { "teenager" } else { "adult" }
    print(f"Age {age}: {category}")  // Age 20: adult

    let score = 85
    let grade = if score >= 90 { "A" } else if score >= 80 { "B" } else if score >= 70 { "C" } else if score >= 60 { "D" } else { "F" }
    print(f"Score {score}: Grade {grade}")  // Score 85: Grade B

    // any：至少有一个元素为真
    let numbers = [0, 0, 0, 1, 0]
    print(any(numbers))   // true

    let empty: [int] = []
    print(any(empty))     // false

    let all_zeros = [0, 0, 0]
    print(any(all_zeros)) // false

    // all：所有元素都为真
    let positives = [1, 2, 3, 4]
    print(all(positives))  // true

    let mixed = [1, 2, 0, 4]
    print(all(mixed))      // false

    // 实际示例：检查所有字符串是否非空
    let words = ["hello", "world", "auto"]
    let mut all_nonempty = true
    for word in words {
        if word.len() == 0 {
            all_nonempty = false
            break
        }
    }
    print(all_nonempty)  // true

    // 实际示例：检查是否有任何字符串包含数字
    let inputs = ["hello", "test123", "world"]
    let mut has_digit = false
    for s in inputs {
        for c in s {
            if c.isdigit() {
                has_digit = true
                break
            }
        }
        if has_digit {
            break
        }
    }
    print(has_digit)  // true

    // 组合条件表达式与 any/all
    let scores = [65, 72, 88, 91, 45]
    let passing = [s for s in scores if s >= 60]  // Auto 使用 for 循环
    // Python: passing = [s for s in scores if s >= 60]

    let mut filtered: [int] = []
    for s in scores {
        if s >= 60 {
            filtered.append(s)
        }
    }
    print(filtered)     // [65, 72, 88, 91]
    print(all(filtered)) // true（全部 >= 60）

    // 使用 any 的类生成器模式
    let mut any_failing = false
    for s in scores {
        if s < 60 {
            any_failing = true
            break
        }
    }
    print(any_failing)  // true
}
```

```python
def main():
    # 条件表达式（三元运算符）
    age = 20
    category = "child" if age < 13 else ("teenager" if age < 18 else "adult")
    print(f"Age {age}: {category}")  # Age 20: adult

    score = 85
    grade = ("A" if score >= 90 else ("B" if score >= 80 else ("C" if score >= 70 else ("D" if score >= 60 else "F"))))
    print(f"Score {score}: Grade {grade}")  # Score 85: Grade B

    # any：至少有一个元素为真
    numbers = [0, 0, 0, 1, 0]
    print(any(numbers))   # True

    empty = []
    print(any(empty))     # False

    all_zeros = [0, 0, 0]
    print(any(all_zeros)) # False

    # all：所有元素都为真
    positives = [1, 2, 3, 4]
    print(all(positives))  # True

    mixed = [1, 2, 0, 4]
    print(all(mixed))      # False

    # 实际示例：检查所有字符串是否非空
    words = ["hello", "world", "auto"]
    all_nonempty = True
    for word in words:
        if len(word) == 0:
            all_nonempty = False
            break
    print(all_nonempty)  # True

    # 实际示例：检查是否有任何字符串包含数字
    inputs = ["hello", "test123", "world"]
    has_digit = False
    for s in inputs:
        for c in s:
            if c.isdigit():
                has_digit = True
                break
        if has_digit:
            break
    print(has_digit)  # True

    # 组合条件表达式与 any/all
    scores = [65, 72, 88, 91, 45]

    filtered = []
    for s in scores:
        if s >= 60:
            filtered.append(s)
    print(filtered)     # [65, 72, 88, 91]
    print(all(filtered)) # True（全部 >= 60）

    # 使用 any 的类生成器模式
    any_failing = False
    for s in scores:
        if s < 60:
            any_failing = True
            break
    print(any_failing)  # True


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

Auto 的条件表达式语法是 `if condition { value1 } else { value2 }`，类似于 Python 的 `value1 if condition else value2`，但条件放在前面（像 `if` 语句一样）。对于链式条件，Auto 自然地嵌套表达式。

`any` 和 `all` 函数在 Auto 和 Python 中的工作方式相同。它们接受一个可迭代对象并返回一个布尔值。在 Auto 中，当需要提前终止（如 `break`）时，你使用显式循环而非生成器表达式。

> **Python 程序员注意：**
>
> Python 的条件表达式将值放在前面：`x if condition else y`。Auto 将条件放在前面：`if condition { x } else { y }`。Python 的生成器表达式（如 `any(x > 0 for x in numbers)`）没有直接的 Auto 等价写法 —— 请使用显式循环。

## 调试

当你使用集合、字典和其他集合类型时，有一些常见的错误来源：

**可变默认参数：** 在 Python 中，使用可变对象（如列表或字典）作为默认参数可能会导致意外行为，因为同一个对象在所有调用之间共享。在 Auto 中，默认值每次都会重新求值，因此这不是问题。

**集合/字典键类型：** 只有不可变类型才能用作字典的键或集合的元素。在 Python 中，这意味着字符串、数字和由不可变对象组成的元组。Auto 遵循相同的规则 —— 你不能将列表用作字典的键。

**迭代时修改：** 在迭代集合时修改它可能会导致错误或意外行为。如果你需要在迭代期间修改集合，请迭代一个副本。

```auto
// 错误：在迭代时修改列表
let mut items = [1, 2, 3, 4, 5]
for item in items {
    if item == 3 {
        items.remove(item)  // 未定义行为！
    }
}

// 正确：收集要删除的元素，然后删除它们
let mut items = [1, 2, 3, 4, 5]
let mut to_remove: [int] = []
for item in items {
    if item == 3 {
        to_remove.append(item)
    }
}
for item in to_remove {
    items.remove(item)
}
```

## 术语表

**集合（set）：**
一个无序的唯一元素集合。在 Auto 中由 `HashSet` 表示。

**HashSet：**
Auto 的集合类型，从 `std::collections` 导入。

**集合运算：**
如并集（`|`）、交集（`&`）、差集（`-`）和对称差集（`^`）等组合集合的运算。

**计数器（Counter）：**
一个将元素映射到其出现次数的字典。在 Python 中由 `collections.Counter` 提供。在 Auto 中使用普通的 `HashMap` 实现。

**defaultdict：**
一个为缺失键提供默认值的字典。在 Python 中由 `collections.defaultdict` 提供。在 Auto 中通过显式键检查实现。

**列表推导式（list comprehension）：**
一种 Python 表达式，通过对可迭代对象的每个元素应用表达式来创建列表，可选择按条件过滤。Auto 使用显式的 `for` 循环代替。

**条件表达式（conditional expression）：**
根据布尔条件返回两个值之一表达式。也称为"三元运算符"。

**命名元组（named tuple）：**
每个元素都有名称的元组。在 Auto 中通过 `type` 定义实现。

**any：**
如果可迭代对象中至少有一个元素为真则返回 `true` 的函数。

**all：**
如果可迭代对象中所有元素都为真则返回 `true` 的函数。

## 练习

### 练习 1

编写一个名为 `has_duplicates` 的函数，接受一个列表，如果任何元素出现超过一次则返回 `true`。它不应修改原始列表。

### 练习 2

编写一个名为 `word_frequency` 的函数，接受一个字符串，返回一个将每个单词映射到其出现次数的字典。在计数前将字符串转换为小写并去除标点。

### 练习 3

编写一个名为 `unique_words` 的函数，接受一个单词列表，返回按字母顺序排列的唯一单词列表，使用 `HashSet`。

### 练习 4

Python 的 `dict` 有一个名为 `setdefault` 的方法，仅在键不存在时才设置字典中的值。在 Auto 中的等价写法是：

```auto
let mut d: HashMap<str, [int]> = {}
// 代替 d.setdefault(key, []).append(value):
if key not in d {
    d[key] = []
}
d[key].append(value)
```

使用此模式编写一个名为 `invert_dict` 的函数，接受一个字典并返回一个键值互换的新字典。如果原始字典有重复的值，反转后的字典应将每个值映射到一个键的列表。
