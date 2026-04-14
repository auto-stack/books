# 日常类型

本章介绍你在 Auto 中最常使用的日常类型，以及它们如何映射到对应的 TypeScript 类型。

## 基本类型：`string`、`number` 和 `boolean`

TypeScript 有三个核心基本类型：`string`、`number` 和 `boolean`。Auto 为每个
类型提供了更简短的别名：

| TypeScript | Auto   |
|-----------|--------|
| `string`  | `str`  |
| `number`  | `int`, `float` |
| `boolean` | `bool` |

Auto 区分 `int` 和 `float`，但两者都会转译为 TypeScript 的 `number` 类型，
因为 TypeScript 在运行时不区分整数和浮点数。

<Listing number="02-01" file="listings/ch02/listing-02-01/main.at" caption="基本类型">

```auto
fn main() {
    let name = "Alice"
    let age = 25
    let is_active = true
    print(name)
    print(age)
    print(is_active)
}
```

```typescript
function main(): void {
    const name: string = "Alice";
    const age: number = 25;
    const is_active: boolean = true;
    console.log(name);
    console.log(age);
    console.log(is_active);
}

main();
```

</Listing>

如你所见，Auto 会自动推断类型。`"Alice"` 被推断为 `str`，`25` 被推断为
`int`，`true` 被推断为 `bool`。你也可以显式标注类型：

```auto
let name str = "Alice"
let age int = 25
let is_active bool = true
```

注意 Auto 使用空格（而非冒号）分隔变量名和类型标注。

## 数组

在 TypeScript 中，你使用 `number[]` 或 `string[]` 来指定数组类型。在 Auto
中，语法是反过来的：你写 `[]int` 或 `[]str`。这遵循了 Auto 的一般模式，
将类型放在名称之后。

<Listing number="02-02" file="listings/ch02/listing-02-02/main.at" caption="数组">

```auto
fn main() {
    let nums = [1, 2, 3]
    let names = ["Alice", "Bob", "Charlie"]
    for n in nums {
        print(n)
    }
    for name in names {
        print(name)
    }
}
```

```typescript
function main(): void {
    const nums: number[] = [1, 2, 3];
    const names: string[] = ["Alice", "Bob", "Charlie"];
    for (const n of nums) {
        console.log(n);
    }
    for (const name of names) {
        console.log(name);
    }
}

main();
```

</Listing>

Auto 的 `for ... in` 遍历元素（而非索引），映射到 TypeScript 的
`for ... of` 循环。如果你需要索引，使用 `enumerate` 函数：

```auto
for (i, name) in enumerate(names) {
    print(f"${i}: ${name}")
}
```

## 函数

Auto 中的函数使用 `fn` 关键字。参数类型用空格（而非冒号）标注，返回类型跟
在参数列表之后。

<Listing number="02-03" file="listings/ch02/listing-02-03/main.at" caption="函数类型标注">

```auto
fn add(a int, b int) int {
    return a + b
}

fn greet(name str) {
    print(f"Hello, ${name}!")
}

fn main() {
    let result = add(5, 3)
    print(result)
    greet("Alice")
}
```

```typescript
function add(a: number, b: number): number {
    return a + b;
}

function greet(name: string): void {
    console.log(`Hello, ${name}!`);
}

function main(): void {
    const result = add(5, 3);
    console.log(result);
    greet("Alice");
}

main();
```

</Listing>

没有显式返回类型的函数会被自动推断。如果函数不返回值，转译器会在 TypeScript
输出中生成 `: void`。

对于函数类型表达式，Auto 使用简洁的箭头语法：

| TypeScript | Auto |
|-----------|------|
| `(a: number, b: number) => number` | `(a int, b int) => int` |
| `(name: string) => void` | `(name str) =>` |

当返回类型为 `void` 时，你可以在 Auto 中完全省略。

## 对象类型

在 TypeScript 中，你使用接口或内联类型如 `{ name: string; age: number }` 来
定义对象形状。Auto 使用 `type` 关键字定义命名的对象类型及其字段：

<Listing number="02-04" file="listings/ch02/listing-02-04/main.at" caption="对象类型">

```auto
type User {
    name str
    age int
}

fn main() {
    let user = User("Alice", 30)
    print(f"${user.name} is ${user.age} years old")
}
```

```typescript
class User {
    name: string;
    age: number;

    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }
}

function main(): void {
    const user = User("Alice", 30);
    console.log(`${user.name} is ${user.age} years old`);
}

main();
```

</Listing>

Auto 的 `type Name { fields }` 转译为带有构造函数的 TypeScript `class`。构造
函数参数按位置对应，与字段声明顺序一致。这为你提供了一种简洁的方式来创建
类型化对象，而无需样板代码。

对于结构化契约（类似 TypeScript 的 `interface`），Auto 提供了 `spec` 关键字，
这将在后面的章节中介绍。

## 使用枚举的可空类型

TypeScript 使用 `T | null` 来表示可能缺失的值。在 Auto 中，你可以使用带标签
变体的枚举来建模可空类型。这受到 Rust 的 `Option<T>` 启发，并在编译时提供
穷尽模式匹配。

<Listing number="02-05" file="listings/ch02/listing-02-05/main.at" caption="使用枚举的可空类型">

```auto
enum MaybeId {
    Just int
    Nothing
}

fn process_id(id MaybeId) {
    is id {
        MaybeId.Just(n) => print("ID:", n)
        MaybeId.Nothing => print("No ID provided")
    }
}

fn main() {
    let a = MaybeId.Just(42)
    process_id(a)
    process_id(MaybeId.Nothing)
}
```

```typescript
type MaybeId =
    { _tag: "Just", value: number }
    | { _tag: "Nothing", value: void };

const MaybeId = {
    Just: (value: number) => ({ _tag: "Just", value }),
    Nothing: (value: void) => ({ _tag: "Nothing", value })
};


function process_id(id: MaybeId): void {
    switch (id) {
        case MaybeId.Just(n):
            console.log("ID:", n);
            break;
        case MaybeId.Nothing(_):
            console.log("No ID provided");
            break;
    }
}

function main(): void {
    const a = MaybeId.Just(42);
    process_id(a);
    process_id(MaybeId.Nothing);
}

main();
```

</Listing>

枚举 `MaybeId` 转译为 TypeScript 中的可辨识联合类型。每个变体变成一个
`{ _tag: "...", value: T }` 对象，枚举命名空间提供类似 `MaybeId.Just(42)`
的构造函数。`is` 表达式转译为对 `_tag` 字段进行模式匹配的 `switch` 语句。

这种方式为你提供穷尽匹配——编译器确保你处理了每种情况。在 TypeScript 中，
你通常会使用 `T | null`，但 Auto 的枚举方法更安全、更明确。

对于基于字符串的可空类型，你可以定义类似的枚举：

```auto
enum MaybeName {
    Just str
    Nothing
}
```

注意：Auto 将 `Some` 和 `None` 保留为关键字。请使用 `Just` 和 `Nothing`
（或任何其他非关键字名称）作为你的枚举变体。

## 可选参数

TypeScript 支持使用 `?` 标记可选参数：`function greet(name: string, greeting?:
string)`。Auto 在参数名前使用相同的 `?` 前缀来标记可选参数。

<Listing number="02-06" file="listings/ch02/listing-02-06/main.at" caption="可选函数参数">

```auto
fn greet(name str, greeting? str) {
    if greeting {
        print(f"${greeting}, ${name}!")
    } else {
        print(f"Hello, ${name}!")
    }
}

fn main() {
    greet("Alice")
    greet("Bob", "Hi")
}
```

```typescript
function greet(name: string, greeting: string | null): void {
    if (greeting) {
        console.log(`${greeting}, ${name}!`);
    } else {
        console.log(`Hello, ${name}!`);
    }
}

function main(): void {
    greet("Alice");
    greet("Bob", "Hi");
}

main();
```

</Listing>

Auto 中的可选参数直接转译为 TypeScript 的可选参数（`param?: T`）。`if greeting`
检查有效是因为 Auto 将 `null` 和 `undefined` 视为假值，与 TypeScript 相同。

## 类型别名

TypeScript 的 `type` 关键字为现有类型创建别名。Auto 支持相同的概念，语法更
简洁：

```auto
type ID = int
type Name = str
type UserList = []User
```

这直接转译为：

```typescript
type ID = number;
type Name = string;
type UserList = User[];
```

类型别名对于为复杂类型赋予有意义的名称以及保持代码自文档化非常有用。

## 快速参考

| TypeScript | Auto | 描述 |
|-----------|------|------|
| `string` | `str` | 文本 |
| `number` | `int`, `float` | 数值 |
| `boolean` | `bool` | 布尔值 |
| `T[]` | `[]T` | 数组 |
| `T \| null` | 带 `Just`/`Nothing` 的枚举 | 可空类型 |
| `{ name: string }` | `type Obj { name str }` | 对象 |
| `(a: number) => void` | `(a int) =>` | 函数类型 |

## TypeScript 独有功能

以下 TypeScript 功能在 Auto 中没有直接对应的等价物。

### `any` 类型

TypeScript 的 `any` 类型完全禁用类型检查。Auto 没有 `any` 类型 -- 该语言被
设计为类型安全的。如果你需要处理动态类型数据，请使用显式的可空类型或联合
类型代替。

```typescript
// 仅限 TypeScript
let data: any = JSON.parse(input);
```

### 元组类型

TypeScript 支持具有固定长度和类型化位置的数组，称为元组：

```typescript
// 仅限 TypeScript
let pair: [number, string] = [1, "hello"];
```

Auto 没有元组类型。请使用带有字段的命名 `type` 代替：

```auto
type Pair {
    first int
    second str
}

let pair = Pair(1, "hello")
```

### 字面量类型

TypeScript 允许你将特定值作为类型使用：

```typescript
// 仅限 TypeScript
let direction: "left" | "right" = "left";
```

Auto 不支持字面量类型。请使用 `enum` 或带验证的 `str` 代替：

```auto
enum Direction {
    Left
    Right
}

let direction = Direction::Left
```
