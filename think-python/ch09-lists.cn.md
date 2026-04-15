# 列表

本章介绍 Python 最有用的内置类型之一 -- 列表（list）。你还将进一步了解对象，以及当多个变量引用同一个对象时会发生什么。

在本章末尾的练习中，我们将创建一个单词列表，并用它来搜索回文和字母重排等特殊单词。

## 列表是序列

与字符串一样，**列表**（list）是一个值的序列。在字符串中，值是字符；在列表中，值可以是任何类型。列表中的值称为**元素**（element）。

创建新列表有几种方式；最简单的是将元素放在方括号（`[` 和 `]`）中。例如，这是一个包含两个整数的列表：

```auto
let numbers = [42, 123]
```

以下是包含三个字符串的列表：

```auto
let cheeses = ["Cheddar", "Edam", "Gouda"]
```

列表中的元素不必是相同类型。以下列表包含一个字符串、一个浮点数、一个整数，甚至还有另一个列表：

```auto
let t = ["spam", 2.0, 5, [10, 20]]
```

列表中的列表是**嵌套的**（nested）。不包含任何元素的列表称为空列表；你可以用空方括号 `[]` 来创建：

```auto
let empty = []
```

`len` 函数返回列表的长度：

```auto
print(cheeses.len())
print(empty.len())
```

> **Python 程序员注意：**
>
> Auto 使用 `.len()` 方法代替 Python 的 `len()` 函数。`a2p` 转译器会自动将 `.len()` 转换为 `len()`。

<Listing number="9-1" file-name="list_basics.auto" caption="创建和索引列表">

```auto
fn main() {
    // 创建列表
    let numbers = [42, 123]
    let cheeses = ["Cheddar", "Edam", "Gouda"]
    let mixed = ["spam", 2.0, 5, [10, 20]]
    let empty: [str; 0] = []

    // 通过索引访问元素
    print("cheeses[0]:", cheeses[0])
    print("cheeses[1]:", cheeses[1])
    print("cheeses[2]:", cheeses[2])
    print("cheeses[-1]:", cheeses[-1])

    // 长度
    print("len(cheeses):", cheeses.len())
    print("len(numbers):", numbers.len())
    print("len(empty):", empty.len())

    // 'in' 运算符
    print("Edam in cheeses:", "Edam" in cheeses)
    print("Wensleydale in cheeses:", "Wensleydale" in cheeses)

    // 嵌套列表：算作一个元素
    print("len(mixed):", mixed.len())
    print("10 in mixed:", 10 in mixed)

    // 访问嵌套元素
    print("mixed[3]:", mixed[3])
    print("mixed[3][0]:", mixed[3][0])
}
```

```python
def main():
    # 创建列表
    numbers = [42, 123]
    cheeses = ["Cheddar", "Edam", "Gouda"]
    mixed = ["spam", 2.0, 5, [10, 20]]
    empty = []

    # 通过索引访问元素
    print(f"cheeses[0]: {cheeses[0]}")
    print(f"cheeses[1]: {cheeses[1]}")
    print(f"cheeses[2]: {cheeses[2]}")
    print(f"cheeses[-1]: {cheeses[-1]}")

    # 长度
    print(f"len(cheeses): {len(cheeses)}")
    print(f"len(numbers): {len(numbers)}")
    print(f"len(empty): {len(empty)}")

    # 'in' 运算符
    print(f"Edam in cheeses: {'Edam' in cheeses}")
    print(f"Wensleydale in cheeses: {'Wensleydale' in cheeses}")

    # 嵌套列表：算作一个元素
    print(f"len(mixed): {len(mixed)}")
    print(f"10 in mixed: {10 in mixed}")

    # 访问嵌套元素
    print(f"mixed[3]: {mixed[3]}")
    print(f"mixed[3][0]: {mixed[3][0]}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

列表使用方括号 `[]` 创建。元素可以是任何类型，列表可以包含混合类型。索引的工作方式与字符串相同 -- `cheeses[0]` 返回第一个元素，`cheeses[-1]` 返回最后一个。`in` 运算符检查某个值是否出现在列表中的任何位置。嵌套列表（列表中的列表）算作单个元素，所以 `10 in mixed` 为 `false`，即使 `10` 是嵌套列表 `mixed[3]` 的元素。

## 列表是可变的

与字符串不同，列表是可变的。当方括号运算符出现在赋值的左侧时，它标识要赋值的列表元素：

```auto
let mut numbers = [42, 123]
numbers[1] = 17
print(numbers)
```

`numbers` 的第二个元素原来是 `123`，现在是 `17`。

列表索引的工作方式与字符串索引相同：

- 任何整数表达式都可以用作索引。
- 如果尝试读取或写入不存在的元素，会得到 `IndexError`。
- 如果索引为负值，则从列表末尾向后计数。

## 列表切片

切片运算符对列表的操作与对字符串的操作相同：

```auto
let letters = ["a", "b", "c", "d"]
print(letters[1..3])   // ["b", "c"]
print(letters[..2])    // ["a", "b"]
print(letters[2..])    // ["c", "d"]
print(letters[..])     // ["a", "b", "c", "d"]
```

复制列表的另一种方法是使用 `list` 函数：

```auto
let copy = list(letters)
```

因为 `list` 是内置函数的名称，所以应避免将其用作变量名。

## 列表运算

`+` 运算符连接列表：

```auto
let t1 = [1, 2]
let t2 = [3, 4]
print(t1 + t2)    // [1, 2, 3, 4]
```

`*` 运算符将列表重复给定次数：

```auto
print(["spam"] * 4)    // ["spam", "spam", "spam", "spam"]
```

内置函数 `sum` 对元素求和：

```auto
print(sum(t1))    // 3
```

`min` 和 `max` 分别找到最小和最大的元素。

## 列表方法

Python 提供了对列表进行操作的方法。例如，`append` 在列表末尾添加一个新元素：

```auto
let mut letters = ["a", "b", "c"]
letters.append("d")
```

`extend` 接受一个列表作为参数，并附加所有元素：

```auto
letters.extend(["e", "f"])
```

有两种方法可以从列表中删除元素。如果你知道索引，可以使用 `pop`：

```auto
let mut t = ["a", "b", "c"]
let removed = t.pop(1)    // 删除并返回 "b"
```

如果你知道要删除的元素（但不知道索引），可以使用 `remove`：

```auto
let mut t = ["a", "b", "c"]
t.remove("b")    // 修改列表，返回 None
```

<Listing number="9-2" file-name="list_methods.auto" caption="列表方法：append、sort、pop">

```auto
fn main() {
    // append：添加一个元素
    let mut letters = ["a", "b", "c"]
    letters.append("d")
    print("After append:", letters)

    // extend：添加多个元素
    letters.extend(["e", "f"])
    print("After extend:", letters)

    // pop：按索引删除
    let mut t = ["a", "b", "c"]
    let removed = t.pop(1)
    print("Popped:", removed)
    print("After pop:", t)

    // remove：按值删除
    let mut t2 = ["a", "b", "c"]
    t2.remove("b")
    print("After remove:", t2)

    // sort：原地排序（升序）
    let mut nums = [3, 1, 4, 1, 5, 9]
    nums.sort()
    print("Sorted:", nums)

    // sorted：返回新的排序列表（原列表不变）
    let scramble = ["c", "a", "b"]
    let sorted_list = sorted(scramble)
    print("Original:", scramble)
    print("Sorted copy:", sorted_list)

    // reverse
    let mut items = [1, 2, 3]
    items.reverse()
    print("Reversed:", items)

    // index：查找元素位置
    let fruits = ["apple", "banana", "cherry"]
    print("index of banana:", fruits.index("banana"))

    // count：计数出现次数
    let data = [1, 2, 2, 3, 2]
    print("count of 2:", data.count(2))
}
```

```python
def main():
    # append：添加一个元素
    letters = ["a", "b", "c"]
    letters.append("d")
    print(f"After append: {letters}")

    # extend：添加多个元素
    letters.extend(["e", "f"])
    print(f"After extend: {letters}")

    # pop：按索引删除
    t = ["a", "b", "c"]
    removed = t.pop(1)
    print(f"Popped: {removed}")
    print(f"After pop: {t}")

    # remove：按值删除
    t2 = ["a", "b", "c"]
    t2.remove("b")
    print(f"After remove: {t2}")

    # sort：原地排序（升序）
    nums = [3, 1, 4, 1, 5, 9]
    nums.sort()
    print(f"Sorted: {nums}")

    # sorted：返回新的排序列表（原列表不变）
    scramble = ["c", "a", "b"]
    sorted_list = sorted(scramble)
    print(f"Original: {scramble}")
    print(f"Sorted copy: {sorted_list}")

    # reverse
    items = [1, 2, 3]
    items.reverse()
    print(f"Reversed: {items}")

    # index：查找元素位置
    fruits = ["apple", "banana", "cherry"]
    print(f"index of banana: {fruits.index('banana')}")

    # count：计数出现次数
    data = [1, 2, 2, 3, 2]
    print(f"count of 2: {data.count(2)}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`append` 在末尾添加一个元素；`extend` 从另一个列表添加所有元素。`pop(index)` 删除并返回给定索引处的元素。`remove(value)` 删除给定值的第一次出现（返回 `None`）。`sort()` 原地排序列表，修改原始列表。`sorted()` 返回一个新的排序列表，不改变原始列表。`reverse()` 原地反转列表。`index(value)` 返回第一次出现的索引。`count(value)` 返回出现次数。

> **Python 程序员注意：**
>
> Auto 使用与 Python 类似的 `.len()` 和 `.sort()` 方法。`a2p` 转译器会自动转换这些方法。注意 `sorted()` 在两种语言中都是内置函数，返回一个新列表。

## 列表与字符串

字符串是字符的序列，列表是值的序列，但字符列表与字符串不同。要将字符串转换为字符列表，可以使用 `list` 函数：

```auto
let s = "spam"
let t = list(s)
print(t)    // ["s", "p", "a", "m"]
```

`list` 函数将字符串拆分为单个字母。如果要将字符串拆分为单词，可以使用 `split` 方法：

```auto
let s = "pining for the fjords"
let t = s.split(" ")
```

一个可选参数叫做**分隔符**（delimiter），指定哪些字符用作单词边界：

```auto
let s = "ex-parrot"
let t = s.split("-")    // ["ex", "parrot"]
```

如果你有一个字符串列表，可以使用 `join` 将它们连接成单个字符串。`join` 是一个字符串方法，所以你必须在分隔符上调用它，并将列表作为参数传递：

```auto
let delimiter = " "
let t = ["pining", "for", "the", "fjords"]
let s = delimiter.join(t)
```

## 遍历列表

你可以使用 `for` 语句来遍历列表中的元素：

```auto
let cheeses = ["Cheddar", "Edam", "Gouda"]

for cheese in cheeses {
    print(cheese)
}
```

例如，使用 `split` 将字符串拆分为单词列表后，我们可以使用 `for` 来遍历它们：

```auto
let s = "pining for the fjords"

for word in s.split(" ") {
    print(word)
}
```

对空列表的 `for` 循环永远不会执行缩进的语句。

## 列表排序

Python 提供了一个名为 `sorted` 的内置函数来排序列表的元素。原始列表保持不变：

```auto
let scramble = ["c", "a", "b"]
let sorted_scramble = sorted(scramble)
print(scramble)         // ["c", "a", "b"] -- 不变
print(sorted_scramble)  // ["a", "b", "c"]
```

`sorted` 可以处理任何类型的序列，不仅仅是列表。所以我们可以这样对字符串中的字母进行排序：

```auto
let sorted_letters = sorted("letters")
print(sorted_letters)   // ['e', 'e', 'l', 'r', 's', 't', 't']
```

结果是一个列表。要将列表转换为字符串，我们可以使用 `join`：

```auto
let result = "".join(sorted("letters"))
print(result)   // "eelrstt"
```

以空字符串作为分隔符，列表中的元素将不加任何间隔地连接在一起。

<Listing number="9-3" file-name="list_operations.auto" caption="遍历与列表操作">

```auto
fn main() {
    // 遍历列表
    let cheeses = ["Cheddar", "Edam", "Gouda"]
    print("Cheeses:")
    for cheese in cheeses {
        print(" ", cheese)
    }

    // 遍历字符串中的单词
    let sentence = "pining for the fjords"
    print("\nWords:")
    for word in sentence.split(" ") {
        print(" ", word)
    }

    // 列表连接
    let t1 = [1, 2]
    let t2 = [3, 4]
    print("\nConcat:", t1 + t2)

    // 列表重复
    print("Repeat:", ["spam"] * 3)

    // Sum, min, max
    print("Sum:", sum([1, 2, 3, 4]))
    print("Min:", min([5, 2, 8, 1]))
    print("Max:", max([5, 2, 8, 1]))

    // 字符串 <-> 列表转换
    let s = "hello"
    let chars = list(s)
    print("list('hello'):", chars)
    print("join:", chars.join("-"))

    // 排序字符串字母
    let sorted_str = "".join(sorted("letters"))
    print("Sorted letters:", sorted_str)

    // 使用 enumerate 带索引遍历
    let fruits = ["apple", "banana", "cherry"]
    print("\nWith index:")
    for (i, fruit) in fruits.enumerate() {
        print(f"  $i: $fruit")
    }
}
```

```python
def main():
    # 遍历列表
    cheeses = ["Cheddar", "Edam", "Gouda"]
    print("Cheeses:")
    for cheese in cheeses:
        print(f" {cheese}")

    # 遍历字符串中的单词
    sentence = "pining for the fjords"
    print("\nWords:")
    for word in sentence.split(" "):
        print(f" {word}")

    # 列表连接
    t1 = [1, 2]
    t2 = [3, 4]
    print(f"\nConcat: {t1 + t2}")

    # 列表重复
    print(f"Repeat: {['spam'] * 3}")

    # Sum, min, max
    print(f"Sum: {sum([1, 2, 3, 4])}")
    print(f"Min: {min([5, 2, 8, 1])}")
    print(f"Max: {max([5, 2, 8, 1])}")

    # 字符串 <-> 列表转换
    s = "hello"
    chars = list(s)
    print(f"list('hello'): {chars}")
    print(f"join: {'-'.join(chars)}")

    # 排序字符串字母
    sorted_str = "".join(sorted("letters"))
    print(f"Sorted letters: {sorted_str}")

    # 使用 enumerate 带索引遍历
    fruits = ["apple", "banana", "cherry"]
    print("\nWith index:")
    for i, fruit in enumerate(fruits):
        print(f"  {i}: {fruit}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`for item in list` 遍历每个元素。`split(" ")` 将字符串拆分为单词列表。`+` 运算符连接列表，`*` 重复列表。内置函数 `sum`、`min` 和 `max` 对列表进行操作。`list(string)` 将字符串转换为字符列表，`delimiter.join(list)` 将列表连接为字符串。`sorted()` 从任何序列返回一个新的排序列表。`enumerate()` 产生 `(index, value)` 对，用于带索引的遍历。

> **Python 程序员注意：**
>
> Auto 使用 `.enumerate()` 方法代替 Python 的 `enumerate()` 函数。`a2p` 转译器会自动转换。Auto 的 `.split()` 需要显式传递分隔符参数。

## 对象与值

如果我们运行以下赋值语句：

```auto
let a = "banana"
let b = "banana"
```

我们知道 `a` 和 `b` 都引用一个字符串，但我们不知道它们是否引用*同一个*字符串。要检查两个变量是否引用同一个对象，可以使用 `is` 运算符：

```auto
print(a is b)    // true（对于字符串，Auto 可能重用同一个对象）
```

但当你创建两个列表时，你得到的是两个对象：

```auto
let a = [1, 2, 3]
let b = [1, 2, 3]
print(a is b)    // false（两个独立的列表对象）
```

在这种情况下，我们会说这两个列表是**等价的**（equivalent），因为它们有相同的元素，但不是**同一的**（identical），因为它们不是同一个对象。如果两个对象是同一的，它们也是等价的，但如果它们是等价的，不一定是同一的。

## 别名

如果 `a` 引用一个对象，而你赋值 `b = a`，那么两个变量都引用同一个对象：

```auto
let mut a = [1, 2, 3]
let b = a
print(b is a)    // true
```

变量与对象的关联称为**引用**（reference）。在这个例子中，对同一个对象有两个引用。

有多个引用的对象有多个名称，所以我们说该对象是**别名的**（aliased）。如果被别名的对象是可变的，通过一个名称进行的修改会影响另一个：

```auto
b[0] = 5
print(a)    // [5, 2, 3] -- a "看到"了这个变化
```

所以我们会说 `a` "看到"了这个变化。虽然这种行为很有用，但容易出错。通常，在使用可变对象时，避免别名更安全。

对于像字符串这样不可变的对象，别名不是太大的问题。

## 列表参数

当你将列表传递给函数时，函数获得对列表的引用。如果函数修改了列表，调用者会看到变化：

```auto
fn pop_first(lst: [int]) -> int {
    return lst.pop(0)
}

let mut letters = ["a", "b", "c"]
let first = pop_first(letters)
print(first)    // "a"
print(letters)  // ["b", "c"] -- 列表被修改了
```

在这个例子中，参数 `lst` 和变量 `letters` 是同一个对象的别名。将对象的引用作为参数传递给函数创建了一种别名形式。如果函数修改了对象，这些修改在函数完成后仍然存在。

<Listing number="9-4" file-name="aliasing.auto" caption="别名与引用">

```auto
fn pop_first(lst: [str]) -> str {
    return lst.pop(0)
}

fn append_item(lst: [str], item: str) {
    lst.append(item)
}

fn main() {
    // 别名：两个名称，一个对象
    let mut a = [1, 2, 3]
    let b = a
    print("b is a:", b is a)
    print("Before change - a:", a)

    // 通过 b 修改会影响 a
    b[0] = 5
    print("After b[0] = 5 - a:", a)

    // 列表即使等价也不是同一的
    let c = [1, 2, 3]
    let d = [1, 2, 3]
    print("c == d:", c == d)
    print("c is d:", c is d)

    // 字符串：别名是安全的（不可变）
    let s1 = "banana"
    let s2 = s1
    print("s1 is s2:", s1 is s2)

    // 列表参数：调用者看到变化
    let mut letters = ["a", "b", "c"]
    print("\nBefore pop_first:", letters)
    let first = pop_first(letters)
    print("Popped:", first)
    print("After pop_first:", letters)

    let mut items = ["x", "y"]
    print("\nBefore append_item:", items)
    append_item(items, "z")
    print("After append_item:", items)

    // 复制列表以避免别名
    let mut original = [10, 20, 30]
    let copy = original[..]  // 切片复制
    copy[0] = 99
    print("\noriginal after copy modified:", original)
    print("copy:", copy)
}
```

```python
def pop_first(lst):
    return lst.pop(0)


def append_item(lst, item):
    lst.append(item)


def main():
    # 别名：两个名称，一个对象
    a = [1, 2, 3]
    b = a
    print(f"b is a: {b is a}")
    print(f"Before change - a: {a}")

    # 通过 b 修改会影响 a
    b[0] = 5
    print(f"After b[0] = 5 - a: {a}")

    # 列表即使等价也不是同一的
    c = [1, 2, 3]
    d = [1, 2, 3]
    print(f"c == d: {c == d}")
    print(f"c is d: {c is d}")

    # 字符串：别名是安全的（不可变）
    s1 = "banana"
    s2 = s1
    print(f"s1 is s2: {s1 is s2}")

    # 列表参数：调用者看到变化
    letters = ["a", "b", "c"]
    print(f"\nBefore pop_first: {letters}")
    first = pop_first(letters)
    print(f"Popped: {first}")
    print(f"After pop_first: {letters}")

    items = ["x", "y"]
    print(f"\nBefore append_item: {items}")
    append_item(items, "z")
    print(f"After append_item: {items}")

    # 复制列表以避免别名
    original = [10, 20, 30]
    copy = original[:]
    copy[0] = 99
    print(f"\noriginal after copy modified: {original}")
    print(f"copy: {copy}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

当你对列表赋值 `b = a` 时，两个变量指向同一个对象。通过一个名称修改列表（`b[0] = 5`）会通过另一个名称可见（`a`）。这就是**别名**（aliasing）。

`is` 运算符检查同一性（同一对象），而 `==` 检查等价性（相同值）。具有相同内容的两个列表是等价的但不是同一的。

当你将列表传递给函数时，函数接收对同一对象的引用（别名）。函数对列表所做的任何修改对调用者都是可见的。

要避免别名，你可以使用完整切片创建副本：Auto 中为 `original[..]`，Python 中为 `original[:]`。这创建了一个具有相同元素的新列表，对副本的修改不会影响原始列表。

## 创建单词列表

在上一章中，我们读取了文件 `words.txt` 并搜索具有某些属性的单词。但我们多次读取整个文件，这并不高效。更好的做法是只读取一次文件并将单词放入列表中：

```auto
let mut word_list: [str] = []

for line in open("words.txt") {
    let word = line.strip()
    word_list.append(word)
}

print(word_list.len())
```

另一种做同样事情的方法是使用 `read` 将整个文件读入一个字符串，然后使用 `split` 将其拆分为单词列表：

```auto
let string = open("words.txt").read()
let word_list = string.split("\n")
print(word_list.len())
```

现在，要检查字符串是否出现在列表中，我们可以使用 `in` 运算符。

## 调试

请注意，大多数列表方法修改参数并返回 `None`。这与字符串方法相反，字符串方法返回一个新字符串而不修改原始字符串。

如果你习惯写这样的字符串代码：

```auto
let word = "plumage!"
let word = word.strip("!")
```

你可能会想写这样的列表代码：

```auto
let mut t = [1, 2, 3]
t = t.remove(3)    // 错误！
```

`remove` 修改列表并返回 `None`，所以 `t` 变成 `None`，后续对 `t` 的任何操作都可能失败。这是从字符串转向列表的程序员常犯的错误。

如果你看到这样的错误信息，你应该回溯程序，检查是否可能错误地调用了列表方法。

## 术语表

**列表（list）：**
包含值序列的对象。

**元素（element）：**
列表或其他序列中的一个值。

**嵌套列表（nested list）：**
作为另一个列表元素的列表。

**分隔符（delimiter）：**
用于指示字符串应在何处拆分的字符或字符串。

**等价的（equivalent）：**
具有相同的值。

**同一的（identical）：**
是同一个对象（这暗示等价性）。

**引用（reference）：**
变量与其值之间的关联。

**别名的（aliased）：**
如果有多个变量引用一个对象，则该对象是别名的。

**属性（attribute）：**
与对象关联的命名值之一。

## 练习

### 练习

两个单词是**字母重排**（anagram），如果你能从一个单词中重新排列字母拼出另一个单词。例如，`tops` 是 `stop` 的字母重排。

检查两个单词是否为字母重排的一种方法是对两个单词中的字母进行排序。如果排序后的字母列表相同，这两个单词就是字母重排。

编写一个名为 `is_anagram` 的函数，接受两个字符串，如果是字母重排则返回 `true`。

```
is_anagram("tops", "stop")     // 应该为 true
is_anagram("skate", "takes")   // 应该为 true
is_anagram("tops", "takes")    // 应该为 false
```

### 练习

**回文**（palindrome）是正读反读都一样的单词，如 "noon" 和 "rotator"。编写一个名为 `is_palindrome` 的函数，接受一个字符串参数，如果是回文则返回 `true`，否则返回 `false`。

```
is_palindrome("bob")      // 应该为 true
is_palindrome("alice")    // 应该为 false
is_palindrome("a")        // 应该为 true
is_palindrome("")         // 应该为 true
```

### 练习

编写一个名为 `reverse_sentence` 的函数，接受一个包含任意数量由空格分隔的单词的字符串。它应该返回一个包含相同单词但顺序相反的新字符串。例如，如果参数是 "Reverse this sentence"，结果应该是 "Sentence this reverse"。

提示：你可以使用 `capitalize` 方法将第一个单词首字母大写，并将其他单词转换为小写。

### 练习

编写一个名为 `total_length` 的函数，接受一个字符串列表并返回这些字符串的总长度。使用循环和累加器模式。
