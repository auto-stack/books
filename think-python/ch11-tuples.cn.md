# 元组

本章介绍另一种内置类型 -- 元组（tuple），然后展示列表、字典和元组如何协同工作。本章还将介绍元组赋值以及可变长度参数列表的实用特性。

在练习中，我们将使用元组以及列表和字典来解决更多单词谜题并实现高效算法。

## 元组类似于列表

元组是一个值的序列。值可以是任何类型，通过整数索引，因此元组在很多方面类似于列表。重要的区别在于元组是**不可变的**（immutable）。

要创建元组，可以编写用括号括起来的逗号分隔的值列表。

```auto
let t: Tuple = ('l', 'u', 'p', 'i', 'n')
print(type(t))  // Tuple
```

要创建只有一个元素的元组，必须在末尾加上逗号。

```auto
let t1: Tuple = ('p',)
```

另一种创建元组的方式是使用内置的 `Tuple` 类型。不带参数时创建空元组。如果参数是序列，结果是一个包含序列元素的元组。

```auto
let t: Tuple = Tuple("lupin")
print(t)  // ('l', 'u', 'p', 'i', 'n')
```

大多数列表运算符也适用于元组。例如，方括号运算符索引元素。

```auto
print(t[0])  // 'l'
```

切片运算符选择一个范围的元素。

```auto
print(t[1:3])  // ('u', 'p')
```

`+` 运算符连接元组。

```auto
print(Tuple("lup") + ('i', 'n'))  // ('l', 'u', 'p', 'i', 'n')
```

`sorted` 函数适用于元组 -- 但结果是列表，不是元组。

```auto
let s = sorted(t)
print(s)  // ['i', 'l', 'n', 'p', 'u']
```

> **Python 程序员注意：**
>
> Auto 使用大写的 `Tuple` 代替 Python 的 `tuple`。`a2p` 转译器会自动将 `Tuple` 转换为 `tuple`。

## 元组是不可变的

如果你尝试用方括号运算符修改元组，会得到一个错误。元组没有修改列表的方法，如 `append` 和 `remove`。

由于元组是不可变的，它们是**可哈希的**（hashable），这意味着它们可以用作字典的键。例如，下面的字典包含两个元组作为键，映射到整数。

```auto
let mut d: HashMap<Tuple, int> = {}
d[(1, 2)] = 3
d[(3, 4)] = 7
print(d[(1, 2)])  // 3
```

或者如果我们有一个引用元组的变量，可以将其用作键。

```auto
let t: Tuple = (3, 4)
print(d[t])  // 7
```

元组也可以作为字典中的值出现。

```auto
let d: HashMap<str, Tuple> = {"key": ('a', 'b', 'c')}
print(d)  // {"key": ('a', 'b', 'c')}
```

<Listing number="11-1" file-name="tuple_basics.auto" caption="元组的创建和索引">

```auto
fn main() {
    // 创建元组
    let t: Tuple = ('l', 'u', 'p', 'i', 'n')
    print("Tuple:", t)

    // 从字符串创建元组
    let t2: Tuple = Tuple("hello")
    print("Tuple from string:", t2)

    // 单元素元组
    let single: Tuple = ('p',)
    print("Single element:", single)

    // 索引
    print("First element:", t[0])
    print("Last element:", t[-1])

    // 切片
    print("Slice [1:3]:", t[1:3])

    // 连接
    let combined = Tuple("lup") + ('i', 'n')
    print("Concatenated:", combined)

    // 长度
    print("Length:", len(t))

    // 排序（返回列表）
    print("Sorted:", sorted(t))

    // 元组作为字典键
    let mut d: HashMap<Tuple, int> = {}
    d[(1, 2)] = 3
    d[(3, 4)] = 7
    print("Dict with tuple keys:", d)
    print("d[(1, 2)]:", d[(1, 2)])
}
```

```python
def main():
    # 创建元组
    t = ('l', 'u', 'p', 'i', 'n')
    print(f"Tuple: {t}")

    # 从字符串创建元组
    t2 = tuple("hello")
    print(f"Tuple from string: {t2}")

    # 单元素元组
    single = ('p',)
    print(f"Single element: {single}")

    # 索引
    print(f"First element: {t[0]}")
    print(f"Last element: {t[-1]}")

    # 切片
    print(f"Slice [1:3]: {t[1:3]}")

    # 连接
    combined = tuple("lup") + ('i', 'n')
    print(f"Concatenated: {combined}")

    # 长度
    print(f"Length: {len(t)}")

    # 排序（返回列表）
    print(f"Sorted: {sorted(t)}")

    # 元组作为字典键
    d = {}
    d[(1, 2)] = 3
    d[(3, 4)] = 7
    print(f"Dict with tuple keys: {d}")
    print(f"d[(1, 2)]: {d[(1, 2)]}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

元组用包含逗号分隔值的括号创建。单元素元组需要尾随逗号以区别于带括号的表达式。`Tuple()` 构造函数可以将其他序列（如字符串）转换为元组。

与列表一样，元组支持索引、切片、连接和 `len()`。与列表不同的是，元组是不可变的 -- 不能修改元素、追加或删除。这种不可变性使元组可哈希，因此可以用作字典键，如示例最后一部分所示。

## 元组赋值

你可以将变量元组放在赋值的左侧，将值元组放在右侧。

```auto
let (a, b) = (1, 2)
print(a, b)  // 1 2
```

值从左到右分配给变量。更一般地说，如果赋值的左侧是元组，右侧可以是任何序列 -- 字符串、列表或元组。例如，要将电子邮件地址拆分为用户名和域名：

```auto
let email = "monty@python.org"
let (username, domain) = email.split("@")
print(username)  // "monty"
print(domain)    // "python.org"
```

元组赋值在交换两个变量的值时很有用。

```auto
let mut (a, b) = (1, 2)
let (a, b) = (b, a)
print(a, b)  // 2 1
```

我们也可以在 `for` 语句中使用元组赋值。例如，要遍历字典中的项，可以使用 `items` 方法。

```auto
let d: HashMap<str, int> = {"one": 1, "two": 2}
for (key, value) in d.items() {
    print(f"$key -> $value")
}
```

每次循环时，一个键和对应的值直接赋给 `key` 和 `value`。

## 元组作为返回值

严格来说，函数只能返回一个值，但如果值是元组，效果与返回多个值相同。

内置函数 `divmod` 接受两个参数，返回一个包含商和余数的二元组。

```auto
let result: Tuple = divmod(7, 3)
print(result)  // (2, 1)
```

我们可以使用元组赋值将元组的元素存储在两个变量中。

```auto
let (quotient, remainder) = divmod(7, 3)
print(quotient)   // 2
print(remainder)  // 1
```

以下是一个返回元组的函数示例。

```auto
fn min_max(t: Tuple) -> Tuple {
    return (min(t), max(t))
}
```

`max` 和 `min` 是内置函数，用于查找序列中最大和最小的元素。`min_max` 同时计算两者并返回一个二元组。

<Listing number="11-2" file-name="tuple_assign.auto" caption="元组赋值和返回值">

```auto
fn min_max(t: Tuple) -> Tuple {
    return (min(t), max(t))
}

fn swap(a: int, b: int) -> Tuple {
    return (b, a)
}

fn main() {
    // 元组赋值
    let (x, y) = (10, 20)
    print("x:", x, "y:", y)

    // 用元组赋值拆分字符串
    let email = "monty@python.org"
    let (username, domain) = email.split("@")
    print("Username:", username)
    print("Domain:", domain)

    // 交换变量
    let mut (a, b) = (3, 7)
    print("Before swap: a =", a, "b =", b)
    let (a, b) = swap(a, b)
    print("After swap:  a =", a, "b =", b)

    // divmod -- 返回元组
    let (quotient, remainder) = divmod(17, 5)
    print("17 / 5 =", quotient, "remainder", remainder)

    // 返回元组的函数
    let numbers: Tuple = (4, 1, 7, 2, 9, 3)
    let (low, high) = min_max(numbers)
    print("Numbers:", numbers)
    print("Min:", low, "Max:", high)

    // 用元组赋值遍历字典项
    let scores: HashMap<str, int> = {"Alice": 95, "Bob": 87, "Charlie": 92}
    print("Scores:")
    for (name, score) in scores.items() {
        print(f"  $name: $score")
    }
}
```

```python
def min_max(t):
    return (min(t), max(t))


def swap(a, b):
    return (b, a)


def main():
    # 元组赋值
    x, y = 10, 20
    print(f"x: {x} y: {y}")

    # 用元组赋值拆分字符串
    email = "monty@python.org"
    username, domain = email.split("@")
    print(f"Username: {username}")
    print(f"Domain: {domain}")

    # 交换变量
    a, b = 3, 7
    print(f"Before swap: a = {a} b = {b}")
    a, b = swap(a, b)
    print(f"After swap:  a = {a} b = {b}")

    # divmod -- 返回元组
    quotient, remainder = divmod(17, 5)
    print(f"17 / 5 = {quotient} remainder {remainder}")

    # 返回元组的函数
    numbers = (4, 1, 7, 2, 9, 3)
    low, high = min_max(numbers)
    print(f"Numbers: {numbers}")
    print(f"Min: {low} Max: {high}")

    # 用元组赋值遍历字典项
    scores = {"Alice": 95, "Bob": 87, "Charlie": 92}
    print("Scores:")
    for name, score in scores.items():
        print(f"  {name}: {score}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

元组赋值允许你一次分配多个变量。左侧的变量数量必须与右侧的值数量匹配。这对于返回多个值的函数特别有用，如 `divmod` 或我们自定义的 `min_max`。

`swap` 函数演示了一个常见模式：返回元组并使用元组赋值解包。当遍历 `d.items()` 时，每次迭代产生一个键值对，我们可以直接在 `for` 循环头部解构它。

## Zip

元组对于遍历两个序列的元素并对对应元素执行操作非常有用。例如，假设两支队伍进行七场比赛，我们将他们的比分记录在两个列表中。

```auto
let scores1: List<int> = [1, 2, 4, 5, 1, 5, 2]
let scores2: List<int> = [5, 5, 2, 2, 5, 2, 3]
```

我们将使用 `zip`，这是一个内置函数，接受两个或多个序列并将元素配对。

```auto
let mut wins = 0
for (team1, team2) in zip(scores1, scores2) {
    if team1 > team2 {
        wins += 1
    }
}
print("Team 1 wins:", wins)  // 3
```

如果你有一个键列表和一个值列表，可以使用 `zip` 和 `dict` 来创建字典。

```auto
let letters = "abcdefghijklmnopqrstuvwxyz"
let numbers = 0..len(letters)
let letter_map: HashMap<str, int> = dict(zip(letters, numbers))
print(letter_map["a"])  // 0
print(letter_map["z"])  // 25
```

## 比较和排序

关系运算符适用于元组和其他序列。例如，如果对元组使用 `<` 运算符，它首先比较每个序列的第一个元素。如果相等，则继续比较下一对元素，依此类推。

```auto
print((0, 1, 2) < (0, 3, 4))         // true
print((0, 1, 2000000) < (0, 3, 4))    // true
```

这种比较元组的方式对于排序元组列表或查找最小/最大值很有用。你可以使用带有 `key` 参数的 `sorted` 函数来控制排序顺序。

## 反转字典

假设你想反转字典，以便通过值查找对应的键。但有一个问题 -- 字典中的键必须是唯一的，但值不必唯一。

因此，反转字典的一种方法是创建一个新字典，其中的值是原字典中键的列表。下面的函数接受一个字典并返回其反转后的新字典。

```auto
fn invert_dict(d: HashMap<str, int>) -> HashMap<int, List<str>> {
    let mut new: HashMap<int, List<str>> = {}
    for (key, value) in d.items() {
        if !new.contains_key(value) {
            new[value] = [key]
        } else {
            new[value].append(key)
        }
    }
    return new
}
```

我们可以这样测试：

```auto
let d: HashMap<str, int> = value_counts("parrot")
print(d)           // {"p": 1, "a": 1, "r": 2, "o": 1, "t": 1}
print(invert_dict(d))  // {1: ["p", "a", "o", "t"], 2: ["r"]}
```

这是我们第一次看到字典中的值是列表的示例。以后还会看到更多！

<Listing number="11-3" file-name="tuple_zip.auto" caption="Zip 与字典反转">

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

fn invert_dict(d: HashMap<str, int>) -> HashMap<int, List<str>> {
    let mut new: HashMap<int, List<str>> = {}
    for (key, value) in d.items() {
        if !new.contains_key(value) {
            new[value] = [key]
        } else {
            new[value].append(key)
        }
    }
    return new
}

fn main() {
    // Zip：配对两个序列的元素
    let names: List<str> = ["Alice", "Bob", "Charlie", "Diana"]
    let scores: List<int> = [95, 87, 92, 88]
    print("Zipped pairs:")
    for (name, score) in zip(names, scores) {
        print(f"  $name: $score")
    }

    // 用 zip 从两个列表构建字典
    let letters = "abcde"
    let values = [10, 20, 30, 40, 50]
    let letter_values: HashMap<str, int> = dict(zip(letters, values))
    print("Letter values:", letter_values)

    // Enumerate：将元素与其索引配对
    print("Enumerated:")
    for (index, letter) in enumerate("hello") {
        print(f"  $index: $letter")
    }

    // 字典反转
    let d = value_counts("parrot")
    print("Original:", d)
    let inverted = invert_dict(d)
    print("Inverted:", inverted)

    // 比较元组
    print((0, 1, 2) < (0, 3, 4))         // true
    print((0, 1, 2000000) < (0, 3, 4))    // true
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


def invert_dict(d):
    new = {}
    for key, value in d.items():
        if value not in new:
            new[value] = [key]
        else:
            new[value].append(key)
    return new


def main():
    # Zip：配对两个序列的元素
    names = ["Alice", "Bob", "Charlie", "Diana"]
    scores = [95, 87, 92, 88]
    print("Zipped pairs:")
    for name, score in zip(names, scores):
        print(f"  {name}: {score}")

    # 用 zip 从两个列表构建字典
    letters = "abcde"
    values = [10, 20, 30, 40, 50]
    letter_values = dict(zip(letters, values))
    print(f"Letter values: {letter_values}")

    # Enumerate：将元素与其索引配对
    print("Enumerated:")
    for index, letter in enumerate("hello"):
        print(f"  {index}: {letter}")

    # 字典反转
    d = value_counts("parrot")
    print(f"Original: {d}")
    inverted = invert_dict(d)
    print(f"Inverted: {inverted}")

    # 比较元组
    print((0, 1, 2) < (0, 3, 4))
    print((0, 1, 2000000) < (0, 3, 4))


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`zip` 将两个（或多个）序列的元素配对，产生一个元组迭代器。这对于遍历对应元素很有用 -- 例如，将名字与分数匹配。与 `dict()` 结合使用时，`zip` 可以从单独的键列表和值列表构建字典。

`enumerate` 是 `zip` 的特例，将每个元素与其索引配对。当你需要元素的位置和值时，这是一个常见的模式。

`invert_dict` 演示了一个经典模式：交换字典中键和值的角色。由于值可能不唯一，反转后的字典将每个原始值映射到拥有该值的键的*列表*。

## 调试

列表、字典和元组都是**数据结构**（data structure）。在本章中，我们开始看到复合数据结构，如元组列表、以元组为键且以列表为值的字典。复合数据结构很有用，但容易因数据结构的类型、大小或结构不正确而产生错误。

为了帮助调试这类错误，打印值的类型和结构通常就足够了。对于字典，打印项的数量和几个示例条目可以帮助验证数据是否正确。

## 术语表

**元组（tuple）：**
一个不可变的值序列。

**元组赋值（tuple assignment）：**
左侧是元组、右侧是序列的赋值。右侧被解包，元素被分配给左侧的变量。

**打包（pack）：**
将多个参数收集到一个元组中。

**解包（unpack）：**
将元组（或其他序列）视为多个参数。

**zip 对象（zip object）：**
调用内置函数 `zip` 的结果，可用于遍历元组序列。

**enumerate 对象（enumerate object）：**
调用内置函数 `enumerate` 的结果，可用于遍历索引-元素对的序列。

**排序键（sort key）：**
一个值或计算值的函数，用于对集合中的元素进行排序。

**数据结构（data structure）：**
一个值的集合，组织方式使得某些操作可以高效执行。

## 练习

### 练习

如果元组包含可变值（如列表），则该元组不再可哈希。编写一行代码，向元组内的列表追加一个值，然后确认该元组不能用作字典键。

### 练习

编写一个名为 `shift_word` 的函数，接受一个字符串和一个整数，返回一个新字符串，其中每个字母在字母表中移动给定数量的位置。使用取模运算符从 `'z'` 回到 `'a'`。

### 练习

编写一个名为 `most_frequent_letters` 的函数，接受一个字符串并按频率递减的顺序打印字母。

### 练习

编写一个程序，接受一个单词列表并打印所有回文词组。提示：对于每个单词，对字母排序并拼回字符串。创建一个字典，将排序后的字符串映射到回文词列表。

### 练习

编写一个名为 `word_distance` 的函数，接受两个长度相同的单词，返回两个单词在不同位置的数量。提示：使用 `zip` 遍历对应的字母。
