# 文本分析与生成

本章是一个案例研究，使用 Python 的核心数据结构 -- 列表、字典和元组 -- 来探索文本分析和马尔可夫生成：

* 文本分析是一种描述文档中单词之间统计关系的方法，例如一个单词后面跟着另一个单词的概率，以及

* 马尔可夫生成是一种生成与原始文本具有相似单词和短语的新文本的方法。

这些算法与大语言模型（LLM）的某些部分相似，LLM 是聊天机器人的关键组件。

我们将从计算一本书中每个单词出现的次数开始。然后我们将查看单词对，并列出每个单词后面可能出现的单词列表。我们将制作一个简单版本的马尔可夫生成器，作为练习，你将有机会制作一个更通用的版本。

## 唯一单词

作为文本分析的第一步，让我们读一本书 -- 罗伯特·路易斯·史蒂文森的《化身博士》（*The Strange Case Of Dr. Jekyll And Mr. Hyde*）-- 并计算唯一单词的数量。

我们将使用 `for` 循环从文件中逐行读取，用 `split` 将行分成单词。然后，为了跟踪唯一单词，我们将每个单词作为键存储在字典中。

```auto
let mut unique_words: HashMap<str, int> = {}
for line in open(filename) {
    let seq = line.split()
    for word in seq {
        unique_words[word] = 1
    }
}
print(len(unique_words))
```

字典的长度就是唯一单词的数量 -- 按这种计数方式大约有 6000 个。但如果我们检查它们，会发现有些不是有效的单词。

例如，让我们看看 `unique_words` 中最长的单词。我们可以使用 `sorted` 来排序单词，将 `len` 函数作为关键字参数传递，这样单词就按长度排序。

```auto
sorted(unique_words.keys(), key=len)[-5:]
```

切片索引 `[-5:]` 选择排序列表的最后 5 个元素，即最长的单词。

列表包含一些真正较长的单词，如 "circumscription"，以及一些带连字符的单词，如 "chocolate-coloured"。但有些最长的"单词"实际上是由破折号分隔的两个单词。还有一些单词包含标点符号，如句号、感叹号和引号。

所以，在继续之前，让我们先处理破折号和其他标点符号。

## 标点符号

为了识别文本中的单词，我们需要处理两个问题：

* 当行中出现破折号时，我们应该将其替换为空格 -- 这样使用 `split` 时，单词就会被分开。

* 分割单词后，我们可以使用 `strip` 来删除标点符号。

为了处理第一个问题，我们可以使用以下函数，它接受一个字符串，用空格替换破折号，分割字符串，并返回结果列表。

```auto
fn split_line(line: str) -> List<str> {
    return line.replace("\u2014", " ").split()
}
```

注意 `split_line` 只替换破折号（`\u2014`），不替换连字符。

```auto
split_line("coolness\u2014frightened")  // ["coolness", "frightened"]
```

现在，要从每个单词的开头和结尾删除标点符号，我们可以使用 `strip`，但我们需要一个被视为标点符号的字符列表。

以下循环将唯一的标点符号存储在字典中。

```auto
let mut punc_marks: HashMap<str, int> = {}
for line in open(filename) {
    for char in line {
        if not char.is_alphanumeric() and char != " " {
            punc_marks[char] = 1
        }
    }
}
let punctuation = "".join(punc_marks.keys())
print(punctuation)
```

现在我们知道书中有哪些标点符号，可以编写一个函数，接受一个单词，去除开头和结尾的标点，并将其转换为小写。

```auto
fn clean_word(word: str, punctuation: str) -> str {
    return word.strip(punctuation).lower()
}
```

示例：

```auto
clean_word("\u201cBehold!\u201d", punctuation)  // "behold"
```

由于 `strip` 只删除开头和结尾的字符，因此带连字符的单词保持不变。

```auto
clean_word("pocket-handkerchief", punctuation)  // "pocket-handkerchief"
```

<Listing number="12-1" file-name="unique_words.auto" caption="带标点清理的唯一单词计数">

```auto
fn split_line(line: str) -> List<str> {
    return line.replace("\u2014", " ").split()
}

fn clean_word(word: str, punctuation: str) -> str {
    return word.strip(punctuation).lower()
}

fn main() {
    // 来自《化身博士》的模拟文本
    let lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?"
    ]

    // 简单版本（不清理标点）
    let mut unique_words: HashMap<str, int> = {}
    for line in lines {
        let seq = line.split()
        for word in seq {
            unique_words[word] = 1
        }
    }
    print("Unique words (simple):", len(unique_words))

    let sorted_words = sorted(unique_words.keys(), key=len)
    print("Longest words:", sorted_words[-3:])

    // 构建标点集合
    let mut punc_marks: HashMap<str, int> = {}
    for line in lines {
        for char in line {
            if not char.is_alphanumeric() and char != " " {
                punc_marks[char] = 1
            }
        }
    }
    let punctuation = "".join(punc_marks.keys())
    print("Punctuation marks:", punctuation)

    // 清理后的唯一单词计数
    let mut unique_words2: HashMap<str, int> = {}
    for line in lines {
        for word in split_line(line) {
            let cleaned = clean_word(word, punctuation)
            unique_words2[cleaned] = 1
        }
    }
    print("Unique words (cleaned):", len(unique_words2))

    let sorted2 = sorted(unique_words2.keys(), key=len)
    print("Longest cleaned words:", sorted2[-3:])
}
```

```python
def split_line(line):
    return line.replace("\u2014", " ").split()


def clean_word(word, punctuation):
    return word.strip(punctuation).lower()


def main():
    # 来自《化身博士》的模拟文本
    lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?"
    ]

    # 简单版本（不清理标点）
    unique_words = {}
    for line in lines:
        seq = line.split()
        for word in seq:
            unique_words[word] = 1
    print(f"Unique words (simple): {len(unique_words)}")

    sorted_words = sorted(unique_words.keys(), key=len)
    print(f"Longest words: {sorted_words[-3:]}")

    # 构建标点集合
    punc_marks = {}
    for line in lines:
        for char in line:
            if not char.isalnum() and char != " ":
                punc_marks[char] = 1
    punctuation = "".join(punc_marks.keys())
    print(f"Punctuation marks: {punctuation}")

    # 清理后的唯一单词计数
    unique_words2 = {}
    for line in lines:
        for word in split_line(line):
            cleaned = clean_word(word, punctuation)
            unique_words2[cleaned] = 1
    print(f"Unique words (cleaned): {len(unique_words2)}")

    sorted2 = sorted(unique_words2.keys(), key=len)
    print(f"Longest cleaned words: {sorted2[-3:]}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

简单的单词计数方法将每个空白分隔的标记视为一个单词，包括带有附加标点的字符串如 `"Hyde"` 或 `"remarkable!"`。通过检测非字母数字字符并构建标点字符串，`clean_word` 从两端去除标点并将结果转为小写。破折号（`\u2014`）在分割前被替换为空格，因此由破折号连接的单词被正确分开。带连字符的单词如 `"pocket-handkerchief"` 被保留，因为 `strip` 只删除两端的字符。

## 词频

现在让我们看看每个单词被使用了多少次。以下循环计算每个唯一单词的频率。

```auto
let mut word_counter: HashMap<str, int> = {}
for line in open(filename) {
    for word in split_line(line) {
        word = clean_word(word, punctuation)
        if word not in word_counter {
            word_counter[word] = 1
        } else {
            word_counter[word] += 1
        }
    }
}
```

第一次看到某个单词时，我们将其频率初始化为 `1`。如果稍后再次看到相同的单词，我们增加其频率。

要查看哪些单词出现最频繁，我们可以使用 `items` 获取 `word_counter` 中的键值对，并按第二个元素（即频率）排序。

```auto
fn second_element(t: Tuple) -> int {
    return t[1]
}

let items = sorted(word_counter.items(), key=second_element, reverse=true)
```

以下是出现频率最高的五个单词。

```auto
for i in 0..5 {
    let (word, freq) = items[i]
    print(f"$freq\t$word")
}
```

在下一节中，我们将把这个循环封装在一个函数中。我们还将用它来演示一个新特性 -- 可选参数。

## 可选参数

我们使用过带可选参数的内置函数。例如，`round` 有一个可选参数 `ndigits`，指示保留多少位小数。

```auto
round(3.141592653589793, ndigits=3)  // 3.142
```

但不仅仅是内置函数 -- 我们也可以编写带可选参数的函数。例如，以下函数接受两个参数，`word_counter` 和 `num`。

```auto
fn print_most_common(word_counter: HashMap<str, int>, num: int = 5) {
    let items = sorted(word_counter.items(), key=second_element, reverse=true)
    for i in 0..num {
        let (word, freq) = items[i]
        print(f"$freq\t$word")
    }
}
```

第二个参数看起来像赋值语句，但它不是 -- 它是一个可选参数。

如果你用一个参数调用这个函数，`num` 获得**默认值**，即 `5`。

```auto
print_most_common(word_counter)
```

如果你用两个参数调用这个函数，第二个参数将赋值给 `num` 而不是默认值。

```auto
print_most_common(word_counter, 3)
```

在这种情况下，我们说可选参数**覆盖**了默认值。

如果函数既有必需参数又有可选参数，所有必需参数必须排在前面，后面跟着可选参数。

> **Python 程序员注意：**
>
> Auto 可选参数使用与 Python 相同的 `param = value` 语法。`a2p` 转译器会直接转换。

<Listing number="12-2" file-name="word_frequencies.auto" caption="计算并显示词频">

```auto
fn split_line(line: str) -> List<str> {
    return line.replace("\u2014", " ").split()
}

fn clean_word(word: str, punctuation: str) -> str {
    return word.strip(punctuation).lower()
}

fn second_element(t: Tuple) -> int {
    return t[1]
}

fn print_most_common(word_counter: HashMap<str, int>, num: int = 5) {
    let items = sorted(word_counter.items(), key=second_element, reverse=true)
    for i in 0..num {
        let (word, freq) = items[i]
        print(f"$freq\t$word")
    }
}

fn main() {
    let lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?",
        "Dr. Jekyll was a well-known man in the city.",
        "Mr. Hyde was a strange and violent man.",
        "The lawyer Utterson was worried about his friend Dr. Jekyll."
    ]

    let mut punc_marks: HashMap<str, int> = {}
    for line in lines {
        for char in line {
            if not char.is_alphanumeric() and char != " " {
                punc_marks[char] = 1
            }
        }
    }
    let punctuation = "".join(punc_marks.keys())

    let mut word_counter: HashMap<str, int> = {}
    for line in lines {
        for word in split_line(line) {
            let cleaned = clean_word(word, punctuation)
            if cleaned == "" { continue }
            if cleaned not in word_counter {
                word_counter[cleaned] = 1
            } else {
                word_counter[cleaned] += 1
            }
        }
    }

    print("Word frequencies (top 10):")
    print_most_common(word_counter, 10)

    print()
    print("Default number (top 5):")
    print_most_common(word_counter)
}
```

```python
def split_line(line):
    return line.replace("\u2014", " ").split()


def clean_word(word, punctuation):
    return word.strip(punctuation).lower()


def second_element(t):
    return t[1]


def print_most_common(word_counter, num=5):
    items = sorted(word_counter.items(), key=second_element, reverse=True)
    for i in range(num):
        word, freq = items[i]
        print(f"{freq}\t{word}")


def main():
    lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?",
        "Dr. Jekyll was a well-known man in the city.",
        "Mr. Hyde was a strange and violent man.",
        "The lawyer Utterson was worried about his friend Dr. Jekyll."
    ]

    punc_marks = {}
    for line in lines:
        for char in line:
            if not char.isalnum() and char != " ":
                punc_marks[char] = 1
    punctuation = "".join(punc_marks.keys())

    word_counter = {}
    for line in lines:
        for word in split_line(line):
            cleaned = clean_word(word, punctuation)
            if cleaned == "":
                continue
            if cleaned not in word_counter:
                word_counter[cleaned] = 1
            else:
                word_counter[cleaned] += 1

    print("Word frequencies (top 10):")
    print_most_common(word_counter, 10)

    print()
    print("Default number (top 5):")
    print_most_common(word_counter)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`word_counter` 将每个清理后的单词映射到其频率。`second_element` 函数用作排序键，按频率排序。`print_most_common` 函数演示了可选参数：用一个参数调用时使用默认的 `num=5`；用两个参数调用时覆盖默认值。

## 字典减法

假设我们想对一本书进行拼写检查 -- 即找到一个可能拼错的单词列表。一种方法是找出书中不在有效单词列表中的单词。

我们可以将这个问题看作集合减法 -- 即找出一个集合（书中的单词）中不在另一个集合（单词列表中的单词）中的所有单词。

```auto
let mut valid_words: HashMap<str, int> = {}
for word in word_list {
    valid_words[word] = 1
}
```

现在，要识别书中出现但不在单词列表中的单词，我们使用 `subtract`，它接受两个字典作为参数，返回一个新字典，包含第一个字典中所有不在第二个字典中的键。

```auto
fn subtract(d1: HashMap<str, int>, d2: HashMap<str, int>) -> HashMap<str, int> {
    let mut res: HashMap<str, int> = {}
    for key in d1 {
        if key not in d2 {
            res[key] = d1[key]
        }
    }
    return res
}
```

```auto
let diff = subtract(word_counter, valid_words)
print_most_common(diff)
```

最常出现的"拼错"单词大多是人名和一些单字母单词。

如果我们选择只出现一次的单词，它们更有可能是真正的拼写错误。

```auto
let mut singletons: List<str> = []
for (word, freq) in diff.items() {
    if freq == 1 {
        singletons.append(word)
    }
}
```

大多数是有效但不在单词列表中的单词。但也可能有一些真正的拼写错误。

<Listing number="12-3" file-name="dict_subtraction.auto" caption="用于拼写检查的字典减法">

```auto
fn split_line(line: str) -> List<str> {
    return line.replace("\u2014", " ").split()
}

fn clean_word(word: str, punctuation: str) -> str {
    return word.strip(punctuation).lower()
}

fn second_element(t: Tuple) -> int {
    return t[1]
}

fn subtract(d1: HashMap<str, int>, d2: HashMap<str, int>) -> HashMap<str, int> {
    let mut res: HashMap<str, int> = {}
    for key in d1 {
        if key not in d2 {
            res[key] = d1[key]
        }
    }
    return res
}

fn print_most_common(word_counter: HashMap<str, int>, num: int = 5) {
    let items = sorted(word_counter.items(), key=second_element, reverse=true)
    for i in 0..num {
        let (word, freq) = items[i]
        print(f"$freq\t$word")
    }
}

fn main() {
    let lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?",
        "Dr. Jekyll was a well-known man in the city.",
        "Mr. Hyde was a strange and violent man.",
        "The lawyer Utterson was worried about his friend Dr. Jekyll."
    ]

    let mut punc_marks: HashMap<str, int> = {}
    for line in lines {
        for char in line {
            if not char.is_alphanumeric() and char != " " {
                punc_marks[char] = 1
            }
        }
    }
    let punctuation = "".join(punc_marks.keys())

    let mut word_counter: HashMap<str, int> = {}
    for line in lines {
        for word in split_line(line) {
            let cleaned = clean_word(word, punctuation)
            if cleaned == "" { continue }
            if cleaned not in word_counter {
                word_counter[cleaned] = 1
            } else {
                word_counter[cleaned] += 1
            }
        }
    }

    let valid_word_list = [
        "the", "a", "was", "and", "of", "not", "but", "it",
        "strange", "case", "door", "man", "city", "two",
        "friend", "worried", "violent", "his", "about"
    ]
    let mut valid_words: HashMap<str, int> = {}
    for word in valid_word_list {
        valid_words[word] = 1
    }

    let diff = subtract(word_counter, valid_words)
    print("Words possibly misspelled (most common):")
    print_most_common(diff, 8)

    let mut singletons: List<str> = []
    for (word, freq) in diff.items() {
        if freq == 1 {
            singletons.append(word)
        }
    }
    print()
    print(f"Singletons: ${len(singletons)} words")
    print("Sample:", singletons[-5:])
}
```

```python
def split_line(line):
    return line.replace("\u2014", " ").split()


def clean_word(word, punctuation):
    return word.strip(punctuation).lower()


def second_element(t):
    return t[1]


def subtract(d1, d2):
    res = {}
    for key in d1:
        if key not in d2:
            res[key] = d1[key]
    return res


def print_most_common(word_counter, num=5):
    items = sorted(word_counter.items(), key=second_element, reverse=True)
    for i in range(num):
        word, freq = items[i]
        print(f"{freq}\t{word}")


def main():
    lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?",
        "Dr. Jekyll was a well-known man in the city.",
        "Mr. Hyde was a strange and violent man.",
        "The lawyer Utterson was worried about his friend Dr. Jekyll."
    ]

    punc_marks = {}
    for line in lines:
        for char in line:
            if not char.isalnum() and char != " ":
                punc_marks[char] = 1
    punctuation = "".join(punc_marks.keys())

    word_counter = {}
    for line in lines:
        for word in split_line(line):
            cleaned = clean_word(word, punctuation)
            if cleaned == "":
                continue
            if cleaned not in word_counter:
                word_counter[cleaned] = 1
            else:
                word_counter[cleaned] += 1

    valid_word_list = [
        "the", "a", "was", "and", "of", "not", "but", "it",
        "strange", "case", "door", "man", "city", "two",
        "friend", "worried", "violent", "his", "about"
    ]
    valid_words = {}
    for word in valid_word_list:
        valid_words[word] = 1

    diff = subtract(word_counter, valid_words)
    print("Words possibly misspelled (most common):")
    print_most_common(diff, 8)

    singletons = []
    for word, freq in diff.items():
        if freq == 1:
            singletons.append(word)
    print()
    print(f"Singletons: {len(singletons)} words")
    print(f"Sample: {singletons[-5:]}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`subtract` 函数对字典执行类似集合的减法操作：返回一个新字典，包含 `d1` 中但不在 `d2` 中的键，保留 `d1` 中的值。通过从 `word_counter` 中减去 `valid_words`，我们得到文本中出现但不在参考列表中的单词 -- 拼写错误的候选词。单例（只出现一次的单词）尤其可能是真正的错误，而不是专有名词或领域特定术语。

## 随机数

作为马尔可夫文本生成的第一步，接下来我们将从 `word_counter` 中选择一个随机单词序列。但首先让我们谈谈随机性。

给定相同的输入，大多数计算机程序是**确定性的**，这意味着它们每次都生成相同的输出。确定性通常是一件好事，因为我们期望相同的计算产生相同的结果。但对于某些应用，我们希望计算机是不可预测的。

`random` 模块提供了生成伪随机数的函数。我们可以这样导入：

```auto
use random
```

`random` 模块提供了一个名为 `choice` 的函数，从列表中随机选择一个元素，每个元素被选中的概率相同。

```auto
let t = [1, 2, 3]
random.choice(t)  // 例如 2
```

`random` 模块还提供了 `choices` 函数，它接受权重作为可选参数。

```auto
random.choices(words, weights=weights)
```

它还接受另一个可选参数 `k`，指定要选择的单词数量。

```auto
let random_words = random.choices(words, weights=weights, k=6)
random_words
```

如果你从书中随机选择单词，你会感受到词汇的风格，但一系列随机单词很少有实际意义，因为连续单词之间没有关系。

## 二元组

现在我们不再一次看一个单词，而是看两个单词的序列，称为**二元组**（bigram）。三个单词的序列称为**三元组**（trigram），具有未指定数量单词的序列称为 **n-元组**（n-gram）。

让我们编写一个程序来查找书中所有二元组及其出现次数。为了存储结果，我们使用一个字典，键是表示二元组的字符串元组，值是表示频率的整数。

当我们浏览书籍时，必须跟踪每对连续的单词。我们使用一个名为 `window` 的列表，因为它像一个在文本上滑动的窗口，一次只显示两个单词。

```auto
let mut window: List<str> = []

fn process_word(word: str) {
    window.append(word)
    if len(window) == 2 {
        count_bigram(window)
        window.pop(0)
    }
}
```

第一次调用此函数时，它将给定的单词追加到 `window`。由于只有一个单词，我们还没有二元组。第二次调用时，它追加第二个单词并调用 `count_bigram`。然后使用 `pop` 删除窗口中的第一个单词，为新单词腾出空间。

## 马尔可夫分析

我们可以使用马尔可夫链文本分析做得更好，它计算文本中每个单词后面可以跟哪些单词的列表。例如，我们将分析 Monty Python 歌曲《Eric, the Half a Bee》的歌词：

```auto
let song = [
    "Half", "a", "bee", "philosophically,",
    "Must", "ipso", "facto,", "half", "not", "be.",
    "But", "half", "the", "bee", "has", "got", "to", "be",
    "Vis", "a", "vis,", "its", "entity.", "D'you", "see?"
]
```

为了存储结果，我们使用一个字典，将每个单词映射到它后面的单词列表。

```auto
let mut successor_map: HashMap<str, List<str>> = {}
```

以下函数封装了将二元组添加到后继映射的逻辑。

```auto
fn add_bigram(successor_map: HashMap<str, List<str>>, bigram: List<str>) {
    let first = bigram[0]
    let second = bigram[1]

    if first not in successor_map:
        successor_map[first] = [second]
    else:
        successor_map[first].append(second)
}
```

如果同一个二元组出现多次，第二个单词会被多次添加到列表中。这样，`successor_map` 就跟踪了每个后继出现的次数。

## 生成文本

我们可以利用上一节的结果来生成与原文具有相同连续单词关系的新文本。工作原理如下：

* 从文本中出现的任何单词开始，查找其可能的后继单词并随机选择一个。

* 然后，使用选定的单词，查找其可能的后继单词，并随机选择一个。

我们可以重复此过程来生成任意数量的单词。

<Listing number="12-4" file-name="markov_text.auto" caption="简单马尔可夫文本生成">

```auto
use random

fn split_line(line: str) -> List<str> {
    return line.replace("\u2014", " ").split()
}

fn clean_word(word: str, punctuation: str) -> str {
    return word.strip(punctuation).lower()
}

fn add_bigram(successor_map: HashMap<str, List<str>>, bigram: List<str>) {
    let first = bigram[0]
    let second = bigram[1]

    if first not in successor_map {
        successor_map[first] = [second]
    } else:
        successor_map[first].append(second)
    }
}

fn main() {
    let song = [
        "Half", "a", "bee", "philosophically,",
        "Must", "ipso", "facto,", "half", "not", "be.",
        "But", "half", "the", "bee", "has", "got", "to", "be",
        "Vis", "a", "vis,", "its", "entity.", "D'you", "see?"
    ]

    let mut punctuation: HashMap<str, int> = {}
    let punc_chars = ",.'"
    for c in punc_chars {
        punctuation[c] = 1
    }
    let punc = "".join(punctuation.keys())

    // 从歌曲构建后继映射
    let mut successor_map: HashMap<str, List<str>> = {}
    let mut window: List<str> = []

    for string in song {
        let word = clean_word(string, punc)
        if word == "" { continue }
        window.append(word)

        if len(window) == 2 {
            add_bigram(successor_map, window)
            window.pop(0)
        }
    }

    print("Successor map from song:")
    for (key, value) in successor_map.items() {
        print(f"  '$key' -> $value")
    }

    // 马尔可夫文本生成
    random.seed(42)
    let start_word = "half"
    print()
    print(f"Starting word: '$start_word'")
    print("Generated text:")

    let mut word = start_word
    let mut result: List<str> = [start_word]

    for i in 0..15 {
        if word not in successor_map {
            break
        }
        let successors = successor_map[word]
        word = random.choice(successors)
        result.append(word)
    }

    print(" ".join(result))
}
```

```python
import random


def split_line(line):
    return line.replace("\u2014", " ").split()


def clean_word(word, punctuation):
    return word.strip(punctuation).lower()


def add_bigram(successor_map, bigram):
    first = bigram[0]
    second = bigram[1]

    if first not in successor_map:
        successor_map[first] = [second]
    else:
        successor_map[first].append(second)


def main():
    song = [
        "Half", "a", "bee", "philosophically,",
        "Must", "ipso", "facto,", "half", "not", "be.",
        "But", "half", "the", "bee", "has", "got", "to", "be",
        "Vis", "a", "vis,", "its", "entity.", "D'you", "see?"
    ]

    punctuation = {}
    punc_chars = ",.'"
    for c in punc_chars:
        punctuation[c] = 1
    punc = "".join(punctuation.keys())

    # 从歌曲构建后继映射
    successor_map = {}
    window = []

    for string in song:
        word = clean_word(string, punc)
        if word == "":
            continue
        window.append(word)

        if len(window) == 2:
            add_bigram(successor_map, window)
            window.pop(0)

    print("Successor map from song:")
    for key, value in successor_map.items():
        print(f"  '{key}' -> {value}")

    # 马尔可夫文本生成
    random.seed(42)
    start_word = "half"
    print()
    print(f"Starting word: '{start_word}'")
    print("Generated text:")

    word = start_word
    result = [start_word]

    for i in range(16):
        if word not in successor_map:
            break
        successors = successor_map[word]
        word = random.choice(successors)
        result.append(word)

    print(" ".join(result))


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

马尔可夫链生成器分两个阶段工作。首先，它使用大小为 2 的滑动窗口扫描文本来构建**后继映射**（也称为转移表）。每对连续的单词成为一个二元组；第一个单词存储为键，第二个单词追加到其可能后继的列表中。如果同一个二元组出现多次，后继会在列表中出现多次，这自然地将选择偏向更频繁的转移。

在生成阶段，算法从给定的单词开始，在映射中查找其后继，并使用 `random.choice` 随机选择一个。选定的单词成为新的当前单词，过程重复。因为后继列表编码了连续单词之间的统计关系，生成的文本保留了原文的一些结构和风格。

我们可以通过在 `successor_map` 中使用多个单词作为键来做得更好。例如，我们可以创建一个字典，将每个二元组（或三元组）映射到后面的单词列表。作为练习，你将有机会实现这个分析并查看结果。

## 调试

此时我们正在编写更复杂的程序，你可能会发现花在调试上的时间更多了。如果你遇到一个棘手的 bug，这里有一些方法可以尝试：

* **阅读**：检查你的代码，读给自己听，确认它是否表达了你的意图。

* **运行**：通过做更改和运行不同版本来实验。通常，如果你在程序中正确的地方显示正确的内容，问题就会变得明显，但有时你需要搭建脚手架。

* **思考**：花一些时间想一想！是什么类型的错误：语法、运行时还是语义错误？你可以从错误消息或程序输出中获得什么信息？

* **橡皮鸭调试**：如果你向别人解释问题，有时你会在问完之前就找到答案。通常你不需要另一个人；你可以对着一个橡皮鸭说话。这就是著名的**橡皮鸭调试**策略的起源。

* **撤退**：在某些时候，最好的做法是后退 -- 撤销最近的更改 -- 直到你得到一个能运行的程序。然后你可以开始重建。

* **休息**：如果你给大脑一个休息的机会，有时它会为你找到问题。

初学者有时会陷入其中一项活动而忘记其他的。每项活动都有自己的失败模式。例如，阅读代码适用于拼写错误，但不适用于概念性误解。

你必须花时间思考。调试就像实验科学。你应该至少有一个关于问题是什么的假设。如果有两种或多种可能性，试着想一个能排除其中之一的测试。

找到一个困难的 bug 需要阅读、运行、思考、撤退，有时还需要休息。如果你在某项活动中卡住了，试试其他的。

## 术语表

**默认值（default value）：**
如果没有提供参数，则赋给参数的值。

**覆盖（override）：**
用参数替换默认值。

**确定性的（deterministic）：**
确定性程序在给定相同输入的情况下，每次运行都执行相同的操作。

**伪随机的（pseudorandom）：**
伪随机数序列看起来是随机的，但是由确定性程序生成的。

**二元组（bigram）：**
两个元素的序列，通常是单词。

**三元组（trigram）：**
三个元素的序列。

**n-元组（n-gram）：**
未指定数量元素的序列。

**马尔可夫分析（Markov analysis）：**
一种分析，计算序列中每个元素后面可以跟哪些元素的集合。

**后继映射（successor map）：**
一个将每个元素映射到可能后继列表的字典。

**橡皮鸭调试（rubber duck debugging）：**
通过向无生命物体大声解释问题来调试的方法。

## 练习

### 练习

编写一个函数来计算每个三元组（三个单词的序列）出现的次数。如果你用《化身博士》的文本测试你的函数，你应该发现最常见的三元组是 "said the lawyer"。

提示：编写一个名为 `count_trigram` 的函数，类似于 `count_bigram`。然后编写一个名为 `process_word_trigram` 的函数，类似于 `process_word_bigram`，但使用大小为 3 的窗口。

### 练习

现在让我们实现马尔可夫链文本分析，将每个二元组映射到可能后继的列表。

从 `add_bigram` 开始，编写一个名为 `add_trigram` 的函数，接受三个单词的列表，在 `successor_map` 中添加或更新一个项，使用前两个单词作为键，第三个单词作为可能的后继。

然后编写一个函数 `process_word_trigram`，使用大小为 3 的窗口并调用 `add_trigram`。

### 练习

使用上一个练习中的 `successor_map`（将二元组映射到后继列表），编写一个循环生成 50 个单词的文本：

1. 从 `successor_map` 中随机选择一个键。

2. 查找可以跟在该二元组后面的单词列表。

3. 随机选择一个并打印。

4. 用当前二元组的第二个单词和选定的后继构成新的二元组。

5. 重复。

如果一切正常，你应该发现生成的文本在风格上与原文明显相似，有些短语是有意义的，但文本可能会从一个主题跳到另一个主题。
