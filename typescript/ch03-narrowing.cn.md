# 类型收窄

TypeScript 使用*收窄*（narrowing）在条件分支中细化值的类型。Auto 使用
`is` 表达式进行模式匹配，提供了更结构化的方式来处理同一问题。

## 使用 `is` 进行模式匹配

Auto 的 `is` 表达式检查值并与模式匹配。当模式匹配时，执行对应的分支。
这是 Auto 收窄类型的主要机制——它用统一的语法替代了 TypeScript 的
`typeof` 检查、`instanceof` 检查和可辨识联合 `switch`。

<Listing number="03-01" file="listings/ch03/listing-03-01/main.at" caption="使用 is 进行模式匹配">

```auto
enum Value {
    Num int
    Text int
}

fn describe(value Value) {
    is value {
        Value.Num(n) => print("It's a number:", n)
        Value.Text(t) => print("It's text:", t)
    }
}

fn main() {
    describe(Value.Num(42))
    describe(Value.Text(99))
}
```

```typescript
type Value =
    { _tag: "Num", value: number }
    | { _tag: "Text", value: number };

const Value = {
    Num: (value: number) => ({ _tag: "Num", value }),
    Text: (value: number) => ({ _tag: "Text", value })
};


function describe(value: Value): void {
    switch (value) {
        case Value.Num(n):
            console.log("It's a number:", n);
            break;
        case Value.Text(t):
            console.log("It's text:", t);
            break;
    }
}

function main(): void {
    describe(Value.Num(42));
    describe(Value.Text(99));
}

main();
```

</Listing>

`is` 表达式转译为 TypeScript 的 `switch` 语句。每个模式绑定变量（如 `n`
和 `t`），这些变量在分支体内可用。在 TypeScript 中，等价的做法是
对可辨识联合的 `_tag` 字段使用 `switch`。

## 真值收窄

Auto 将 `0`、空字符串、`null` 和 `false` 视为假值——与 TypeScript 相同。
你可以直接在 `if` 条件中使用任何值：

<Listing number="03-02" file="listings/ch03/listing-03-02/main.at" caption="真值收窄">

```auto
fn process_count(count int) {
    if count {
        print("Count is non-zero:", count)
    } else {
        print("Count is zero")
    }
}

fn main() {
    process_count(5)
    process_count(0)
}
```

```typescript
function process_count(count: number): void {
    if (count) {
        console.log("Count is non-zero:", count);
    } else {
        console.log("Count is zero");
    }
}

function main(): void {
    process_count(5);
    process_count(0);
}

main();
```

</Listing>

这在 Auto 和 TypeScript 中行为完全相同。`if count` 条件隐式收窄类型
——在 `if` 分支内，编译器知道 `count` 为真值。

## 可辨识联合

TypeScript 的可辨识联合使用公共属性（如 `kind`）来收窄类型。Auto 使用
带标签变体的枚举，自动转译为可辨识联合：

<Listing number="03-03" file="listings/ch03/listing-03-03/main.at" caption="使用枚举的可辨识联合">

```auto
enum Shape {
    Circle float
    Square float
}

fn area(shape Shape) {
    is shape {
        Shape.Circle(r) => print("Circle area:", 3.14 * r * r)
        Shape.Rectangle(w) => print("Rectangle area:", w * w)
    }
}

fn main() {
    let c = Shape.Circle(5.0)
    let s = Shape.Square(4.0)
    area(c)
    area(s)
}
```

```typescript
type Shape =
    { _tag: "Circle", value: number }
    | { _tag: "Square", value: number };

const Shape = {
    Circle: (value: number) => ({ _tag: "Circle", value }),
    Square: (value: number) => ({ _tag: "Square", value })
};


function area(shape: Shape): void {
    switch (shape) {
        case Shape.Circle(r):
            console.log("Circle area:", 3.14 * r * r);
            break;
        case Shape.Rectangle(w):
            console.log("Rectangle area:", w * w);
            break;
    }
}

function main(): void {
    const c = Shape.Circle(5);
    const s = Shape.Square(4);
    area(c);
    area(s);
}

main();
```

</Listing>

每个枚举变体变成一个 `{ _tag: "...", value: T }` 对象。`is` 表达式
转译为对 `_tag` 字段的 `switch`，这正是 TypeScript 处理可辨识联合的方式。

## 穷尽性检查

Auto 的 `is` 表达式要求处理每个变体。如果你向枚举添加新变体但忘记
在 `is` 表达式中处理它，编译器会发出警告。TypeScript 通过 `switch`
默认分支中的 `never` 类型检查实现相同的效果。

## TypeScript 独有的收窄功能

以下 TypeScript 收窄功能在 Auto 中没有直接对应物，因为 Auto 使用 `is`
模式匹配作为统一的收窄机制。

### `typeof` 守卫

```typescript
// 仅限 TypeScript
function format(value: string | number) {
    if (typeof value === "string") {
        return value.toUpperCase();
    }
    return value.toFixed(2);
}
```

在 Auto 中，请改用 `is` 模式匹配与枚举变体。

### `instanceof` 收窄

```typescript
// 仅限 TypeScript
function formatDate(date: Date | string) {
    if (date instanceof Date) {
        return date.toISOString();
    }
    return date;
}
```

Auto 没有带运行时类型信息的类。请改用基于枚举的标签。

### 类型谓词

```typescript
// 仅限 TypeScript
function isFish(pet: Fish | Bird): pet is Fish {
    return (pet as Fish).swim !== undefined;
}
```

Auto 的 `is` 表达式隐式处理了这一点——每个分支已经具有收窄后的类型。

## 快速参考

| TypeScript | Auto | 描述 |
|-----------|------|------|
| `typeof x === "string"` | `x is str => ...` | 类型检查 |
| `x instanceof Date` | 枚举标签 | 运行时类型检查 |
| `switch (x.kind)` | `x is { ... }` | 可辨识联合 |
| `if (value)` | `if value` | 真值检查 |
| `x is Type`（谓词） | `is` 分支绑定 | 类型谓词 |
