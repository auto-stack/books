# 设计模式

本章介绍 TypeScript 中常见的设计模式，以及它们如何映射到 Auto。大多数模式
可以直接迁移，但 Auto 的类型系统和模块模型简化了其中几种。

## 单例

**单例**模式确保一个类只有一个实例。在 TypeScript 中，经典做法是使用
`private` 构造函数配合 `static getInstance()` 方法：

```typescript
// TypeScript — 单例类
class Database {
    private static instance: Database;
    private constructor() {}

    static getInstance(): Database {
        if (!Database.instance) {
            Database.instance = new Database();
        }
        return Database.instance;
    }
}
```

在实践中，TypeScript 开发者更倾向于使用更简单的**模块级导出**方式——
模块只会被求值一次，因此其顶层导出天然就是单例：

```typescript
// TypeScript — 模块单例（推荐）
export const db = new Database();
```

Auto 更进一步。在 Auto 中，**模块的顶层状态天然就是单例**——在整个程序中
共享。不需要私有构造函数或 `getInstance()` 样板代码：

```auto
// Auto — 模块单例（唯一的方式）
var db = Database()
```

无需任何仪式。模块系统保证了单一实例。

## 柯里化

**柯里化**将 `f(a, b) => c` 转换为 `f(a) => f(b) => c`，实现**偏应用**
和干净的函数组合：

```typescript
// TypeScript
const add = (x: number) => (y: number) => x + y;
const add5 = add(5);
add5(3);   // 8
add5(10);  // 15
```

Auto 的语法几乎完全相同——用空格分隔的类型注解替代冒号：

```auto
// Auto
let add = (x int) => (y int) => x + y
let add5 = add(5)
add5(3)   // 8
add5(10)  // 15
```

柯里化在构建可复用的工具函数时非常有用。柯里化的日志函数可以预绑定日志级别：

```typescript
const log = (level: string) => (msg: string) =>
    console.log(`[${level}] ${msg}`);
const warn = log("WARN");
warn("disk space low");
```

```auto
let log = (level str) => (msg str) =>
    print("[{level}] {msg}")
let warn = log("WARN")
warn("disk space low")
```

## 构建器模式

**构建器**模式通过链式调用逐步构建复杂对象。两种语言都通过返回 `this`
或 `self` 的链式方法来支持这一模式：

```typescript
// TypeScript
class QueryBuilder {
    private table = "";
    private conditions: string[] = [];

    from(table: string): this { this.table = table; return this; }
    where(c: string): this { this.conditions.push(c); return this; }
    build(): string {
        const w = this.conditions.length > 0
            ? " WHERE " + this.conditions.join(" AND ") : "";
        return "SELECT * FROM " + this.table + w;
    }
}
const q = new QueryBuilder().from("users").where("age > 18").build();
```

```auto
// Auto
type QueryBuilder {
    var table str
    var conditions []str

    fn from(table str) QueryBuilder { self.table = table; self }
    fn where(c str) QueryBuilder { self.conditions.push(c); self }
    fn build() str {
        let w = if self.conditions.len() > 0 {
            " WHERE " + self.conditions.join(" AND ")
        } else { "" }
        "SELECT * FROM " + self.table + w
    }
}
fn main() {
    let q = QueryBuilder().from("users").where("age > 18").build()
    print(q)
}
```

该模式在两种语言中完全相同。Auto 的显式 `self` 返回类型比 TypeScript
的多态 `this` 更清晰。

## 类型安全的事件发射器

**类型安全的事件发射器**提供订阅/发射机制，具有完整的类型安全。每个发射器
由事件数据类型 `T` 参数化，因此监听器接收正确类型的参数。

<Listing name="event-emitter" file="listings/ch14-event-emitter">

```auto
// Auto — 类型安全的事件发射器
type Emitter<T> {
    var listeners []fn(T)

    fn on(listener fn(T)) {
        self.listeners.push(listener)
    }

    fn emit(event T) {
        for listener in self.listeners {
            listener(event)
        }
    }

    fn off(listener fn(T)) bool {
        let idx = self.listeners.index_of(listener)
        if idx >= 0 {
            self.listeners.remove_at(idx)
            true
        } else {
            false
        }
    }
}

// 柯里化示例
let add = (x int) => (y int) => x + y

fn main() {
    // 事件发射器
    var clicks = Emitter([]fn(int))
    clicks.on((n int) => print("Click #{n}"))
    clicks.on((n int) => print("  count = {n}"))
    clicks.emit(1)
    clicks.emit(2)

    // 柯里化
    let add5 = add(5)
    print("add(5)(3) = {add5(3)}")
    print("add(5)(10) = {add5(10)}")

    // 字符串事件
    var messages = Emitter([]fn(str))
    messages.on((msg str) => print("Message: {msg}"))
    messages.emit("Hello, Auto!")
}
```

```typescript
// TypeScript — 类型安全的事件发射器
class Emitter<T> {
    private listeners: ((event: T) => void)[] = [];

    on(listener: (event: T) => void): void {
        this.listeners.push(listener);
    }

    emit(event: T): void {
        for (const listener of this.listeners) {
            listener(event);
        }
    }

    off(listener: (event: T) => void): boolean {
        const idx = this.listeners.indexOf(listener);
        if (idx >= 0) {
            this.listeners.splice(idx, 1);
            return true;
        }
        return false;
    }
}

// 柯里化示例
const add = (x: number) => (y: number) => x + y;

// 事件发射器
const clicks = new Emitter<number>();
clicks.on((n) => console.log("Click #" + n));
clicks.on((n) => console.log("  count = " + n));
clicks.emit(1);
clicks.emit(2);

// 柯里化
const add5 = add(5);
console.log("add(5)(3) = " + add5(3));
console.log("add(5)(10) = " + add5(10));

// 字符串事件
const messages = new Emitter<string>();
messages.on((msg) => console.log("Message: " + msg));
messages.emit("Hello, TypeScript!");
```

</Listing>

`Emitter<T>` 泛型确保 `Emitter<number>` 只接受和发射数字。两种语言以相同
方式实现——Auto 只是去掉了分号并使用空格分隔的类型注解。

## 观察者模式

**观察者**模式与事件发射器密切相关——订阅者监听被观察对象的状态变更。其实现
与上文的 `Emitter<T>` 几乎相同，用 `subscribe()`/`set()` 替代 `on()`/`emit()`。
Auto 的 `is` 模式匹配还可以在单个处理函数中路由不同的事件类型。在大多数
情况下，事件发射器更受青睐，因为它将事件源与触发状态解耦。

## 工厂模式

**工厂**模式在不暴露创建逻辑的情况下创建对象。Auto 使用 `type` 代替
`class`，并返回 `Result<T>` 而非抛出异常：

```typescript
// TypeScript — 工厂（错误时抛异常）
interface Shape { area(): number; }
class Circle implements Shape {
    constructor(private r: number) {}
    area(): number { return Math.PI * this.r * this.r; }
}
function createShape(t: string): Shape {
    if (t === "circle") return new Circle(5);
    throw new Error("Unknown: " + t);
}
```

```auto
// Auto — 工厂（返回 Result）
spec Shape { fn area() f64 }
type Circle is Shape {
    radius f64
    fn area() f64 { 3.14159 * self.radius * self.radius }
}
fn createShape(t str) Result<Shape> {
    t is
        "circle" => ok(Circle(5.0))
        _        => err("Unknown: " + t)
}
```

使用 `Result<T>` 而非异常使错误路径显式化，并强制调用者在编译期处理失败。

## 快速参考

| 概念 | TypeScript | Auto |
|------|-----------|------|
| 单例 | `private constructor` + `static getInstance()` | 模块顶层状态 |
| 柯里化 | `(x: number) => (y: number) => ...` | `(x int) => (y int) => ...` |
| 构建器 | 链式方法返回 `this` | 链式方法返回 `self` |
| 事件发射器 | `class Emitter<T>` | `type Emitter<T>` |
| 观察者 | `subscribe()` 返回取消订阅函数 | `subscribe()` 配合 `is` 匹配 |
| 工厂 | `function` 返回 `Shape`（抛异常） | `fn` 返回 `Result<Shape>` |
| 错误处理 | `throw new Error(...)` | `Result<T>` 配合 `err(...)` |
