# 字符串与正则表达式

字符串与整数、浮点数和布尔值不同。字符串是一个**序列**（sequence），这意味着它包含按特定顺序排列的多个值。在本章中，我们将了解如何访问组成字符串的值，并使用处理字符串的函数。

我们还将使用正则表达式（regular expression），这是一种在字符串中查找模式并执行搜索和替换等操作的强大工具。

## 字符串是序列

字符串是字符的序列。**字符**（character）可以是一个字母（几乎任何字母表中的）、一个数字、一个标点符号或一个空白字符。

你可以使用方括号运算符从字符串中选择一个字符。以下示例语句从 `fruit` 中选择第 1 个字符并将其赋值给 `letter`：

```auto
let fruit = "banana"
let letter = fruit[1]
```

方括号中的表达式是一个**索引**（index），之所以这样称呼是因为它*指示*要选择序列中的哪个字符。但结果可能与你预期的不同。索引为 `1` 的字母实际上是字符串的第二个字母。索引是从字符串开头算起的偏移量，所以第一个字母的偏移量是 `0`：

```auto
print(fruit[0])
```

你可以把 `'b'` 看作 `'banana'` 的第 0 个字母 -- 读作"零-eth"。

方括号中的索引可以是一个变量：

```auto
let mut i = 1
print(fruit[i])
```

也可以是包含变量和运算符的表达式：

```auto
print(fruit[i + 1])
```

如我们在第 1 章中看到的，我们可以使用内置函数 `len` 来获取字符串的长度：

```auto
let n = fruit.len()
print(n)
```

要获取字符串的最后一个字母，你可能会尝试使用索引 `n`，但这会导致错误，因为 `'banana'` 中没有索引为 6 的字母。因为我们从 `0` 开始计数，六个字母的编号是 `0` 到 `5`。要获取最后一个字符，你必须从 `n` 中减去 `1`：

```auto
print(fruit[n - 1])
```

但有一个更简单的方法。要获取字符串中的最后一个字母，你可以使用负索引，它从末尾向后计数：

```auto
print(fruit[-1])
```

索引 `-1` 选择最后一个字母，`-2` 选择倒数第二个，以此类推。

> **Python 程序员注意：**
>
> Auto 使用 `.len()` 方法来获取字符串长度，而不是 Python 的 `len()` 函数。`a2p` 转译器会自动将 `.len()` 转换为 `len()`。

## 字符串切片

字符串的一个片段称为**切片**（slice）。选择切片类似于选择字符。

```auto
let fruit = "banana"
print(fruit[0..3])
```

运算符 `[n..m]` 返回字符串中从第 `n` 个字符到第 `m` 个字符的部分，包含第一个但不包含第二个。这种行为可能不太直观，但你可以想象索引指向字符*之间*的位置。

如果省略第一个索引，切片从字符串的开头开始：

```auto
print(fruit[..3])
```

如果省略第二个索引，切片到字符串的末尾：

```auto
print(fruit[3..])
```

如果第一个索引大于或等于第二个索引，结果是一个**空字符串**（empty string），用两个引号表示：

```auto
print(fruit[3..3])
```

空字符串不包含任何字符，长度为 0。如果两个索引都省略，切片就是整个字符串的副本：

```auto
print(fruit[..])
```

> **Python 程序员注意：**
>
> Auto 使用 `s[n..m]` 进行切片，而不是 Python 的 `s[n:m]`。`a2p` 转译器会自动将 `..` 转换为 `:`。

<Listing number="8-1" file-name="string_slicing.auto" caption="字符串切片与索引">

```auto
fn main() {
    let fruit = "banana"

    // 索引：访问单个字符
    print("fruit[0]:", fruit[0])
    print("fruit[1]:", fruit[1])
    print("fruit[-1]:", fruit[-1])
    print("fruit[-2]:", fruit[-2])

    // 切片：访问子字符串
    print("fruit[0..3]:", fruit[0..3])
    print("fruit[2..5]:", fruit[2..5])
    print("fruit[..3]:", fruit[..3])
    print("fruit[3..]:", fruit[3..])
    print("fruit[..]:", fruit[..])

    // 空切片
    print("fruit[3..3]:", fruit[3..3])

    // 长度
    print("len(fruit):", fruit.len())
}
```

```python
def main():
    fruit = "banana"

    # 索引：访问单个字符
    print(f"fruit[0]: {fruit[0]}")
    print(f"fruit[1]: {fruit[1]}")
    print(f"fruit[-1]: {fruit[-1]}")
    print(f"fruit[-2]: {fruit[-2]}")

    # 切片：访问子字符串
    print(f"fruit[0:3]: {fruit[0:3]}")
    print(f"fruit[2:5]: {fruit[2:5]}")
    print(f"fruit[:3]: {fruit[:3]}")
    print(f"fruit[3:]: {fruit[3:]}")
    print(f"fruit[:]: {fruit[:]}")

    # 空切片
    print(f"fruit[3:3]: {fruit[3:3]}")

    # 长度
    print(f"len(fruit): {len(fruit)}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

使用 `fruit[0]` 进行索引返回第一个字符，`fruit[-1]` 返回最后一个。使用 `fruit[0..3]` 进行切片返回索引为 0、1 和 2 的字符（上界不包含在内）。省略起始位置（`..3`）表示"从头开始"；省略结束位置（`3..`）表示"到末尾"。空切片 `fruit[3..3]` 返回空字符串，因为起始位置等于结束位置。

## 字符串是不可变的

你可能会想在赋值的左侧使用 `[]` 运算符来改变字符串中的字符，像这样：

```auto
let mut greeting = "Hello, world!"
greeting[0] = "J"  // 错误！
```

这会导致错误，因为字符串是**不可变的**（immutable），这意味着你不能改变已有的字符串。你最多只能创建一个原始字符串的变体：

```auto
let greeting = "Hello, world!"
let new_greeting = "J" + greeting[1..]
print(new_greeting)
```

这个例子将一个新首字母连接到 `greeting` 的切片上。它对原始字符串没有影响：

```auto
print(greeting)
```

## 字符串比较

关系运算符可以用于字符串。要检查两个字符串是否相等，我们可以使用 `==` 运算符：

```auto
let word = "banana"

if word == "banana" {
    print("All right, banana.")
}
```

其他关系运算符对于按字母顺序排列单词很有用：

```auto
fn compare_word(word: str) {
    if word < "banana" {
        print(f"$word comes before banana.")
    } else if word > "banana" {
        print(f"$word comes after banana.")
    } else {
        print("All right, banana.")
    }
}
```

Python（和 Auto）处理大小写字母的方式与人们不同。所有大写字母排在小写字母之前。要解决这个问题，我们可以在比较之前将字符串转换为标准格式，比如全部小写。

## 字符串方法

字符串提供了执行各种有用操作的方法。方法类似于函数 -- 它接受参数并返回一个值 -- 但语法不同。例如，`to_uppercase` 方法接受一个字符串并返回一个全大写的新字符串。

不是使用函数语法 `to_uppercase(word)`，而是使用方法语法 `word.to_uppercase()`：

```auto
let word = "banana"
let new_word = word.to_uppercase()
print(new_word)
```

点运算符指定了方法的名称 `to_uppercase`，以及要应用该方法的字符串名称 `word`。空括号表示此方法不接受参数。

方法调用被称为**调用**（invocation）；在这个例子中，我们会说我们在 `word` 上调用 `to_uppercase`。

<Listing number="8-2" file-name="string_methods.auto" caption="字符串方法">

```auto
fn main() {
    let word = "banana"

    // 大小写转换
    print("upper:", word.to_uppercase())
    print("lower:", "BANANA".to_lowercase())

    // 搜索
    print("find 'a':", word.find("a"))
    print("find 'z':", word.find("z"))
    print("contains 'ana':", word.contains("ana"))
    print("starts with 'ban':", word.starts_with("ban"))
    print("ends with 'na':", word.ends_with("na"))

    // 去除空白
    let spaced = "  hello world  "
    print("strip:", spaced.strip())
    print("len before:", spaced.len())
    print("len after:", spaced.strip().len())

    // 计数出现次数
    print("count 'a':", word.matches("a").count())

    // 替换
    let text = "I like cats and cats like me"
    print("replace:", text.replace("cats", "dogs"))

    // 分割
    let sentence = "pining for the fjords"
    let words = sentence.split(" ")
    print("split:", words)

    // 连接
    let parts = ["hello", "world"]
    print("join:", parts.join(" "))
}
```

```python
def main():
    word = "banana"

    # 大小写转换
    print(f"upper: {word.upper()}")
    print(f"lower: {'BANANA'.lower()}")

    # 搜索
    print(f"find 'a': {word.find('a')}")
    print(f"find 'z': {word.find('z')}")
    print(f"contains 'ana': {'ana' in word}")
    print(f"starts with 'ban': {word.startswith('ban')}")
    print(f"ends with 'na': {word.endswith('na')}")

    # 去除空白
    spaced = "  hello world  "
    print(f"strip: {spaced.strip()}")
    print(f"len before: {len(spaced)}")
    print(f"len after: {len(spaced.strip())}")

    # 计数出现次数
    print(f"count 'a': {word.count('a')}")

    # 替换
    text = "I like cats and cats like me"
    print(f"replace: {text.replace('cats', 'dogs')}")

    # 分割
    sentence = "pining for the fjords"
    words = sentence.split(" ")
    print(f"split: {words}")

    # 连接
    parts = ["hello", "world"]
    print(f"join: {' '.join(parts)}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`to_uppercase()`（Python 中为 `.upper()`）和 `to_lowercase()`（Python 中为 `.lower()`）返回转换大小写后的新字符串。`find()` 返回第一次出现的索引，如果未找到则返回 -1。`strip()` 去除前导和尾随空白。`replace()` 返回替换所有出现位置后的新字符串。`split()` 将字符串拆分为子字符串列表，`join()` 将列表连接为单个字符串。

> **Python 程序员注意：**
>
> Auto 使用 `to_uppercase()` / `to_lowercase()` 代替 Python 的 `.upper()` / `.lower()`。Auto 使用 `starts_with()` / `ends_with()` 代替 Python 的 `.startswith()` / `.endswith()`。`a2p` 转译器会自动转换所有这些方法。

## 写入文件

字符串运算符和方法对于读写文本文件很有用。下面是写入字符串到文件的基本模式：

```auto
let writer = open("output.txt", "w")
writer.write("Hello, world!\n")
writer.close()
```

`open` 函数接受一个可选参数来指定"模式" -- `'w'` 表示以写入模式打开文件。如果文件不存在，将创建新文件；如果文件已存在，内容将被替换。

写入后，我们使用 `close` 方法关闭文件，表示操作完成。

<Listing number="8-3" file-name="file_io.auto" caption="文件 I/O：将字符串写入文件">

```auto
fn main() {
    // 向文件写入行
    let writer = open("output.txt", "w")
    writer.write("First line\n")
    writer.write("Second line\n")
    writer.write("Third line\n")
    writer.close()

    // 从文件读取行
    print("Contents of output.txt:")
    for line in open("output.txt") {
        let stripped = line.strip()
        if stripped.len() > 0 {
            print(stripped)
        }
    }

    // 在文件中查找和替换
    let reader = open("output.txt")
    let writer2 = open("output_replaced.txt", "w")
    for line in reader {
        let new_line = line.replace("line", "row")
        writer2.write(new_line)
    }
    reader.close()
    writer2.close()

    print("\nContents of output_replaced.txt:")
    for line in open("output_replaced.txt") {
        let stripped = line.strip()
        if stripped.len() > 0 {
            print(stripped)
        }
    }
}
```

```python
def main():
    # 向文件写入行
    writer = open("output.txt", "w")
    writer.write("First line\n")
    writer.write("Second line\n")
    writer.write("Third line\n")
    writer.close()

    # 从文件读取行
    print("Contents of output.txt:")
    for line in open("output.txt"):
        stripped = line.strip()
        if len(stripped) > 0:
            print(stripped)

    # 在文件中查找和替换
    reader = open("output.txt")
    writer2 = open("output_replaced.txt", "w")
    for line in reader:
        new_line = line.replace("line", "row")
        writer2.write(new_line)
    reader.close()
    writer2.close()

    print("\nContents of output_replaced.txt:")
    for line in open("output_replaced.txt"):
        stripped = line.strip()
        if len(stripped) > 0:
            print(stripped)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`open("output.txt", "w")` 以写入模式打开文件。`write` 方法将字符串写入文件 -- 注意它不会自动添加换行符，所以我们需要显式包含 `\n`。写入后，`close()` 刷新缓冲区并释放文件句柄。

读取循环使用 `for line in open("output.txt")` 逐行遍历文件。每行包含末尾的换行符，所以我们使用 `strip()` 来去除它。第二部分演示了查找和替换：从一个文件读取，替换子字符串，然后写入新文件。

## 查找和替换

要检查字符串是否包含特定的子字符串，可以使用 `contains` 方法（或 `in` 运算符）。要获取出现次数的总数，可以使用 `matches` 方法结合 `count`：

```auto
let text = "Jonathan went to see Jonathan"
print(text.contains("Jonathan"))
print(text.matches("Jonathan").count())
```

要替换所有出现的子字符串，可以使用 `replace` 方法：

```auto
let new_text = text.replace("Jonathan", "Thomas")
print(new_text)
```

## 正则表达式

如果我们确切知道要查找的字符序列，可以使用 `contains` 来查找，用 `replace` 来替换。但还有另一种工具叫做**正则表达式**（regular expression），它也可以执行这些操作 -- 而且能做更多事情。

让我们从一个简单的例子开始演示。假设我们想查找包含特定单词的所有行。以下是《德古拉》中的一行：

```auto
let text = "I am Dracula; and I bid you welcome, Mr. Harker, to my house."
```

一个名为 `re` 的模块提供了与正则表达式相关的函数。我们可以这样导入它，并使用 `search` 函数来检查模式是否出现在文本中：

```auto
use re

let pattern = "Dracula"
let result = re.search(pattern, text)
```

如果模式出现在文本中，`search` 返回一个包含搜索结果的 `Match` 对象。如果模式没有出现在文本中，`search` 的返回值是 `None`。

我们可以使用竖线字符 `'|'` 来匹配左侧或右侧的任一序列：

```auto
let pattern = "Mina|Murray"
```

特殊字符 `'^'` 匹配字符串的开头，`'$'` 匹配字符串的末尾：

```auto
let pattern = "^Dracula"
let pattern2 = "Harker$"
```

## 字符串替换

我们可以使用 `re` 模块中的 `sub` 函数，它执行**字符串替换**（string substitution）。第一个参数是要查找和替换的模式，第二个是要替换成的字符串，第三个是要搜索的字符串：

```auto
let pattern = "colou?r"
let result = re.sub(pattern, "color", "He liked the colour of the sky")
```

模式中的 `'?'` 表示前一个字符是可选的，所以这个模式匹配 "colour" 或 "color"。

模式中的括号将部分内容分组在一起，使竖线仅应用于组内：

```auto
let pattern = "cent(er|re)"
```

这个模式匹配以 `'cent'` 开头、以 `'er'` 或 `'re'` 结尾的序列。

<Listing number="8-4" file-name="regex.auto" caption="正则表达式：搜索与替换">

```auto
use re

fn main() {
    let text = "I am Dracula; and I bid you welcome, Mr. Harker, to my house."

    // 基本搜索
    let pattern = "Dracula"
    let result = re.search(pattern, text)
    print("Found:", result.group())
    print("Span:", result.span())

    // 搜索失败的情况
    let result2 = re.search("Count", text)
    print("Not found:", result2)

    // 选择匹配：匹配任一名称
    let pattern2 = "Mina|Murray"
    let result3 = re.search(pattern2, "Mina Murray was there")
    print("Alternation:", result3.group())

    // 锚点：字符串的开头和结尾
    let result4 = re.search("^Dracula", "Dracula is here")
    print("Starts with Dracula:", result4.group())

    let result5 = re.search("Harker$", "Mr. Harker")
    print("Ends with Harker:", result5.group())

    // 可选字符 ?
    let pattern3 = "colou?r"
    let result6 = re.sub(pattern3, "color", "The colour of the sky")
    print("Sub colour:", result6)
    let result7 = re.sub(pattern3, "color", "The color of the sky")
    print("Sub color:", result7)

    // 使用括号分组
    let pattern4 = "cent(er|re)"
    let result8 = re.sub(pattern4, "center", "the centre of town")
    print("Sub centre:", result8)
    let result9 = re.sub(pattern4, "center", "the center of town")
    print("Sub center:", result9)

    // findall：查找所有匹配
    let words = "cat bat rat cat hat"
    let result10 = re.findall("cat", words)
    print("findall cat:", result10)
}
```

```python
import re

def main():
    text = "I am Dracula; and I bid you welcome, Mr. Harker, to my house."

    # 基本搜索
    pattern = "Dracula"
    result = re.search(pattern, text)
    print(f"Found: {result.group()}")
    print(f"Span: {result.span()}")

    # 搜索失败的情况
    result2 = re.search("Count", text)
    print(f"Not found: {result2}")

    # 选择匹配：匹配任一名称
    pattern2 = "Mina|Murray"
    result3 = re.search(pattern2, "Mina Murray was there")
    print(f"Alternation: {result3.group()}")

    # 锚点：字符串的开头和结尾
    result4 = re.search("^Dracula", "Dracula is here")
    print(f"Starts with Dracula: {result4.group()}")

    result5 = re.search("Harker$", "Mr. Harker")
    print(f"Ends with Harker: {result5.group()}")

    # 可选字符 ?
    pattern3 = "colou?r"
    result6 = re.sub(pattern3, "color", "The colour of the sky")
    print(f"Sub colour: {result6}")
    result7 = re.sub(pattern3, "color", "The color of the sky")
    print(f"Sub color: {result7}")

    # 使用括号分组
    pattern4 = "cent(er|re)"
    result8 = re.sub(pattern4, "center", "the centre of town")
    print(f"Sub centre: {result8}")
    result9 = re.sub(pattern4, "center", "the center of town")
    print(f"Sub center: {result9}")

    # findall：查找所有匹配
    words = "cat bat rat cat hat"
    result10 = re.findall("cat", words)
    print(f"findall cat: {result10}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`re.search(pattern, text)` 在 `text` 中搜索 `pattern` 的第一次出现，返回一个 `Match` 对象（如果未找到则返回 `None`）。`group()` 方法返回匹配的文本，`span()` 返回起始和结束索引。

模式中的 `|` 运算符表示"或" -- `Mina|Murray` 匹配任一字符串。`^` 锚点匹配字符串开头，`$` 匹配字符串末尾。`?` 使前一个字符变为可选。括号将模式的部分分组在一起。`re.sub(pattern, replacement, text)` 对所有出现的位置执行搜索和替换。`re.findall(pattern, text)` 返回所有非重叠匹配的列表。

> **Python 程序员注意：**
>
> Auto 使用 `use re` 代替 Python 的 `import re`。`a2p` 转译器会自动转换。`re` 模块的函数（`search`、`sub`、`findall`）在两种语言中的工作方式完全相同。

## 调试

在读写文件时，调试可能会比较困难。一个好的调试策略是从文件的一部分开始，让程序正常工作，然后再用整个文件运行。

常见的字符串相关 bug 包括：

- **切片中的差一错误**：对上界是包含还是不包含感到困惑。
- **忘记去除换行符**：从文件读取行时，每行以 `\n` 结尾。
- **索引中的类型错误**：使用浮点数或字符串作为索引而不是整数。
- **比较中的大小写敏感**：`"Banana"` 和 `"banana"` 不相等。

## 术语表

**序列（sequence）：**
一个有序的值集合，其中每个值由一个整数索引标识。

**字符（character）：**
字符串的元素，包括字母、数字和符号。

**索引（index）：**
用于选择序列中某个项（如字符串中的字符）的整数值。索引从 `0` 开始。

**切片（slice）：**
由索引范围指定的字符串的一部分。

**空字符串（empty string）：**
不包含任何字符且长度为 `0` 的字符串。

**对象（object）：**
变量可以引用的东西。对象有类型和值。

**不可变的（immutable）：**
如果一个对象的元素不能被改变，则该对象是不可变的。

**调用（invocation）：**
调用方法的表达式或表达式的一部分。

**正则表达式（regular expression）：**
定义搜索模式的字符序列。

**模式（pattern）：**
指定字符串必须满足的要求才能构成匹配的规则。

**字符串替换（string substitution）：**
用一个字符串替换另一个字符串或其一部分。

## 练习

### 练习

编写一个名为 `is_palindrome` 的函数，接受一个字符串参数，如果它是回文（正读反读都一样）则返回 `true`，否则返回 `false`。例如，`"noon"` 和 `"rotator"` 是回文。

```
is_palindrome("noon")     // 应该为 true
is_palindrome("hello")    // 应该为 false
is_palindrome("a")        // 应该为 true
is_palindrome("")         // 应该为 true
```

### 练习

编写一个名为 `count_vowels` 的函数，接受一个字符串并返回其中元音字母（a、e、i、o、u）的数量，忽略大小写。

```
count_vowels("banana")    // 应该为 3
count_vowels("hello")     // 应该为 2
count_vowels("xyz")       // 应该为 0
```

### 练习

编写一个正则表达式，匹配以大写字母开头并以句号结尾的任何单词。使用 `re.search` 在 `"Hello."`、`"world."` 和 `"Python."` 等字符串上进行测试。

### 练习

编写一个名为 `normalize_text` 的函数，接受一个字符串并返回一个新字符串，其中：
- 所有字母转换为小写
- 去除前导和尾随空白
- 单词之间的多个空格合并为一个空格

```
normalize_text("  Hello,   World!  ")   // 应该为 "hello, world!"
```
