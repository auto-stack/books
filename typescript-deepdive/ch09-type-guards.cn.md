# 类型守卫与穷尽性检查

当你使用**联合类型**（union types）时，编译器需要知道在代码的每个位置你处理的是哪个变体。**类型收窄**（type narrowing）是将宽泛的类型细化为具体类型的过程。**穷尽性检查**（exhaustiveness checking）确保你处理了每一种可能的情况。两者共同构成了类型化语言中安全、可预测的控制流基础。

## 类型收窄

TypeScript 在条件块内使用 `typeof`、`instanceof` 和 `in` 检查来收窄类型。每个检查都告诉编译器：*"在这个分支内，将值视为更具体的类型。"*

```typescript
// TypeScript — 使用 typeof 和 instanceof 收窄
function process(value: number | string) {
    if (typeof value === "string") {
        console.log(value.toUpperCase());  // value: string
    } else {
        console.log(value.toFixed(2));     // value: number
    }
}

class Dog { bark() { console.log("woof"); } }
class Cat { meow() { console.log("meow"); } }

function speak(pet: Dog | Cat) {
    if (pet instanceof Dog) {
        pet.bark();  // pet: Dog
    } else {
        pet.meow();  // pet: Cat
    }
}
```

Auto 使用 `is` 关键字收窄类型——这是一个**统一的模式匹配**（pattern matching）构造，替代了 TypeScript 的三种收窄机制：

```auto
// Auto — 使用 is 收窄
fn process(value int | str) {
    value is
        str => print(value.to_upper())
        int => print("{value}")
}

type Dog { fn bark(self) }
type Cat { fn meow(self) }

fn speak(pet Dog | Cat) {
    pet is
        Dog => pet.bark()
        Cat => pet.meow()
}
```

一个关键字，一种一致的语法，适用于所有收窄场景。

## `typeof` 和 `instanceof` 守卫

TypeScript 提供了两种内置类型守卫。`typeof` 守卫收窄到原始类型：

```typescript
function double(x: number | string): number | string {
    if (typeof x === "number") return x * 2;
    return x + x;
}
```

`instanceof` 守卫收窄到类类型：

```typescript
class FileReader { read() { return "file data"; } }
class HttpReader { fetch() { return "http data"; } }

function get_data(reader: FileReader | HttpReader): string {
    if (reader instanceof FileReader) {
        return reader.read();
    }
    return reader.fetch();
}
```

在 Auto 中，两者都用 `is` 表达：

```auto
fn double(x int | str) int | str {
    x is
        int => x * 2
        str => x + x
}

type FileReader { fn read(self) str }
type HttpReader { fn fetch(self) str }

fn get_data(reader FileReader | HttpReader) str {
    reader is
        FileReader => reader.read()
        HttpReader => reader.fetch()
}
```

`is` 表达式检查运行时类型并为每个分支收窄变量——不需要单独的 `typeof` 或 `instanceof`。

## 字面量类型

在 TypeScript 中，单个值可以作为类型。**字面量类型**（literal type）将变量限制为某个特定值：

```typescript
let direction: "North" | "South" | "East" | "West";
direction = "North";     // OK
// direction = "Up";     // 错误

type Status = "loading" | "success" | "error";
```

字面量类型是**可辨识联合**（discriminated unions）的基础，这将在第 10 章深入讲解。当与共享属性结合时，它们实现了穷尽的 `switch` 语句：

```typescript
type Action =
    | { type: "fetch"; url: string }
    | { type: "cancel"; id: number };

function handle(action: Action) {
    switch (action.type) {
        case "fetch": console.log("Fetching " + action.url); break;
        case "cancel": console.log("Cancel " + action.id); break;
    }
}
```

Auto 支持同样的字面量类型概念：

```auto
let direction "North" | "South" | "East" | "West"
direction = "North"     // OK
// direction = "Up"     // 错误

type Status = "loading" | "success" | "error"
```

## 用户自定义类型守卫

TypeScript 允许你编写**自定义类型守卫函数**，使用 `arg is Type` 返回注解来断言特定类型：

```typescript
function isString(value: unknown): value is string {
    return typeof value === "string";
}

function process(value: string | number) {
    if (isString(value)) {
        console.log(value.toUpperCase());  // value: string
    } else {
        console.log(value.toFixed(2));     // value: number
    }
}
```

`value is string` 部分告诉编译器：当函数返回 `true` 时，`value` 是 `string`。这很强大但很冗长——你必须为每个检查编写和维护一个单独的函数。

Auto **不需要用户自定义类型守卫**。`is` 模式匹配原生处理了这一点：

```auto
fn process(value str | int) {
    value is
        str => print(value.to_upper())
        int => print("{value}")
}
```

不需要单独的守卫函数，不需要 `value is Type` 返回注解。`is` 关键字*就是*类型守卫。

## 使用 `never` 进行穷尽性检查

当你有一个联合类型时，你希望确保每个变体都被处理了。TypeScript 使用 `never` 类型来检测**遗漏的情况**：

```typescript
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rect"; width: number; height: number };

function area(s: Shape): number {
    switch (s.kind) {
        case "circle": return Math.PI * s.radius * s.radius;
        case "rect": return s.width * s.height;
        default:
            const _exhaustive: never = s;
            return _exhaustive;  // 如果 Shape 添加了新变体，此处报错
    }
}
```

如果你后来向 `Shape` 添加了 `{ kind: "triangle"; ... }`，`never` 赋值会在编译时失败，提醒你 `area` 函数不完整。

一个常见的模式是 `assertNever` 辅助函数：

```typescript
function assertNever(x: never): never {
    throw new Error("Unhandled case: " + x);
}
```

Auto 的 `is` 关键字**内置了穷尽性检查**。编译器会验证每个变体都已被处理：

```auto
enum Shape {
    Circle(f64),
    Rect(f64, f64)
}

fn area(s Shape) f64 {
    s is
        Circle(r) => 3.14159 * r * r
        Rect(w, h) => w * h
        // 在此添加新变体会导致编译错误
}
```

不需要 `never` 技巧，不需要 `assertNever` 辅助函数——穷尽性检查内置于语言之中。

## `never` 类型

TypeScript 的 `never` 是**底部类型**（bottom type）——没有任何值可以具有的类型。它出现在两种关键场景中：

*永不返回的函数*——它们要么抛出异常，要么无限循环：

```typescript
function fail(message: string): never {
    throw new Error(message);
}

function infiniteLoop(): never {
    while (true) {}
}
```

*不可达代码*——当所有可能性都被消除时，编译器推断为 `never`：

```typescript
type Status = "ok" | "err";
function check(s: Status) {
    if (s === "ok") return;
    else return;
    // 此处 s 是 never — 两种情况都已处理
}
```

`void` 和 `never` 之间的区别微妙但重要：`void` 意味着函数不返回任何值（如 `console.log`），而 `never` 意味着函数**永远不会返回**。

Auto 使用 `!` 作为返回类型来表示传播错误的函数（类似于 `never` 的发散概念）。但 Auto **不**将 `never` 作为独立类型暴露——`is` 模式匹配直接处理穷尽性检查，因此不需要 `assertNever` 或手动的 `never` 赋值。

<Listing name="pattern-matching" file="listings/ch09-pattern-matching">

```auto
// Auto — pattern matching and exhaustiveness
enum Shape {
    Circle(f64),
    Rect(f64, f64),
    Triangle(f64, f64, f64)
}

enum Option<T> {
    Some(T),
    None
}

fn area(s Shape) f64 {
    s is
        Circle(r) => 3.14159 * r * r
        Rect(w, h) => w * h
        Triangle(a, b, c) => {
            let s = (a + b + c) / 2.0
            sqrt(s * (s - a) * (s - b) * (s - c))
        }
}

fn describe(s Shape) str {
    s is
        Circle(r) => "Circle(r={r})"
        Rect(w, h) => "Rect({w}, {h})"
        Triangle(a, b, c) => "Triangle({a}, {b}, {c})"
}

fn process(value int | str | bool) {
    value is
        int => print("Integer: {value}")
        str => print("String length: {value.len()}")
        bool => print(if value { "true" } else { "false" })
}

fn main() {
    let shapes = [
        Shape.Circle(5.0),
        Shape.Rect(3.0, 4.0),
        Shape.Triangle(3.0, 4.0, 5.0)
    ]
    for shape in shapes {
        print(describe(shape))
        print("  area = {area(shape)}")
    }

    process(42)
    process("hello")
    process(true)
}
```

```typescript
// TypeScript — type guards and narrowing
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rect"; width: number; height: number }
    | { kind: "triangle"; a: number; b: number; c: number };

function area(s: Shape): number {
    switch (s.kind) {
        case "circle":
            return Math.PI * s.radius * s.radius;
        case "rect":
            return s.width * s.height;
        case "triangle":
            const p = (s.a + s.b + s.c) / 2;
            return Math.sqrt(p * (p - s.a) * (p - s.b) * (p - s.c));
    }
}

function describe(s: Shape): string {
    switch (s.kind) {
        case "circle": return `Circle(r=${s.radius})`;
        case "rect": return `Rect(${s.width}, ${s.height})`;
        case "triangle": return `Triangle(${s.a}, ${s.b}, ${s.c})`;
    }
}

function process(value: number | string | boolean): void {
    if (typeof value === "number") {
        console.log("Integer: " + value);
    } else if (typeof value === "string") {
        console.log("String length: " + value.length);
    } else {
        console.log(value ? "true" : "false");
    }
}

const shapes: Shape[] = [
    { kind: "circle", radius: 5 },
    { kind: "rect", width: 3, height: 4 },
    { kind: "triangle", a: 3, b: 4, c: 5 }
];
for (const shape of shapes) {
    console.log(describe(shape));
    console.log("  area = " + area(shape));
}

process(42);
process("hello");
process(true);
```

</Listing>

## 快速参考

| 概念 | TypeScript | Auto |
|---|---|---|
| 类型收窄 | `typeof x === "string"` | `x is str => ...` |
| 类检查 | `x instanceof Foo` | `x is Foo => ...` |
| 属性检查 | `"prop" in obj` | *(使用 `is` 匹配 enum/tag)* |
| 字面量类型 | `type D = "N" \| "S"` | `type D = "N" \| "S"` |
| 用户自定义守卫 | `function isFoo(x): x is Foo` | *(不需要)* |
| 穷尽性检查 | `const _: never = x` | *(内置于 `is`)* |
| 底部类型 | `never` | `!`（错误传播） |
| 无返回值 | `void` | *(隐式)* |
