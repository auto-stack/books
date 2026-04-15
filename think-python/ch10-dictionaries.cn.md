# 字典

本章介绍一种叫做字典的内置类型（在 Auto 中称为 `HashMap`，在 Python 中称为 `dict`）。这是两种语言中最出色的特性之一 -- 也是许多高效且优雅算法的构建基础。

我们将使用字典来计算一本书中不重复单词的数量以及每个单词出现的次数。在练习中，我们将使用字典来解决单词谜题。

## 字典是一种映射

**字典**（dictionary）类似于列表，但更加通用。在列表中，索引必须是整数；在字典中，索引可以是（几乎）任何类型。例如，假设我们创建一个数字单词的列表：

```auto
let lst = ["zero", "one", "two"]
```

我们可以使用整数作为索引来获取对应的单词。

```auto
print(lst[1])  // "one"
```

但如果我们想反过来，通过单词查找对应的整数，就不能用列表了，但可以用字典。我们先创建一个空字典并将其赋值给 `numbers`。

```auto
let mut numbers: HashMap<str, int> = {}
```

在 Auto 中，字典使用 `HashMap` 类型创建，它将一种类型的键映射到另一种类型的值。`{}` 语法创建一个空字典。

要向字典中添加项，我们使用方括号。

```auto
numbers["zero"] = 0
```

这个赋值操作向字典添加了一个**项**（item），表示**键**（key）和**值**（value）之间的关联。在这个例子中，键是字符串 `"zero"`，值是整数 `0`。

我们可以这样添加更多项。

```auto
numbers["one"] = 1
numbers["two"] = 2
print(numbers)  // {"zero": 0, "one": 1, "two": 2}
```

要查找键并获取对应的值，我们使用方括号运算符。

```auto
print(numbers["two"])  // 2
```

`len` 函数也适用于字典；它返回项的数量。

```auto
print(len(numbers))  // 3
```

用数学语言来说，字典表示从键到值的**映射**（mapping），所以你也可以说每个键"映射到"一个值。

> **Python 程序员注意：**
>
> Auto 使用 `HashMap<K, V>` 代替 Python 的 `dict`。`a2p` 转译器会自动将 `HashMap` 转换为 `dict`。Auto 使用 `len()` 的方式与 Python 相同。

## 创建字典

在上一节中，我们创建了一个空字典，然后使用方括号运算符一次添加一个项。我们也可以一次性创建字典：

```auto
let numbers: HashMap<str, int> = {"zero": 0, "one": 1, "two": 2}
```

每个项由键和值组成，用冒号分隔。项之间用逗号分隔，整体用花括号括起来。

我们也可以这样复制字典。

```auto
let numbers_copy: HashMap<str, int> = HashMap::copy(numbers)
```

在执行会修改字典的操作之前，通常需要先制作一个副本。

## `in` 运算符

在 Auto 中，`contains_key` 方法检查键是否存在于字典中。在 Python 中，`in` 运算符完成这个功能。

```auto
print(numbers.contains_key("one"))  // true
```

`contains_key` 方法检查某值是否作为*键*出现在字典中。要检查某值是否作为*值*出现，需要遍历所有的值。

字典中的项存储在**哈希表**（hash table）中，这是一种组织数据的方式，具有一个显著的特性：无论字典中有多少项，查找键所需的时间大致相同。这使得编写非常高效的算法成为可能。

> **Python 程序员注意：**
>
> Auto 使用 `d.contains_key("key")` 代替 Python 的 `"key" in d`。`a2p` 转译器会自动转换。Auto 也支持 `d.get("key", default)`，与 Python 用法相同。

<Listing number="10-1" file-name="dict_basics.auto" caption="创建和访问字典">

```auto
fn main() {
    // 创建空字典
    let mut numbers: HashMap<str, int> = {}
    numbers["zero"] = 0
    numbers["one"] = 1
    numbers["two"] = 2
    print("numbers:", numbers)

    // 一次性创建字典
    let scores: HashMap<str, int> = {"Alice": 95, "Bob": 87, "Charlie": 92}
    print("scores:", scores)

    // 访问值
    print("Alice's score:", scores["Alice"])
    print("Length of scores:", len(scores))

    // 检查键是否存在
    print("Contains 'Alice':", scores.contains_key("Alice"))
    print("Contains 'David':", scores.contains_key("David"))

    // 使用 get 方法并提供默认值
    print("Eve's score:", scores.get("Eve", 0))
    print("Bob's score:", scores.get("Bob", 0))
}
```

```python
def main():
    # 创建空字典
    numbers = {}
    numbers["zero"] = 0
    numbers["one"] = 1
    numbers["two"] = 2
    print(f"numbers: {numbers}")

    # 一次性创建字典
    scores = {"Alice": 95, "Bob": 87, "Charlie": 92}
    print(f"scores: {scores}")

    # 访问值
    print(f"Alice's score: {scores['Alice']}")
    print(f"Length of scores: {len(scores)}")

    # 检查键是否存在
    print(f"Contains 'Alice': {'Alice' in scores}")
    print(f"Contains 'David': {'David' in scores}")

    # 使用 get 方法并提供默认值
    print(f"Eve's score: {scores.get('Eve', 0)}")
    print(f"Bob's score: {scores.get('Bob', 0)}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

第一部分演示了逐步创建字典：从空的 `HashMap<str, int>` 开始，使用方括号表示法添加项。第二部分展示了使用初始值一次性创建字面量字典的语法。

访问值使用相同的方括号表示法。`len()` 返回项的数量。`contains_key` 方法（Python：`in` 运算符）检查键是否存在。`get` 方法在键存在时返回对应的值，否则返回默认值 -- 这避免了在查找可能不存在的键时出现错误。

## 计数器集合

假设给你一个字符串，你想计算每个字母出现的次数。字典是完成这项工作的好工具。我们从空字典开始。

```auto
let mut counter: HashMap<str, int> = {}
```

当我们遍历字符串中的字母时，假设第一次看到字母 `'a'`。我们可以这样将它添加到字典中。

```auto
counter["a"] = 1
```

后来，如果再次看到相同的字母，我们可以这样递增计数器。

```auto
counter["a"] += 1
```

下面的函数使用这些特性来计算字符串中每个字母出现的次数。

```auto
fn value_counts(string: str) -> HashMap<str, int> {
    let mut counter: HashMap<str, int> = {}
    for letter in string {
        if !counter.contains_key(letter) {
            counter[letter] = 1
        } else {
            counter[letter] += 1
        }
    }
    return counter
}
```

每次循环时，如果 `letter` 不在字典中，我们创建一个新项，键为 `letter`，值为 `1`。如果 `letter` 已经在字典中，我们递增与 `letter` 关联的值。

例如：

```auto
let counter = value_counts("brontosaurus")
print(counter)  // {"b": 1, "r": 2, "o": 2, "n": 1, "t": 1, "s": 2, "a": 1, "u": 1}
```

## 遍历和字典

如果在 `for` 语句中使用字典，它会遍历字典的键。为了演示，让我们创建一个统计 `"banana"` 中字母的字典。

```auto
let counter = value_counts("banana")
```

下面的循环打印键，即字母。

```auto
for key in counter.keys() {
    print(key)
}
```

要打印值，可以使用 `values` 方法。

```auto
for value in counter.values() {
    print(value)
}
```

要打印键和值，可以遍历键并查找对应的值。

```auto
for key in counter.keys() {
    let value = counter[key]
    print(key, value)
}
```

在下一章中，我们将看到使用元组的更简洁的方式。

<Listing number="10-2" file-name="dict_looping.auto" caption="使用字典遍历和计数">

```auto
fn value_counts(string: str) -> HashMap<str, int> {
    let mut counter: HashMap<str, int> = {}
    for letter in string {
        if !counter.contains_key(letter) {
            counter[letter] = 1
        } else {
            counter[letter] += 1
        }
    }
    return counter
}

fn main() {
    // 统计单词中的字母
    let counter = value_counts("brontosaurus")
    print("Letter counts:", counter)
    print("Number of unique letters:", len(counter))

    // 遍历键
    print("Keys:")
    for key in counter.keys() {
        print(key, end=" ")
    }
    print()

    // 遍历值
    print("Values:")
    for value in counter.values() {
        print(value, end=" ")
    }
    print()

    // 遍历键值对
    print("Key-value pairs:")
    for key in counter.keys() {
        let value = counter[key]
        print(f"$key: $value")
    }

    // 从列表构建字典
    let words = ["apple", "banana", "cherry", "date", "elderberry"]
    let mut word_lengths: HashMap<str, int> = {}
    for word in words {
        word_lengths[word] = len(word)
    }
    print("Word lengths:", word_lengths)
}
```

```python
def value_counts(string):
    counter = {}
    for letter in string:
        if letter not in counter:
            counter[letter] = 1
        else:
            counter[letter] += 1
    return counter


def main():
    # 统计单词中的字母
    counter = value_counts("brontosaurus")
    print(f"Letter counts: {counter}")
    print(f"Number of unique letters: {len(counter)}")

    # 遍历键
    print("Keys:")
    for key in counter:
        print(key, end=" ")
    print()

    # 遍历值
    print("Values:")
    for value in counter.values():
        print(value, end=" ")
    print()

    # 遍历键值对
    print("Key-value pairs:")
    for key in counter:
        value = counter[key]
        print(f"{key}: {value}")

    # 从列表构建字典
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    word_lengths = {}
    for word in words:
        word_lengths[word] = len(word)
    print(f"Word lengths: {word_lengths}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`value_counts` 演示了直方图模式：初始化一个空字典，遍历每个元素，要么创建新条目，要么递增现有条目。这是字典最常见的用途之一。

三种遍历模式展示了遍历字典的不同方式：仅遍历键、仅遍历值、以及键值对（通过键查找每个值）。最后一个示例展示了将累加器模式应用于字典 -- 通过将列表中的每个元素映射到计算值来构建新字典。

## 列表和字典

你可以将列表作为值放入字典中。例如，下面是一个将数字 `4` 映射到四个字母列表的字典。

```auto
let d: HashMap<int, List<str>> = {4: ["r", "o", "u", "s"]}
```

但你不能将列表作为键放入字典中。字典使用哈希表，这意味着键必须是**可哈希的**（hashable）。由于列表是可变的，它们不可哈希，不能用作键。

由于字典是可变的，它们也不能用作键。但它们*可以*用作值。

## 累积列表

对于许多编程任务，遍历一个列表或字典同时构建另一个列表是很有用的。例如，我们将遍历字典中的单词，构建一个回文列表 -- 即正读反读都一样的单词，如 "noon" 和 "rotator"。

```auto
fn is_palindrome(word: str) -> bool {
    return word == word.reversed()
}
```

我们可以使用类似的模式来构建回文列表。

```auto
let mut palindromes: List<str> = []
for word in word_dict.keys() {
    if is_palindrome(word) {
        palindromes.append(word)
    }
}
```

在这个循环中，`palindromes` 用作**累加器**（accumulator），即在计算过程中收集或累积数据的变量。

像这样遍历列表并选择某些元素而省略其他元素的过程称为**过滤**（filtering）。

## 备忘录

如果你运行了第 6 章的 `fibonacci` 函数，可能注意到参数越大，函数运行时间越长，而且运行时间增长很快。

```auto
fn fibonacci(n: int) -> int {
    if n == 0 {
        return 0
    }
    if n == 1 {
        return 1
    }
    return fibonacci(n - 1) + fibonacci(n - 2)
}
```

一种解决方案是将已经计算过的值存储在字典中，以便跟踪。存储以备将来使用的预先计算的值称为**备忘录**（memo）。以下是 `fibonacci` 的"备忘录化"版本：

```auto
let mut known: HashMap<int, int> = {0: 0, 1: 1}

fn fibonacci_memo(n: int) -> int {
    if known.contains_key(n) {
        return known[n]
    }
    let res = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    known[n] = res
    return res
}
```

`known` 是一个字典，跟踪我们已经知道的斐波那契数。它以两个项开始：`0` 映射到 `0`，`1` 映射到 `1`。

每当调用 `fibonacci_memo` 时，它检查 `known`。如果结果已经存在，可以立即返回。否则需要计算新值，将其添加到字典中，然后返回。

比较两个函数，`fibonacci(40)` 大约需要 30 秒运行。`fibonacci_memo(40)` 大约需要 30 微秒，快了一百万倍。

<Listing number="10-3" file-name="dict_memo.auto" caption="使用备忘录优化斐波那契">

```auto
let mut known: HashMap<int, int> = {0: 0, 1: 1}

fn fibonacci_memo(n: int) -> int {
    if known.contains_key(n) {
        return known[n]
    }
    let res = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    known[n] = res
    return res
}

fn main() {
    // 使用备忘录计算斐波那契数
    print("Fibonacci numbers with memoization:")
    for i in 0..=10 {
        print(f"fib($i) = ${fibonacci_memo(i)}")
    }

    // 大的斐波那契数 -- 使用备忘录很快
    print()
    print("fib(40) =", fibonacci_memo(40))

    // 显示缓存中的内容
    print()
    print("Cache contains", len(known), "entries")

    // 演示重用缓存
    print("fib(35) from cache:", known[35])
}
```

```python
known = {0: 0, 1: 1}


def fibonacci_memo(n):
    if n in known:
        return known[n]
    res = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    known[n] = res
    return res


def main():
    # 使用备忘录计算斐波那契数
    print("Fibonacci numbers with memoization:")
    for i in range(11):
        print(f"fib({i}) = {fibonacci_memo(i)}")

    # 大的斐波那契数 -- 使用备忘录很快
    print()
    print(f"fib(40) = {fibonacci_memo(40)}")

    # 显示缓存中的内容
    print()
    print(f"Cache contains {len(known)} entries")

    # 演示重用缓存
    print(f"fib(35) from cache: {known[35]}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

备忘录化是一种强大的优化技术。`known` 字典存储了之前计算过的斐波那契数。在计算 `fibonacci_memo(n)` 之前，函数会检查结果是否已在缓存中。如果在，函数立即返回 -- 不需要递归调用。

没有备忘录化，`fibonacci(40)` 大约进行 3.3 亿次递归调用。有了备忘录化，只需进行 39 次调用（从 2 到 40 各一次）。这就是秒级和微秒级之间的差距。

关键洞察是，字典查找需要恒定时间，无论存储了多少项。因此，与递归计算的成本相比，检查 `known.contains_key(n)` 基本上是免费的。

## 调试

当你处理更大的数据集时，通过打印并手动检查输出来调试会变得很困难。以下是一些调试大数据集的建议：

1. **缩小输入**：如果可能，减小数据集的大小。例如，如果程序读取文本文件，从只有前 10 行开始，或者从你能找到的最小示例开始。如果有错误，可以将大小减小到错误出现时的最小值。随着发现和修正错误，可以逐步增大大小。

2. **检查摘要和类型**：不要打印和检查整个数据集，而是考虑打印数据的摘要 -- 例如字典中的项数或数字列表的总和。运行时错误的一个常见原因是值的类型不正确。

3. **编写自我检查**：有时可以编写代码来自动检查错误。例如，如果你正在计算数字列表的平均值，可以检查结果不大于列表中的最大元素，也不小于最小元素。这称为"健全性检查"（sanity check）。另一种检查是比较两种不同计算的结果，看它们是否一致 -- 称为"一致性检查"（consistency check）。

4. **格式化输出**：格式化调试输出可以使错误更容易被发现。花在搭建脚手架上的时间可以减少调试的时间。

## 术语表

**字典（dictionary）：**
包含键值对的对象，也称为项（item）。在 Auto 中，类型为 `HashMap`；在 Python 中，类型为 `dict`。

**项（item）：**
在字典中，键值对的另一个名称。

**键（key）：**
在字典中作为键值对第一部分出现的对象。

**值（value）：**
在字典中作为键值对第二部分出现的对象。

**映射（mapping）：**
一种关系，其中一个集合中的每个元素对应另一个集合中的一个元素。

**哈希表（hash table）：**
一种键值对的集合，组织方式使得我们可以高效地查找键并找到其值。

**可哈希的（hashable）：**
不可变类型如整数、浮点数和字符串是可哈希的。可变类型如列表和字典不可哈希。

**累加器（accumulator）：**
在循环中用于累加或累积结果的变量。

**过滤（filtering）：**
遍历序列并选择或省略元素。

**调用图（call graph）：**
一个图表，显示程序执行期间创建的每个帧，以及从每个调用者到每个被调用者的箭头。

**备忘录（memo）：**
存储的已计算值，用于避免不必要的未来计算。

## 练习

### 练习

使用 `get` 方法编写一个更简洁的 `value_counts` 版本。你应该能够消除 `if` 语句。

### 练习

编写一个名为 `has_duplicates` 的函数，接受一个序列（如列表或字符串）作为参数，如果序列中有任何元素出现多次则返回 `true`。

### 练习

编写一个名为 `find_repeats` 的函数，接受一个将每个键映射到计数器的字典（如 `value_counts` 的结果）。它应该遍历字典并返回计数大于 `1` 的键的列表。

### 练习

假设你用两个不同的单词运行 `value_counts`，并将结果保存在两个字典中。编写一个名为 `add_counters` 的函数，接受两个这样的字典，并返回一个新字典，包含所有字母及其在任一单词中出现的总次数。

### 练习

如果一个单词可以通过交替取字母分成两个单词，则该单词是"交错词"（interlocking）。例如，"schooled" 是一个交错词，因为它可以分成 "shoe" 和 "cold"。编写一个名为 `is_interlocking` 的函数，接受一个单词作为参数，如果能将其分成两个交错单词则返回 `true`。
