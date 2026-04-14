# 对象类型

Auto 提供两种主要的对象类型定义机制：`type` 用于数据结构（转译为
TypeScript `class`），`spec` 用于行为契约（转译为 TypeScript `interface`）。

## `spec` 关键字（接口）

使用 `spec` 定义行为契约——一组类型必须实现的方法签名。这是 Auto 中
等同于 TypeScript `interface` 的机制。

<Listing number="05-01" file="listings/ch05/listing-05-01/main.at" caption="spec 声明">

```auto
spec Greetable {
    fn greet()
}

fn main() {
    print("spec Greetable defined")
}
```

```typescript
function main(): void {
    console.log("spec Greetable defined");
}

main();
```

</Listing>

`spec` 转译为带有方法签名的 TypeScript `interface`。实现 spec 的类型必须
为所有方法提供具体实现。

## 实现 spec

使用 `type Name as SpecName` 声明类型实现了某个 spec。这是 Auto 中等同
于 TypeScript `class X implements Y` 的机制。

<Listing number="05-02" file="listings/ch05/listing-05-02/main.at" caption="实现 spec">

```auto
spec Greetable {
    fn greet()
}

type User as Greetable {
    name int
    fn greet() {
        print("Hello from user", self.name)
    }
}

fn main() {
    let user = User(42)
    user.greet()
}
```

```typescript
class User implements Greetable {
    name: number;

    constructor(name: number) {
        this.name = name;
    }

    greet(): void {
        console.log("Hello from user", this.name);
    }
}

function main(): void {
    const user = User(42);
    user.greet();
}

main();
```

</Listing>

类型声明上的 `as Greetable` 子句告诉 TypeScript 编译器 `User` 实现了
`Greetable` 接口。在 `type` 块内定义的方法成为类方法，使用 `self`
（转译为 `this`）访问字段。

## 使用 `has` 进行组合

Auto 通过 `has` 关键字支持组合。当一个类型 `has` 另一个类型时，它
嵌入后者的所有方法。这是混入或 trait 组合的一种形式。

<Listing number="05-04" file="listings/ch05/listing-05-04/main.at" caption="使用 has 进行组合">

```auto
type Wing {
    fn flap() {
        print("Flap!")
    }
}

type Duck has Wing {
    name int
}

fn main() {
    let duck = Duck(1)
    duck.flap()
    print("Duck name:", duck.name)
}
```

```typescript
class Wing {

    flap(): void {
    console.log("Flap!");
}
}

class Duck {
    name: number;

    constructor(name: number) {
        this.name = name;
    }

    flap(): void {
    console.log("Flap!");
}
}

function main(): void {
    const duck = Duck(1);
    duck.flap();
    console.log("Duck name:", duck.name);
}

main();
```

</Listing>

`type Duck has Wing` 声明将 `Wing` 的所有方法嵌入 `Duck`。在 TypeScript
输出中，方法直接内联到 `Duck` 类中。这是继承的有力替代方案——你
可以在不产生 `extends` 链紧耦合的情况下获得代码复用。

## 可选字段

Auto 支持使用字段名后的 `?` 后缀定义可选字段：

<Listing number="05-05" file="listings/ch05/listing-05-05/main.at" caption="可选字段">

```auto
type Config {
    host int
    port? int
}

fn main() {
    let c = Config(8080)
    print("Host:", c.host)
    if c.port {
        print("Port:", c.port)
    }
}
```

```typescript
class Config {
    host: number;
    port: number | null;

    constructor(host: number, port: number | null) {
        this.host = host;
        this.port = port;
    }
}

function main(): void {
    const c = Config(8080);
    console.log("Host:", c.host);
    if (c.port) {
        console.log("Port:", c.port);
    }
}

main();
```

</Listing>

可选字段转译为 TypeScript 的可选属性（`port?: number`），构造函数参数
也是可选的。

## 快速参考

| TypeScript | Auto | 描述 |
|-----------|------|------|
| `interface X { }` | `spec X { }` | 行为契约 |
| `class X implements Y` | `type X as Y { }` | 实现接口 |
| `class X extends Y` | — | 继承（仅限 TypeScript） |
| `class X { ... }` | `type X { ... }` | 数据结构 |
| `obj.x` | `self.x` 或 `obj.x` | 属性访问 |
| `prop?: T` | `prop? T` | 可选属性 |

## TypeScript 独有功能

### 继承（`extends`）

```typescript
// 仅限 TypeScript
class Dog extends Animal {
    breed: string;
}
```

Auto 目前在 a2ts 转译器中不支持通过 `extends` 进行类型继承。请改用
`has` 组合。

### 交叉类型（`&`）

```typescript
// 仅限 TypeScript
type ColorfulCircle = Colorful & Circle;
```

Auto 使用 `has` 进行组合，在实现层面达到类似的效果。

### 只读属性

```typescript
// 仅限 TypeScript
class Person {
    readonly name: string;
}
```

Auto 使用 `let`（不可变）声明变量，但没有字段的 `readonly` 修饰符。
