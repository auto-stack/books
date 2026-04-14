# 类型兼容性

类型兼容性（type compatibility）决定了什么时候一个类型可以替代另一个类型使用。TypeScript 和 Auto 都使用**结构化类型**（structural typing）——类型的*形状*重要，而非其名称。本章介绍两种语言中赋值、函数调用和泛型的有效性规则。

## 结构化类型

在*结构化类型*系统中，如果值至少具有所需的属性，则它与该类型兼容。类型的名称无关紧要——只有其结构才算数。

```typescript
// TypeScript — 结构化类型
interface Point2D { x: number; y: number; }
interface Point3D { x: number; y: number; z: number; }

const p3: Point3D = { x: 1, y: 2, z: 3 };
const p2: Point2D = p3;  // OK — Point3D 拥有 Point2D 的所有属性
```

```auto
// Auto — 结构化类型
type Point2D { x f64, y f64 }
type Point3D { x f64, y f64, z f64 }

let p3 = Point3D(1.0, 2.0, 3.0)
let p2 = p3  // OK — Point3D 拥有 Point2D 的所有字段
```

`Point3D` 可以赋值给 `Point2D`，因为它至少包含 `x` 和 `y`。额外的 `z` 字段被简单地忽略。这在 TypeScript 和 Auto 中的工作方式相同。

这与**名义类型**（nominal typing，Java、Rust struct、Swift 使用）形成对比——在名义类型系统中，兼容性要求类型名称匹配——无论共享多少字段，`Point3D` 都*不能*赋值给 `Point2D`。

## 多余属性检查

虽然结构化类型通常允许额外字段，但 TypeScript 会对直接赋值给带类型位置的*对象字面量*进行**多余属性检查**（excess property checking）。这可以捕获拼写错误和放错位置的属性。

```typescript
// TypeScript — 多余属性检查
interface Point2D { x: number; y: number; }

const p1: Point2D = { x: 1, y: 2, z: 3 };
// 错误：对象字面量只能指定已知属性，
// 且 'z' 不存在于类型 'Point2D' 中。

const obj = { x: 1, y: 2, z: 3 };
const p2: Point2D = obj;  // OK — obj 是变量，不是字面量
```

Auto 遵循相同的原则。当你直接构造类型时，意外的字段会被拒绝。当你赋值一个已存在的变量时，结构化规则适用——额外字段没问题。

```auto
type Point2D { x f64, y f64 }

let p1 = Point2D(1.0, 2.0, 3.0)
// 错误 — Point2D 只接受 x 和 y

let obj = Point3D(1.0, 2.0, 3.0)
let p2 = obj  // OK — obj 已存在，额外字段没问题
```

这是一个务实的折中：在构造时足够严格以捕获错误，在结构化赋值时足够灵活。

## 函数兼容性

函数类型有自己的兼容性规则，这也是 TypeScript 和 Auto 开始产生差异的地方。

**参数类型**——TypeScript 默认对函数参数使用*双变性*（bivariance），意味着 `(x: Base) => void` 可以赋值给 `(x: Derived) => void`，反之亦然。这在技术上是不健全的，但对常见模式（如事件处理器）很方便。

```typescript
// TypeScript — 双变函数参数
class Event { /* ... */ }
class MouseEvent extends Event { /* ... */ }

type EventHandler = (e: Event) => void;
const handler: EventHandler = (e: MouseEvent) => { /* ... */ };
// 在 TS 中 OK — MouseEvent 处理器用在了需要 Event 处理器的地方
```

Auto 更加**严格**——函数参数类型遵循标准逆变（contravariance）。接受 `Base` 的函数可以用在需要 `Derived` 的地方，但反之不行。这是健全的，可以避免微妙的 bug。

**返回类型**——两种语言在返回类型上都是*协变*（covariant）的。返回 `Derived` 的函数可以赋值给返回 `Base` 的函数类型——更具体的返回类型满足更宽泛的契约。

```typescript
// TypeScript — 协变返回类型
class Animal { name: string; }
class Dog extends Animal { breed: string; }

function getDog(): Dog { return new Dog(); }
const getAnimal: () => Animal = getDog;  // OK
```

```auto
type Animal { name str }
type Dog { name str, breed str }

fn get_dog() Dog { Dog("Rex", "Labrador") }
let get_animal = get_dog  // OK — Dog 返回类型满足 Animal 期望
```

## 枚举兼容性

TypeScript 的枚举很不寻常：每个枚举值是一个数字，枚举与 `number` 兼容，但与其他枚举*不*兼容。

```typescript
// TypeScript — 枚举兼容性
enum Direction { Up, Down, Left, Right }
enum Status { Active, Inactive }

let d: Direction = Direction.Up;
let n: number = d;       // OK — 枚举就是数字
// let s: Status = d;     // 错误 — 不同的枚举类型
```

Auto 的枚举是**代数数据类型**（algebraic data types）——每个变体是一个不同的带标签类型，不是数字。没有隐式的数字兼容性。

```auto
enum Direction {
    Up
    Down
    Left
    Right
}

let d = Direction.Up
// let n = d  // 错误 — Direction 不是数字
```

Auto 的枚举变体可以携带数据，使其比 TypeScript 基于数字的枚举更有表达力：

```auto
enum Shape {
    Circle(radius f64)
    Rectangle(width f64, height f64)
}

fn area(s Shape) f64 {
    match s {
        Circle(r) => 3.14159 * r * r
        Rectangle(w, h) => w * h
    }
}
```

## 类兼容性

TypeScript 仅根据*实例成员*比较类。构造函数和静态成员在兼容性检查中被忽略。

```typescript
// TypeScript — 类兼容性
class Animal {
    name: string;
    constructor(name: string) { this.name = name; }
}

class Person {
    name: string;
    age: number;
    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }
}

let animal: Animal = new Person("Alice", 30);  // OK
```

然而，TypeScript 对 `private` 和 `protected` 成员做了例外处理。当类拥有私有或受保护字段时，兼容性变为*名义性*的——两个类只有在共享相同的 private/protected 声明时才兼容。

```typescript
class Secret {
    private id: number;
    constructor(id: number) { this.id = id; }
}

class OtherSecret {
    private id: number;
    constructor(id: number) { this.id = id; }
}

// let s: Secret = new OtherSecret(1);  // 错误 — 不同的私有声明
```

Auto **没有访问修饰符**——所有字段都是可见的。类型兼容性始终是结构化的，无论类型是如何构造的。这消除了 TypeScript 混合方法带来的困惑。

```auto
type Animal { name str }
type Person { name str, age int }

let animal = Person("Alice", 30)  // OK — 结构化兼容
```

## 泛型类型兼容性

当泛型类型的类型参数兼容时，泛型类型才兼容。`Box<int>` 和 `Box<str>` 是*不兼容*的——参数类型不同，容器类型就不同。

```typescript
// TypeScript — 泛型兼容性
class Box<T> { value: T; }

const intBox: Box<number> = { value: 42 };
const strBox: Box<string> = { value: "hello" };

// let a: Box<number> = strBox;  // 错误 — Box<string> 不能赋值给 Box<number>
```

```auto
type Box<T> { value T }

let int_box = Box<int>(42)
let str_box = Box("hello")

// let a = str_box  // 错误 — Box<str> 与 Box<int> 不兼容
```

当类型参数仅在输出位置使用时，协变适用。如果 `T` 仅作为返回类型出现，`Box<Derived>` 可以赋值给 `Box<Base>`。两种语言都遵循此规则，尽管 TypeScript 的结构化系统可能更自由地推断它。

## 结构化赋值实践

<Listing name="structural-assign" file="listings/ch08-structural-assign">

```typescript
// TypeScript — structural type compatibility
interface Point2D { x: number; y: number; }
interface Point3D { x: number; y: number; z: number; }

function printX(p: Point2D): void {
    console.log("x = " + p.x);
}

interface Named { name: string; }
interface Employee { name: string; role: string; }

function greet(n: Named): void {
    console.log("Hello, " + n.name);
}

const p2: Point2D = { x: 1, y: 2 };
const p3: Point3D = { x: 1, y: 2, z: 3 };

printX(p2);  // exact match
printX(p3);  // OK — extra field is fine (structural)

const emp: Employee = { name: "Alice", role: "Engineer" };
greet(emp);  // OK — Employee has `name` property
```

```auto
// Auto — structural type compatibility
type Point2D {
    x f64
    y f64
}

type Point3D {
    x f64
    y f64
    z f64
}

fn print_x(p Point2D) {
    print("x = {p.x}")
}

type Named {
    name str
}

type Employee {
    name str
    role str
}

fn greet(n Named) {
    print("Hello, {n.name}")
}

fn main() {
    let p2 = Point2D(1.0, 2.0)
    let p3 = Point3D(1.0, 2.0, 3.0)

    print_x(p2)   // exact match
    print_x(p3)   // OK — extra field is fine (structural)

    let emp = Employee("Alice", "Engineer")
    greet(emp)    // OK — Employee has `name` field
}
```

</Listing>

## 快速参考

| 概念 | TypeScript | Auto |
|---|---|---|
| 类型规则 | 结构化 | 结构化 |
| 额外字段 | OK（对象字面量除外） | OK（直接构造除外） |
| 函数参数 | 双变（不健全） | 逆变（健全） |
| 返回类型 | 协变 | 协变 |
| 枚举兼容性 | 数值型，跨枚举不兼容 | ADT，无数字转换 |
| 私有/受保护 | 创建名义兼容性 | 不支持（始终结构化） |
| 泛型兼容 | 按类型参数兼容性 | 按类型参数兼容性 |
| `Box<int>` vs `Box<str>` | 不兼容 | 不兼容 |
