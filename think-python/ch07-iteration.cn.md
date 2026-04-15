# 迭代与搜索

1939 年，欧内斯特·文森特·赖特出版了一部 50,000 字的小说《Gadsby》，书中不包含字母 "e"。由于 "e" 是英语中最常见的字母，即使不使用它写几个词也很困难。

为了感受这有多困难，在本章中我们将计算含有至少一个 "e" 的英语单词所占的比例。为此，我们将使用 `for` 循环来遍历字符串中的字母，并在循环中更新变量来计数。我们将使用 `in` 运算符来检查字母是否出现在单词中，你还将学习一种叫做"线性搜索"的编程模式。

## 循环与字符串

在第 3 章中，我们看到了使用范围表达式显示数字序列的 `for` 循环：

```auto
for i in 0..3 {
    print(i, end=" ")
}
```

我们也可以使用 `for` 循环来遍历字符串中的字母：

```auto
for letter in "Gadsby" {
    print(letter, end=" ")
}
```

在 `for` 循环中定义的变量被称为**循环变量**（loop variable）。在这个例子中，我们将变量名从 `i` 改为 `letter`，这提供了更多关于它所引用值的信息。

既然我们可以遍历单词中的字母，就可以检查它是否包含字母 "e"。以下是一个函数，如果单词包含 "e" 则返回 `true`，否则返回 `false`：

```auto
fn has_e(word: str) -> bool {
    for letter in word {
        if letter == 'E' || letter == 'e' {
            return true
        }
    }
    return false
}
```

这个函数遍历单词中的每个字母。如果找到 'E' 或 'e'，立即返回 `true`。如果遍历完整个循环都没有找到，返回 `false`。

> **Python 程序员注意：**
>
> Auto 使用 `||` 代替 Python 的 `or`。`a2p` 转译器会自动将 `||` 转换为 `or`。

<Listing number="7-1" file-name="loop_strings.auto" caption="遍历字符串并检查字母">

```auto
fn has_e(word: str) -> bool {
    for letter in word {
        if letter == 'E' || letter == 'e' {
            return true
        }
    }
    return false
}

fn main() {
    // 遍历字符串中的字符
    print("Letters in Gadsby:")
    for letter in "Gadsby" {
        print(letter, end=" ")
    }
    print()

    // 检查单词中是否有 'e'
    print("has_e('Gadsby'):", has_e("Gadsby"))
    print("has_e('Emma'):", has_e("Emma"))
    print("has_e('hello'):", has_e("hello"))
    print("has_e('world'):", has_e("world"))
}
```

```python
def has_e(word):
    for letter in word:
        if letter == "E" or letter == "e":
            return True
    return False


def main():
    # 遍历字符串中的字符
    print("Letters in Gadsby:")
    for letter in "Gadsby":
        print(letter, end=" ")
    print()

    # 检查单词中是否有 'e'
    print(f"has_e('Gadsby'): {has_e('Gadsby')}")
    print(f"has_e('Emma'): {has_e('Emma')}")
    print(f"has_e('hello'): {has_e('hello')}")
    print(f"has_e('world'): {has_e('world')}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

第一个循环遍历字符串 `"Gadsby"` 中的每个字符并用空格分隔打印。`print` 的 `end=" "` 参数防止每个字符后换行。

`has_e` 函数演示了提前返回模式：它遍历每个字母，一旦找到匹配项就返回 `true`。如果循环完成而没有找到匹配项，函数返回 `false`。注意第二个 `return` 在循环之外 -- 一个常见的错误是将两个 `return` 语句都放在循环内，这样只会检查第一个字母。

## 读取单词列表

要查看有多少单词包含 "e"，我们需要一个单词列表。在 Python 中，我们可以使用 `open` 函数读取文件，然后使用 `for` 循环处理每一行。

在 Auto 中，文件 I/O 的工作方式类似。以下是从文件中读取行的基本模式：

```auto
for line in open("words.txt") {
    let word = line.strip()
    print(word)
}
```

`strip` 方法从字符串的开头和末尾移除空白字符 -- 包括空格、制表符和换行符。这是必要的，因为文件中的每一行都以换行符结尾。

## 更新变量

正如你可能已经发现的，对同一个变量进行多次赋值是合法的。新的赋值使现有变量引用一个新值（并停止引用旧值）。

```auto
let mut x = 5
x = 7
```

一种常见的赋值是**更新**（update），变量的新值依赖于旧值：

```auto
let mut x = 7
x = x + 1
```

这个语句的意思是"获取 `x` 的当前值，加一，然后将结果赋回给 `x`"。

如果你尝试更新一个不存在的变量，会得到一个错误，因为右边的表达式在左边的赋值之前被求值。在更新变量之前，你必须先**初始化**（initialize）它，通常使用一个简单的赋值。

增加变量的值称为**递增**（increment）；减少变量的值称为**递减**（decrement）。由于这些操作非常常见，Auto 提供了**增强赋值运算符**，可以更简洁地更新变量：

```auto
let mut z = 0
z += 2
```

> **Python 程序员注意：**
>
> Auto 要求使用 `let mut` 来声明将被重新赋值的变量。`a2p` 转译器会将 `let mut` 转换为普通赋值。`+=`、`-=` 和 `*=` 等增强赋值运算符在两种语言中工作方式相同。

## 循环与计数

以下程序计算单词列表中的单词数量：

```auto
let mut total = 0

for line in open("words.txt") {
    let word = line.strip()
    total += 1
}
```

它首先将 `total` 初始化为 `0`。每次循环时，将 `total` 递增 1。因此，当循环退出时，`total` 引用单词的总数。

这样的变量，用于计算某事发生的次数，被称为**计数器**（counter）。

<Listing number="7-2" file-name="for_range.auto" caption="带范围的 for 循环与累加器模式">

```auto
fn main() {
    // 带范围的 for 循环
    print("Counting from 0 to 4:")
    for i in 0..5 {
        print(i, end=" ")
    }
    print()

    // 带步长的 for 循环
    print("Even numbers from 0 to 10:")
    for i in 0..=10 {
        if i % 2 == 0 {
            print(i, end=" ")
        }
    }
    print()

    // 遍历字符串
    print("Letters in Auto:")
    for letter in "Auto" {
        print(letter, end=" ")
    }
    print()

    // 累加器模式：从 1 到 10 的和
    let mut total = 0
    for i in 1..=10 {
        total += i
    }
    print("Sum from 1 to 10:", total)
}
```

```python
def main():
    # 带范围的 for 循环
    print("Counting from 0 to 4:")
    for i in range(5):
        print(i, end=" ")
    print()

    # 带步长的 for 循环
    print("Even numbers from 0 to 10:")
    for i in range(11):
        if i % 2 == 0:
            print(i, end=" ")
    print()

    # 遍历字符串
    print("Letters in Auto:")
    for letter in "Auto":
        print(letter, end=" ")
    print()

    # 累加器模式：从 1 到 10 的和
    total = 0
    for i in range(1, 11):
        total += i
    print(f"Sum from 1 to 10: {total}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

第一个循环使用 `0..5` 从 0 计数到 4。在 Auto 中，`0..5` 产生值 0、1、2、3、4（上界是排他的）。第二个循环使用 `0..=10`，这是一个**包含范围**（inclusive range），包含 10，结合 `if` 语句过滤偶数。

第三个循环遍历字符串 `"Auto"` 中的字符。

最后一个例子演示了**累加器模式**（accumulator pattern）：初始化一个变量（`total = 0`），然后在循环中反复更新它（`total += i`）。这种模式在编程中经常用于计算总和、计数和其他聚合值。

## `in` 运算符

我们之前编写的 `has_e` 版本比必要的复杂。Python 提供了一个 `in` 运算符来检查字符是否出现在字符串中。在 Auto 中，我们可以类似地使用 `contains` 方法或 `in` 运算符：

```auto
let word = "Gadsby"
print('e' in word)
```

所以我们可以更简单地重写 `has_e`。由于 `if` 语句的条件具有布尔值，我们可以直接返回布尔值：

```auto
fn has_e(word: str) -> bool {
    return 'e' in word.to_lowercase()
}
```

`to_lowercase` 方法将字符串中的字母转换为小写，创建一个新字符串而不修改原始字符串。这样，我们只需要检查小写的 'e'。

## 搜索

基于这个更简单的 `has_e` 版本，让我们编写一个更通用的函数 `uses_any`，它接受第二个参数作为字母字符串。如果单词使用了其中任何一个字母，它返回 `true`，否则返回 `false`：

```auto
fn uses_any(word: str, letters: str) -> bool {
    for letter in word.to_lowercase() {
        if letters.to_lowercase().contains(letter) {
            return true
        }
    }
    return false
}
```

`uses_any` 的结构与 `has_e` 类似。它逐个检查 `word` 中的字母。如果找到一个出现在 `letters` 中的字母，立即返回 `true`。如果遍历完整个循环都没有找到，返回 `false`。

这种模式被称为**线性搜索**（linear search）。

<Listing number="7-3" file-name="search.auto" caption="线性搜索：uses_any 和 find">

```auto
fn uses_any(word: str, letters: str) -> bool {
    for letter in word.to_lowercase() {
        if letters.to_lowercase().contains(letter) {
            return true
        }
    }
    return false
}

fn find(word: str, letter: str) -> int {
    let mut index = 0
    for ch in word {
        if ch == letter {
            return index
        }
        index += 1
    }
    return -1
}

fn main() {
    // 测试 uses_any（线性搜索）
    print("uses_any('banana', 'aeiou'):", uses_any("banana", "aeiou"))
    print("uses_any('apple', 'xyz'):", uses_any("apple", "xyz"))
    print("uses_any('Banana', 'AEIOU'):", uses_any("Banana", "AEIOU"))

    // 测试 find（查找第一次出现的位置）
    print("find('hello', 'l'):", find("hello", "l"))
    print("find('hello', 'o'):", find("hello", "o"))
    print("find('hello', 'z'):", find("hello", "z"))
}
```

```python
def uses_any(word, letters):
    for letter in word.lower():
        if letter in letters.lower():
            return True
    return False


def find(word, letter):
    index = 0
    for ch in word:
        if ch == letter:
            return index
        index += 1
    return -1


def main():
    # 测试 uses_any（线性搜索）
    print(f"uses_any('banana', 'aeiou'): {uses_any('banana', 'aeiou')}")
    print(f"uses_any('apple', 'xyz'): {uses_any('apple', 'xyz')}")
    print(f"uses_any('Banana', 'AEIOU'): {uses_any('Banana', 'AEIOU')}")

    # 测试 find（查找第一次出现的位置）
    print(f"find('hello', 'l'): {find('hello', 'l')}")
    print(f"find('hello', 'o'): {find('hello', 'o')}")
    print(f"find('hello', 'z'): {find('hello', 'z')}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`uses_any` 使用 `to_lowercase()`（在 Python 中变为 `.lower()`）将 `word` 和 `letters` 都转换为小写，然后执行线性搜索：它将单词的每个字母与允许的字母进行检查。一旦找到匹配项，就返回 `true`。如果检查完所有字母后没有找到匹配项，返回 `false`。

`find` 演示了另一种搜索模式：它在单词中查找特定字母的第一次出现并返回其索引。它维护一个计数器（`index`），每次迭代递增。如果找到该字母，返回当前索引；如果循环完成而没有找到该字母，返回 `-1` 表示"未找到"。

> **Python 程序员注意：**
>
> Auto 使用 `to_lowercase()` 代替 Python 的 `.lower()` 方法。`a2p` 转译器会自动转换。Auto 使用 `contains()` 方法或 `in` 运算符进行成员测试，两者都转换为 Python 的 `in` 运算符。

## 文档测试

我们可以使用文档字符串来测试函数。以下是带有包含测试的文档字符串的 `uses_any` 版本：

```python
def uses_any(word, letters):
    """检查单词是否使用了给定字母中的任何一个。

    >>> uses_any('banana', 'aeiou')
    True
    >>> uses_any('apple', 'xyz')
    False
    """
    for letter in word.lower():
        if letter in letters.lower():
            return True
    return False
```

每个测试以 `>>>` 开始，这在某些 Python 环境中用作提示符。下一行指示如果函数工作正确，表达式应该具有的值。

要运行这些测试，我们使用 `doctest` 模块。如果所有测试都通过，不会显示任何输出 -- 在这种情况下，没有消息就是好消息。如果测试失败，输出将包括失败的示例、期望值和实际值。

## 使用累加器计数

让我们将学到的模式结合起来。以下是一个函数，计算特定字母在单词中出现的次数，然后用它来计算列表中有多少单词包含特定字母：

<Listing number="7-4" file-name="counting.auto" caption="使用累加器模式计数">

```auto
fn count_letter(word: str, target: str) -> int {
    let mut count = 0
    for letter in word {
        if letter == target {
            count += 1
        }
    }
    return count
}

fn main() {
    // 使用累加器模式计数
    print("Counting 'l' in 'hello':", count_letter("hello", "l"))
    print("Counting 'e' in 'Emma':", count_letter("Emma", "e"))
    print("Counting 'a' in 'banana':", count_letter("banana", "a"))
    print("Counting 'z' in 'hello':", count_letter("hello", "z"))

    // 从列表中统计包含 'e' 的单词
    let words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    let mut total = 0
    let mut count_e = 0
    for word in words {
        total += 1
        if count_letter(word, "e") > 0 {
            count_e += 1
        }
    }
    print("Total words:", total)
    print("Words with 'e':", count_e)
    print("Percentage with 'e':", count_e * 100 / total)
}
```

```python
def count_letter(word, target):
    count = 0
    for letter in word:
        if letter == target:
            count += 1
    return count


def main():
    # 使用累加器模式计数
    print(f"Counting 'l' in 'hello': {count_letter('hello', 'l')}")
    print(f"Counting 'e' in 'Emma': {count_letter('Emma', 'e')}")
    print(f"Counting 'a' in 'banana': {count_letter('banana', 'a')}")
    print(f"Counting 'z' in 'hello': {count_letter('hello', 'z')}")

    # 从列表中统计包含 'e' 的单词
    words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    total = 0
    count_e = 0
    for word in words:
        total += 1
        if count_letter(word, "e") > 0:
            count_e += 1
    print(f"Total words: {total}")
    print(f"Words with 'e': {count_e}")
    print(f"Percentage with 'e': {count_e * 100 // total}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`count_letter` 演示了计数器/累加器模式：将 `count` 初始化为 0，遍历每个字母，找到匹配项时递增 `count`，最后返回最终计数。

在 `main()` 中，我们首先用几个示例测试 `count_letter`。然后在一个更大的模式中使用它：我们遍历一个单词列表，维护两个计数器 -- `total`（所有单词）和 `count_e`（包含 'e' 的单词）。这演示了累加器模式如何扩展以解决实际问题。百分比计算显示大约三分之二的英语单词包含字母 "e"，这解释了为什么不使用它来写一本书是如此困难。

## 调试

调试循环时，最常见的错误包括：

- **差一错误**（Off-by-one errors）：循环多运行一次或少运行一次。这通常是因为对范围的上界是包含还是排他的混淆造成的。

- **无限循环**（Infinite loops）：如果循环条件永远不会为假，循环将永远运行。在 Auto 中，带范围的 `for` 循环总是会终止，但 `for cond {}` 循环（行为类似于 `while` 循环）如果条件永远不变为假，可能会无限循环。

- **错误的初始化**：忘记在循环之前初始化计数器或累加器，或者初始化为错误的值。

- **作用域错误**：试图在循环外使用循环变量，或者忘记循环内创建的变量在循环结束后不会持续存在。

## 术语表

**循环变量（loop variable）：**
在 `for` 循环头部定义的变量。

**文件对象（file object）：**
表示打开的文件并跟踪文件哪些部分已被读取或写入的对象。

**方法（method）：**
与对象关联并通过点运算符调用的函数。

**更新（update）：**
为已存在的变量赋予新值的赋值语句。

**初始化（initialize）：**
创建一个新变量并赋予它一个值。

**递增（increment）：**
增加变量的值。

**递减（decrement）：**
减少变量的值。

**计数器（counter）：**
用于计数的变量，通常初始化为零然后递增。

**累加器（accumulator）：**
用于累加结果的变量，例如总和或计数。

**线性搜索（linear search）：**
一种计算模式，搜索一系列元素并在找到目标时停止。

**通过（pass）：**
如果测试运行且结果符合预期，则测试通过。

**失败（fail）：**
如果测试运行且结果不符合预期，则测试失败。

## 练习

### 练习

编写一个名为 `uses_none` 的函数，接受一个单词和一个禁止字母字符串，如果单词不使用任何禁止字母则返回 `true`。

```
uses_none('banana', 'xyz')   // 应该返回 true
uses_none('apple', 'efg')    // 应该返回 false
```

### 练习

编写一个名为 `uses_only` 的函数，接受一个单词和一个字母字符串，如果单词只包含该字符串中的字母则返回 `true`。

```
uses_only('banana', 'ban')   // 应该返回 true
uses_only('apple', 'apl')    // 应该返回 false
```

### 练习

编写一个名为 `uses_all` 的函数，接受一个单词和一个字母字符串，如果单词至少包含该字符串中的所有字母各一次则返回 `true`。

```
uses_all('banana', 'ban')   // 应该返回 true
uses_all('apple', 'api')    // 应该返回 false
```

### 练习

《纽约时报》每天发布一个名为"Spelling Bee"的谜题，挑战读者仅使用七个字母拼出尽可能多的单词，其中一个是必需的字母。单词必须至少有四个字母。

编写一个名为 `check_word` 的函数来检查给定单词是否可接受。它应该接受要检查的单词、七个可用字母的字符串和包含单个必需字母的字符串作为参数。你可以使用之前练习中编写的函数。

```
check_word('color', 'ACDLORT', 'R')    // 应该返回 true
check_word('ratatat', 'ACDLORT', 'R')  // 应该返回 true
check_word('rat', 'ACDLORT', 'R')      // 应该返回 false（太短）
check_word('told', 'ACDLORT', 'R')     // 应该返回 false（缺少 R）
```
