# 控制流

程序按顺序执行语句，从上到下。控制流语句改变这个顺序：让你在路径之间选择、重复代码块，或在多个选项中选择。本章涵盖三种主要的控制流机制——条件、迭代和多路选择——在 C 和 Auto 两个语言中。

## 3.1 条件执行

最基本的控制流构造是条件：根据条件决定做这个还是做那个。

### C 的 if/else

在 C 中，`if` 求值一个表达式。如果结果非零，执行第一个分支。否则，执行 `else` 分支（如果有的话）：

```c
if (x > 0) {
    printf("positive\n");
} else if (x < 0) {
    printf("negative\n");
} else {
    printf("zero\n");
}
```

对于单语句分支，循环体周围的花括号是可选的，但现代 C 风格总是使用它们。这可以防止一类 bug：维护编辑添加第二条语句但忘记加花括号。

### Auto 的 if/else

Auto 使用相同的逻辑结构，但条件不需要括号：

```auto
if x > 0 {
    print("positive")
} else if x < 0 {
    print("negative")
} else {
    print("zero")
}
```

Auto 要求所有分支都使用花括号。没有"可选花括号"规则。这完全消除了悬空 else 歧义和忘记单语句花括号的 bug。

### 真与假

在 C 中，真假很简单：零为假，其他一切为真。这适用于所有标量类型：

```c
if (42)        // 真
if (0)         // 假
if (3.14)      // 真
if (0.0)       // 假
if (ptr)       // 如果 ptr 不是 NULL 则为真
if (!ptr)      // 如果 ptr 是 NULL 则为真
```

Auto 继承了相同的模型。非零值为真，零为假。`bool` 类型提供显式的布尔值 `true` 和 `false`，但任何条件表达式的工作方式与 C 相同。

> **C 深潜：** 在 C 中，*每个*标量值都有真值解释：零为假，非零为真。这意味着 `if (ptr)`、`if (count)` 和 `if (difference != 0)` 都是有效的条件。现代 C 的建议是明确的："不要与 0、false 或 null 比较。"但这是一种风格选择，许多 C 程序员更喜欢显式比较以增加清晰度。Auto 不改变这一点——相同的真值模型适用。

<Listing name="条件执行" file="listings/ch03/listing-03-01">

这个 Listing 定义了一个 `classify` 函数，根据数字是正数、负数还是零返回字符串。main 函数用五个值的数组测试它。

a2c 转译器将 Auto 函数映射为 C，如下所示：

```c
const char* classify(int n) {
    if (n > 0) {
        return "positive";
    } else if (n < 0) {
        return "negative";
    } else {
        return "zero";
    }
}
```

注意 Auto 的隐式返回（每个分支的最后一个表达式成为返回值）如何映射到 C 的显式 `return` 语句。每个分支都是字符串字面量，所以转译器在前面插入了 `return`。

> **要点：** 条件在路径之间做选择。C 要求条件加括号；Auto 不需要。两者以相同方式求值真值：非零为真，零为假。

## 3.2 迭代

迭代让你重复执行一段代码。C 提供三种循环构造；Auto 提供两种。

### For 循环

C 的 `for` 循环有三个组成部分：初始化、条件和递增：

```c
for (int i = 0; i < 10; i++) {
    printf("%d\n", i);
}
```

Auto 用基于范围的形式替代：

```auto
for i in 0..10 {
    print(i)
}
```

范围 `0..10` 表示"从 0 开始，到但不包含 10。"a2c 转译器生成 `for (int i = 0; i < 10; i++)`。

你也可以使用非零的起始值：

```auto
for i in 5..15 {
    // i 从 5 到 14
}
```

这变成 `for (int i = 5; i < 15; i++)`。

### While 循环

C 和 Auto 都有 `while` 循环：

```c
// C
while (countdown > 0) {
    countdown = countdown - 1;
}
```

```auto
// Auto
while countdown > 0 {
    countdown = countdown - 1
}
```

语义完全相同：检查条件，执行循环体，重复。

`while` 是当你预先不知道迭代次数时的正确选择——例如，等待用户输入、读取到文件末尾，或收敛到解。

### 循环变量和作用域

在 C 中，在 `for` 初始化器中声明的变量的作用域限于循环：

```c
for (int i = 0; i < 10; i++) {
    // i 在这里可见
}
// i 在这里不可见
```

Auto 基于范围的 `for` 工作方式相同。循环变量 `i` 为循环而创建，循环后不可访问：

```auto
for i in 0..10 {
    // i 在这里可见
}
// i 在这里不可见
```

<Listing name="迭代" file="listings/ch03/listing-03-02">

这个 Listing 演示了三种迭代模式：

1. **向上计数：** 使用带范围的 `for` 循环求 0 到 10 的和。
2. **倒计时：** 使用 `while` 循环递减变量直到为零。
3. **斐波那契：** 使用带可变状态的 `for` 循环生成前 10 个斐波那契数。

斐波那契示例特别有启发性。它用 `var` 声明 `a` 和 `b`，因为它们在每次迭代中改变；用 `let` 声明 `temp`，因为它只在循环体内作为临时变量使用。

> **C 深潜：** C 还有 `do...while` 循环，在循环体*之后*检查条件，保证至少执行一次。Auto 不提供 `do...while`，因为在实践中，先检查条件的普通 `while` 循环覆盖了大多数用例，少数例外可以重构。`do...while` 也是 C 中少数需要在右花括号后加分号的地方：`do { ... } while (cond);`。

> **要点：** Auto 的 `for i in 0..n` 替代 C 的 `for (int i = 0; i < n; i++)`。Auto 的 `while` 直接对应 C 的 `while`。两者都是对相同机器代码的零开销抽象。

## 3.3 多路选择

当你需要根据单个值在多个选项中选择时，`switch`（C）或 `is`（Auto）比一串 `if/else if` 块更清晰。

### C 的 switch

C 的 `switch` 语句跳转到匹配的 `case` 标签：

```c
switch (day) {
    case 1: printf("Monday\n"); break;
    case 2: printf("Tuesday\n"); break;
    case 3: printf("Wednesday\n"); break;
    case 4: printf("Thursday\n"); break;
    case 5: printf("Friday\n"); break;
    case 6: printf("Weekend\n"); break;
    case 7: printf("Weekend\n"); break;
    default: printf("Invalid\n"); break;
}
```

每个 case 以 `break` 结束。没有 `break`，执行会贯穿到下一个 case。这种贯穿行为是 C 最受批评的特性之一。

### Auto 的 is

Auto 的 `is` 构造提供无贯穿的模式匹配：

```auto
is day {
    1 => "Monday"
    2 => "Tuesday"
    3 => "Wednesday"
    4 => "Thursday"
    5 => "Friday"
    6 => "Weekend"
    7 => "Weekend"
    else => "Invalid"
}
```

每个分支都是独立的表达式。没有贯穿。a2c 转译器为每个 case 生成带 `break`（或 `return`）的 `switch`。

### 为什么 is 比 switch 更好

`is` 构造修复了 C 的 `switch` 的三个问题：

1. **无贯穿。** 你不可能忘记 `break`，因为没有 `break` 可忘。
2. **表达式语义。** 整个 `is` 块是一个产生值的表达式。你可以赋值它：`let result str = is day { ... }`。
3. **穷尽性。** `else =>` 分支是必需的，强制你显式处理默认情况。

> **C 深潜：** C 的 `switch` 有*贯穿（fall-through）*：执行从匹配的 case 继续到下一个 case，除非遇到 `break` 语句。这是 C 最臭名昭著的特性之一。忘记 `break` 是经典的 bug。现代 C 风格通常用 `/* fall through */` 注释或 `[[fallthrough]]` 属性（C23）标注有意的贯穿。

<Listing name="多路选择" file="listings/ch03/listing-03-03">

Listing 使用 `is` 将日期数字映射到日期名称。转译器将其转换为干净的 `switch` 语句：

```c
const char* day_type(int day) {
    switch (day) {
        case 1: return "Monday";
        case 2: return "Tuesday";
        case 3: return "Wednesday";
        case 4: return "Thursday";
        case 5: return "Friday";
        case 6: return "Weekend";
        case 7: return "Weekend";
        default: return "Invalid";
    }
}
```

注意：

- 每个 case 有显式的 `return`——不可能贯穿。
- `else` 分支映射到 `default`。
- 生成的 C 是惯用的且安全的。

> **要点：** 使用 `is` 进行多路分派。它在设计上消除了贯穿 bug，并在输出中生成干净的 `switch` 语句。

## 快速参考

| 构造 | C | Auto |
|---|---|---|
| 条件 | `if (cond) { } else { }` | `if cond { } else { }` |
| Else-if 链 | `else if (cond)` | `else if cond` |
| 必需花括号 | 否（但推荐） | 是（强制） |
| For 循环 | `for (int i = 0; i < n; i++)` | `for i in 0..n` |
| While 循环 | `while (cond) { }` | `while cond { }` |
| Do-while | `do { } while (cond);` | （不提供） |
| Switch | `switch (x) { case ... }` | `is x { ... }` |
| 默认分支 | `default:` | `else =>` |
| 贯穿 | 可能（需要 `break`） | 不可能 |
| 真值 | 非零 = 真 | 非零 = 真 |
