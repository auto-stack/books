# 类

Auto 的 `type` 加方法等价于 TypeScript 的类。Auto 使用 `self` 代替
`this`，通过 `as` 支持 spec 实现，并通过 `has` 提供组合。本章涵盖 Auto
的方式以及额外的 TypeScript 独有类特性。

## 带方法的类型

在 Auto 中，方法直接定义在 `type` 块内。字段声明为名称-类型对，方法使用
`self` 引用当前实例：

```auto
type Counter {
    count int

    fn new() Counter {
        return Counter(0)
    }

    fn increment() {
        self.count = self.count + 1
    }

    fn get() int {
        return self.count
    }
}

fn main() {
    let c = Counter.new()
    c.increment()
    c.increment()
    print(c.get())
}
```

```typescript
class Counter {
    count: number;

    constructor(count: number) {
        this.count = count;
    }

    increment(): void {
        this.count = this.count + 1;
    }

    get(): number {
        return this.count;
    }
}

function main(): void {
    const c = Counter.new();
    c.increment();
    c.increment();
    console.log(c.get());
}

main();
```

`self` 转译为 TypeScript 中的 `this`。`new` 方法作为工厂构造函数，
返回 `Counter` 的新实例。

## 实现 Spec

类型可以使用 `as` 关键字实现一个或多个 spec：

```auto
spec Printable {
    fn toString() string
}

type User as Printable {
    name string

    fn toString() string {
        return "User(" + self.name + ")"
    }
}

fn main() {
    let u = User("Alice")
    print(u.toString())
}
```

```typescript
interface Printable {
    toString(): string;
}

class User implements Printable {
    name: string;

    constructor(name: string) {
        this.name = name;
    }

    toString(): string {
        return "User(" + this.name + ")";
    }
}

function main(): void {
    const u = User("Alice");
    console.log(u.toString());
}

main();
```

一个类型可以通过逗号分隔实现多个 spec：`type X as SpecA, SpecB { }`。

## 使用 `has` 进行组合

Auto 使用 `has` 通过将一个类型的方法嵌入另一个类型来组合类型。这是继承
的结构性替代方案：

```auto
type Logger {
    fn log(msg string) {
        print("[LOG]", msg)
    }
}

type Service has Logger {
    name string

    fn start() {
        self.log("Service started:" + self.name)
    }
}

fn main() {
    let svc = Service("api")
    svc.start()
    svc.log("custom message")
}
```

```typescript
class Logger {
    log(msg: string): void {
        console.log("[LOG]", msg);
    }
}

class Service {
    name: string;

    constructor(name: string) {
        this.name = name;
    }

    log(msg: string): void {
        console.log("[LOG]", msg);
    }

    start(): void {
        this.log("Service started:" + this.name);
    }
}

function main(): void {
    const svc = Service("api");
    svc.start();
    svc.log("custom message");
}

main();
```

`has Logger` 声明将 `Logger` 的所有方法内联到 `Service` 中。与继承不同，
组合不会创建子类关系——`Service` 不是 `Logger`，它只是拥有 `Logger` 的
方法。

## 基于枚举的状态

Auto 鼓励使用枚举配合模式匹配来建模状态机，而非类层次结构：

```auto
enum State {
    Idle,
    Running,
    Done
}

type Task {
    state State
    name string

    fn new(name string) Task {
        return Task(Idle, name)
    }

    fn advance() {
        self.state = is self.state {
            Idle => Running,
            Running => Done,
            Done => Done,
        }
    }

    fn status() string {
        return is self.state {
            Idle => "idle",
            Running => "running",
            Done => "done",
        }
    }
}

fn main() {
    let t = Task.new("build")
    print(t.status())
    t.advance()
    print(t.status())
    t.advance()
    print(t.status())
}
```

```typescript
enum State {
    Idle,
    Running,
    Done
}

class Task {
    state: State;
    name: string;

    constructor(state: State, name: string) {
        this.state = state;
        this.name = name;
    }

    advance(): void {
        this.state = (() => {
            switch (this.state) {
                case State.Idle: return State.Running;
                case State.Running: return State.Done;
                case State.Done: return State.Done;
            }
        })();
    }

    status(): string {
        return (() => {
            switch (this.state) {
                case State.Idle: return "idle";
                case State.Running: return "running";
                case State.Done: return "done";
            }
        })();
    }
}

function main(): void {
    const t = Task.new("build");
    console.log(t.status());
    t.advance();
    console.log(t.status());
    t.advance();
    console.log(t.status());
}

main();
```

这种模式比带有方法重写的类层次结构更加明确和完备。`is` 表达式确保每个
情况都被处理。

## TypeScript 独有：访问器（get/set）

TypeScript 支持 getter 和 setter 访问器：

```typescript
// 仅限 TypeScript
class Temperature {
    private _celsius: number = 0;

    get fahrenheit(): number {
        return this._celsius * 9 / 5 + 32;
    }

    set fahrenheit(value: number) {
        this._celsius = (value - 32) * 5 / 9;
    }
}

const temp = new Temperature();
temp.fahrenheit = 212;
console.log(temp.celsius);  // 100
```

Getter 和 setter 提供对底层字段的受控访问。它们像属性一样调用，而非方法。

## TypeScript 独有：抽象类

TypeScript 的 `abstract` 关键字定义不能直接实例化的基类：

```typescript
// 仅限 TypeScript
abstract class Shape {
    abstract getArea(): number;

    describe(): string {
        return `Area: ${this.getArea()}`;
    }
}

class Circle extends Shape {
    constructor(public radius: number) {
        super();
    }

    getArea(): number {
        return Math.PI * this.radius * this.radius;
    }
}

const circle = new Circle(5);
console.log(circle.describe());
```

抽象类定义子类必须实现的方法，同时为其他方法提供共享实现。

## TypeScript 独有：可见性修饰符

TypeScript 支持三种类成员可见性修饰符：

```typescript
// 仅限 TypeScript
class BankAccount {
    public owner: string;
    private balance: number;
    protected id: number;

    constructor(owner: string, balance: number, id: number) {
        this.owner = owner;
        this.balance = balance;
        this.id = id;
    }
}

class SavingsAccount extends BankAccount {
    getDetails(): string {
        return `${this.owner} (id: ${this.id})`;
        // this.balance  // 错误：private
    }
}
```

- `public` — 任何地方都可访问（默认）
- `private` — 仅在类内部可访问
- `protected` — 在类及其子类中可访问

Auto 没有可见性修饰符。所有字段和方法都是公开可访问的。

## TypeScript 独有：静态成员

TypeScript 支持静态成员和静态初始化块：

```typescript
// 仅限 TypeScript
class Config {
    static instance: Config;
    static readonly VERSION = "1.0.0";

    private constructor() {}

    static {
        Config.instance = new Config();
    }

    static getInstance(): Config {
        return Config.instance;
    }
}

const cfg = Config.getInstance();
console.log(Config.VERSION);
```

静态成员属于类本身而非实例。`static { }` 块在类定义时执行一次。Auto 没有
`static` 关键字；请使用模块级函数和变量代替。

## 快速参考

| TypeScript | Auto | 描述 |
|-----------|------|------|
| `class X { }` | `type X { }` | 定义类型 |
| `this` | `self` | 引用当前实例 |
| `class X implements Y` | `type X as Y { }` | 实现 spec |
| `class X extends Y` | -- | 继承（仅限 TypeScript） |
| `get prop()` / `set prop()` | -- | 访问器（仅限 TypeScript） |
| `abstract class X` | -- | 抽象类（仅限 TypeScript） |
| `public` / `private` / `protected` | -- | 可见性修饰符（仅限 TypeScript） |
| `static` 成员 | -- | 静态成员（仅限 TypeScript） |
| `type X has Y { }` | `type X has Y { }` | 组合 |
