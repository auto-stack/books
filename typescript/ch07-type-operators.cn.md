# 类型运算符

TypeScript 提供了几个运算符，让你在类型级别查询和组合类型。Auto 共享基本
的属性访问，但不实现高级类型级运算符。

## 属性访问

Auto 和 TypeScript 都使用点表示法进行属性访问：

```auto
type Point {
    x int
    y int
}

fn main() {
    let p = Point(3, 4)
    print(p.x)
    print(p.y)
}
```

```typescript
class Point {
    x: number;
    y: number;

    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
    }
}

function main(): void {
    const p = Point(3, 4);
    console.log(p.x);
    console.log(p.y);
}

main();
```

这是 Auto 支持的唯一类型运算符。本章其余内容均为 TypeScript 独有。

## TypeScript 独有：`keyof`

`keyof` 运算符创建给定类型的所有已知公共属性名的联合类型：

```typescript
// 仅限 TypeScript
type Person = { name: string; age: number; city: string };
type Keys = keyof Person;
// "name" | "age" | "city"
```

这对于编写接受属性名作为参数的泛型函数很有用：

```typescript
// 仅限 TypeScript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const person = { name: "Alice", age: 30 };
const name = getProperty(person, "name");  // string
const age = getProperty(person, "age");    // number
```

将 `keyof` 与泛型约束结合使用可确保动态访问属性时的类型安全。

### `keyof` 与索引类型

`keyof` 也可用于数组和映射：

```typescript
// 仅限 TypeScript
type ArrayKeys = keyof string[];    // "length" | "toString" | ...
type MapKeys = keyof Map<string, number>;  // Map 方法名
```

注意，对数组使用 `keyof` 不会产生数字索引——它产生的是 `Array` 方法和
属性的名称。

## TypeScript 独有：`typeof` 类型运算符

`typeof` 运算符在类型级别捕获值的类型。这与 JavaScript 运行时的 `typeof`
不同：

```typescript
// 仅限 TypeScript
const colors = {
    red: "#ff0000",
    green: "#00ff00",
    blue: "#0000ff",
};

type Colors = typeof colors;
// { red: string; green: string; blue: string }

type ColorValue = typeof colors["red"];
// string
```

### 与 `const` 断言配合

`typeof` 通常与 `as const` 配合使用以获取精确的字面量类型：

```typescript
// 仅限 TypeScript
const directions = ["north", "south", "east", "west"] as const;
type Direction = typeof directions[number];
// "north" | "south" | "east" | "west"
```

如果不使用 `as const`，`typeof directions` 将是 `string[]`，会丢失字面量
信息。

### 捕获函数类型

`typeof` 也可用于函数和类：

```typescript
// 仅限 TypeScript
function createPair(x: number, y: string): [number, string] {
    return [x, y];
}

type FnType = typeof createPair;
// (x: number, y: string) => [number, string]
```

## TypeScript 独有：索引访问类型

索引访问类型让你使用括号表示法查找类型的特定属性：

```typescript
// 仅限 TypeScript
type Person = { name: string; age: number; address: { city: string } };

type Name = Person["name"];            // string
type City = Person["address"]["city"]; // string
```

### 联合键

当索引是键的联合时，结果是对应属性类型的联合：

```typescript
// 仅限 TypeScript
type Person = { name: string; age: number };
type NameOrAge = Person["name" | "age"];
// string | number
```

### 与 `keyof` 配合

将索引访问与 `keyof` 结合会产生所有属性类型的联合：

```typescript
// 仅限 TypeScript
type Person = { name: string; age: number; active: boolean };
type Values = Person[keyof Person];
// string | number | boolean
```

### 对数组使用 `number`

在数组类型上使用 `number` 作为索引会得到元素类型：

```typescript
// 仅限 TypeScript
type StringArray = string[];
type Element = StringArray[number];
// string
```

## 快速参考

| TypeScript | Auto | 描述 |
|-----------|------|------|
| `obj.field` | `obj.field` 或 `self.field` | 属性访问 |
| `keyof T` | -- | 属性键的联合（仅限 TypeScript） |
| `typeof value` | -- | 值的类型（仅限 TypeScript） |
| `Type["key"]` | -- | 索引访问类型（仅限 TypeScript） |
| `T[keyof T]` | -- | 属性类型的联合（仅限 TypeScript） |
| `Array[number]` | -- | 数组元素类型（仅限 TypeScript） |
| `as const` | -- | 字面量类型断言（仅限 TypeScript） |
