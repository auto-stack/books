# 索引签名与类型运算符

TypeScript 提供**索引签名**（index signatures）和**类型级运算符**（`keyof`、
`typeof`、mapped types），让你能够处理动态属性访问并程序化地变换类型。Auto
有意省略了这些特性，转而选择 `has` 组合和显式方法。本章将探讨两种方法
并解释各自的适用场景。

## TypeScript 中的索引签名

**索引签名**声明一个对象可以拥有给定类型的任意键，所有键都映射到相同的
值类型。这对于字典、映射和其他动态数据结构非常有用。

```typescript
// TypeScript — 字符串索引签名
interface StringMap {
    [key: string]: number;
}

const scores: StringMap = {};
scores["alice"] = 95;
scores["bob"] = 87;
// scores["charlie"] = "excellent"; // 错误：值必须是 number
```

```typescript
// TypeScript — 数字索引签名
interface StringArray {
    [index: number]: string;
}

const names: StringArray = ["Alice", "Bob"];
console.log(names[0]); // "Alice"
```

索引签名只允许 `string` 或 `number` 作为键类型。数字索引签名主要用于描述
类数组对象。对于大多数字典用例，TypeScript 开发者也会使用内置的
`Map<K, V>` 类。

一个细微之处：当字符串索引签名与已知属性同时存在时，已知属性的值类型
必须可赋值给索引签名的值类型：

```typescript
// TypeScript — 混合索引签名与已知属性
interface Config {
    [key: string]: string | number;
    host: string;    // OK — string 可赋值给 string | number
    port: number;    // OK — number 可赋值给 string | number
    // debug: boolean; // 错误 — boolean 不可赋值给 string | number
}
```

## Auto 的方法：用 `has` 组合替代索引签名

Auto **没有**索引签名。任意的动态键访问本质上是不安全的——你会在编译时
失去对哪些键存在以及它们映射到什么类型的了解。取而代之的是，Auto 使用
`has` 组合从可复用组件构建类型。

```auto
// Auto — 用 has 组合
type Engine {
    horsepower int
    fn start() { print("Engine started") }
}

type Wheels {
    count int
    fn roll() { print("Rolling...") }
}

type Car has Engine, Wheels {
    brand str
}
```

`type Car has Engine, Wheels` 让 `Car` 获得 `Engine` 和 `Wheels` 的所有字段
和方法。这比索引签名更明确、更类型安全，因为每个字段和方法都在编译时
已知。

```auto
fn main() {
    let car = Car(horsepower: 300, count: 4, brand: "Tesla")
    car.start()   // 来自 Engine 的方法
    car.roll()    // 来自 Wheels 的方法
    print(car.brand)  // 自有字段
}
```

在 TypeScript 使用索引签名处理动态数据的地方，Auto 提供标准库中的专用
集合类型——如 `Map<K, V>`——通过显式方法进行访问：

```auto
// Auto — 显式 map 类型
let scores = Map<str, int>()
scores.set("alice", 95)
scores.set("bob", 87)

let alice_score = scores.get("alice")  // ?int (可选值)

match alice_score {
    Some(v) => print("Alice scored {v}")
    None => print("Alice not found")
}
```

<Listing name="has-composition" file="listings/ch11-has-composition">

```auto
// Auto — has composition vs index signatures
type Named {
    name str
    fn greet() { print("Hi, I'm {self.name}") }
}

type Aged {
    age int
}

type Logged {
    fn log(msg str) { print("[LOG] {msg}") }
}

type User has Named, Aged, Logged {
    email str
}

type Admin has Named, Logged {
    level int
}

fn introduce(u User) {
    u.greet()
    print("Age: {u.age}")
}

fn main() {
    let user = User("Alice", 30, "alice@example.com")
    user.greet()
    user.log("User created")
    print("Email: {user.email}")

    let admin = Admin("Bob", 1)
    admin.greet()
    admin.log("Admin logged in")
    print("Admin level: {admin.level}")

    // Structural typing — Admin satisfies the parts User needs
    // But introduce() requires `age`, which Admin doesn't have
}
```

</Listing>

## `keyof` 运算符（TypeScript 独有）

TypeScript 的 `keyof` 运算符生成一个类型的所有属性**名称**的联合。它是
mapped types 和许多工具类型的基础：

```typescript
// TypeScript — keyof 提取属性名
type Person = { name: string; age: number };
type PersonKeys = keyof Person;  // "name" | "age"

// 用于安全的属性访问
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const p: Person = { name: "Ada", age: 30 };
getProperty(p, "name");  // string
// getProperty(p, "email"); // 错误："email" 不是 Person 的键
```

`keyof` 与 mapped types 结合使用时尤其强大，可以变换类型的每个属性。Auto
**没有** `keyof`——Auto 枚举和 `is` 模式匹配服务于类似的类型安全属性处理
需求。

## `typeof` 运算符

TypeScript 的 `typeof` 在类型层面捕获值的**类型**。这对于将类型声明与
运行时值同步非常有用：

```typescript
// TypeScript — typeof 捕获值的类型
const config = {
    host: "localhost",
    port: 8080,
    debug: true
};

type Config = typeof config;
// { host: string; port: number; debug: boolean }

function loadConfig(c: Config): void { /* ... */ }
loadConfig(config); // OK — config 匹配自身的类型
```

Auto 通过**类型推断**来处理这一点。当你声明一个值时，编译器会自动推断
其类型。显式的 `typeof` 是不必要的，因为推断的类型始终可用：

```auto
// Auto — 类型推断替代 typeof
let config = {
    host = "localhost"
    port = 8080
    debug = true
}
// config 被推断为 { host: str; port: int; debug: bool }

fn load_config(c typeof config) { ... }
load_config(config)
```

## Mapped Types（TypeScript 独有）

**Mapped types**（映射类型）变换已有类型的每个属性以产生新类型。它们使用
`keyof` 和 `in` 来遍历属性名：

```typescript
// TypeScript — mapped types
type Readonly<T> = { readonly [K in keyof T]: T[K] };

type Partial<T> = { [K in keyof T]?: T[K] };

type Pick<T, K extends keyof T> = { [P in K]: T[P] };

type Record<K extends string, V> = { [P in K]: V };
```

这些是 TypeScript 内置工具类型的基础。`Partial<T>` 使每个属性变为可选；
`Readonly<T>` 使每个属性变为不可变；`Record<K, V>` 从键集合创建类型。

```typescript
// TypeScript — 使用 mapped types
interface Todo {
    title: string;
    description: string;
    done: boolean;
}

type PartialTodo = Partial<Todo>;
// { title?: string; description?: string; done?: boolean }

type TodoKeys = keyof Todo;  // "title" | "description" | "done"
type TodoPreview = Pick<Todo, "title" | "done">;
// { title: string; done: boolean }
```

Auto **没有** mapped types。类型级计算被有意省略，以保持类型系统简洁且编译
快速。Auto 通过泛型、spec 和 `has` 组合实现类似目标——无需类型级循环和
条件式的复杂性。

## 实战对比——构建字典

以下是在两种语言中构建类似映射结构的方式：

```typescript
// TypeScript — 索引签名方式
interface Dictionary<T> {
    [key: string]: T;
}

const dict: Dictionary<number> = {};
dict["x"] = 42;
console.log(dict["x"]);  // 42
console.log(dict["missing"]);  // undefined — 无编译时警告
```

```typescript
// TypeScript — Map 方式（更安全）
const map = new Map<string, number>();
map.set("x", 42);
map.get("x");       // 42
map.get("missing"); // undefined
map.has("x");       // true
```

```auto
// Auto — 标准库 Map
let map = Map<str, int>()
map.set("x", 42)

let value = map.get("x")       // ?int (Some(42))
let missing = map.get("nope")  // ?int (None)
let exists = map.has("x")      // bool (true)
```

Auto 的 `Map` 从 `get` 返回 `?T`（可选值），强制你显式处理缺失键的情况。
TypeScript 的索引签名静默返回 `undefined`，这是运行时错误的常见来源。

## 快速参考

| 概念 | TypeScript | Auto |
|------|-----------|------|
| 字符串索引签名 | `{ [key: string]: T }` | *(不支持)* |
| 数字索引签名 | `{ [index: number]: T }` | *(不支持)* |
| 字典 | 索引签名或 `Map<K, V>` | `Map<K, V>`，返回 `?T` |
| 属性名联合 | `keyof T` | *(不支持)* |
| 值类型捕获 | `typeof x` | 类型推断 |
| 映射类型 | `{ [K in keyof T]: T[K] }` | *(不支持)* |
| 工具类型 | `Partial<T>`、`Pick<T, K>` | *(不支持)* |
| 组合 | 交集类型 `&` | `has` 关键字 |
