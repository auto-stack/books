# 从类型创建类型

Auto 支持 `type` 和 `spec` 声明的泛型，提供了一种编写跨多种类型工作的
代码的方式。TypeScript 通过几个 Auto 不复现的高级类型级特性扩展了泛型。

## 泛型类型

Auto 使用 `<T>` 语法支持泛型类型。泛型类型转译为 TypeScript 泛型类。

```auto
type Box<T> {
    value T
}

fn main() {
    let intBox = Box(42)
    let strBox = Box("hello")
    print(intBox.value)
    print(strBox.value)
}
```

```typescript
class Box<T> {
    value: T;

    constructor(value: T) {
        this.value = value;
    }
}

function main(): void {
    const intBox = Box(42);
    const strBox = Box("hello");
    console.log(intBox.value);
    console.log(strBox.value);
}

main();
```

`<T>` 参数是任意类型的占位符。创建 `Box` 时，编译器从参数推断具体类型。
你也可以显式指定：

```auto
let intBox = Box<int>(42)
```

## 泛型 Spec

Spec 也可以是泛型的，转译为 TypeScript 泛型接口：

```auto
spec Container<T> {
    fn get() T
    fn set(value T)
}

type Bag<T> as Container<T> {
    items Array<T>

    fn get() T {
        return self.items[0]
    }

    fn set(value T) {
        self.items[0] = value
    }
}
```

```typescript
interface Container<T> {
    get(): T;
    set(value: T): void;
}

class Bag<T> implements Container<T> {
    items: Array<T>;

    constructor(items: Array<T>) {
        this.items = items;
    }

    get(): T {
        return this.items[0];
    }

    set(value: T): void {
        this.items[0] = value;
    }
}
```

泛型 spec 允许你定义适用于任何类型的契约。spec 体中使用的每个类型参数
都必须出现在 spec 声明中（`<T>`）。

## 多个类型参数

Auto 支持用逗号分隔的多个类型参数：

```auto
type Pair<T, U> {
    first T
    second U
}

fn main() {
    let p = Pair("age", 30)
    print(p.first, p.second)
}
```

```typescript
class Pair<T, U> {
    first: T;
    second: U;

    constructor(first: T, second: U) {
        this.first = first;
        this.second = second;
    }
}

function main(): void {
    const p = Pair("age", 30);
    console.log(p.first, p.second);
}

main();
```

类型参数的数量没有上限，但实际中两到三个最常见。当含义在上下文中不明显时，
使用描述性名称如 `TKey` 和 `TValue` 而非单个字母。

## TypeScript 独有：条件类型

条件类型让你根据条件选择一个类型：

```typescript
// 仅限 TypeScript
type IsString<T> = T extends string ? "yes" : "no";

type A = IsString<string>;   // "yes"
type B = IsString<number>;   // "no"
```

语法类似于三元表达式，但在类型级别操作。当 `T` 继承自 `string` 时，
结果类型为 `"yes"`；否则为 `"no"`。

### 分布式条件类型

当条件类型应用于联合类型时，它会在联合的每个成员上分发：

```typescript
// 仅限 TypeScript
type ToArray<T> = T extends any ? T[] : never;

type Result = ToArray<string | number>;
// Result is string[] | number[]
```

### `infer` 关键字

`infer` 关键字让你从另一个类型中提取类型：

```typescript
// 仅限 TypeScript
type ReturnType<T> = T extends (...args: any) => infer R ? R : any;

type Fn = (x: number) => string;
type R = ReturnType<Fn>;  // string
```

`infer R` 声明一个新的类型变量 `R`，从匹配的位置推断而来。这对于提取
函数返回类型、数组元素类型等特别有用。

## TypeScript 独有：映射类型

映射类型通过转换现有类型中的每个属性来创建新类型：

```typescript
// 仅限 TypeScript
type Readonly<T> = {
    readonly [Property in keyof T]: T[Property];
};

type Optional<T> = {
    [Property in keyof T]?: T[Property];
};
```

`[Property in keyof T]` 语法迭代 `T` 的每个键，在结果类型中产生一个新属性。

### 修饰符

你可以使用 `+` 和 `-` 添加或移除修饰符：

```typescript
// 仅限 TypeScript
type Modify<T> = {
    -readonly [Property in keyof T]: T[Property];  // 移除 readonly
    +optional [Property in keyof T]: T[Property];   // 添加 optional
};
```

### 键重映射

TypeScript 4.1+ 支持使用 `as` 在映射类型中重映射键：

```typescript
// 仅限 TypeScript
type Getters<T> = {
    [Property in keyof T as `get${Capitalize<string & Property>}`]: () => T[Property];
};

type Person = { name: string; age: number };
type PersonGetters = Getters<Person>;
// { getName: () => string; getAge: () => number }
```

`as` 子句通过模板字面量类型转换每个键。

## TypeScript 独有：模板字面量类型

模板字面量类型允许在类型级别进行字符串插值：

```typescript
// 仅限 TypeScript
type EventName = "click" | "focus" | "blur";
type Handler = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"
```

### 内置字符串类型

TypeScript 提供了内置的字符串操作类型：

```typescript
// 仅限 TypeScript
type Uppercase<T> = ...;
type Lowercase<T> = ...;
type Capitalize<T> = ...;
type Uncapitalize<T> = ...;

type Greeting = Capitalize<"hello">;  // "Hello"
type Shout = Uppercase<"quiet">;       // "QUIET"
```

当与映射类型和条件类型结合使用时，这些类型特别强大，可以转换字符串字面量
联合。

## TypeScript 独有：工具类型

TypeScript 附带了几个基于上述高级特性构建的内置工具类型：

### `ReturnType<T>`

提取函数类型的返回类型。

```typescript
// 仅限 TypeScript
type R = ReturnType<() => string>;  // string
```

### `Parameters<T>`

将函数类型的参数类型提取为元组。

```typescript
// 仅限 TypeScript
type P = Parameters<(x: number, y: string) => void>;
// [number, string]
```

### `Partial<T>`

将 `T` 的所有属性变为可选。

```typescript
// 仅限 TypeScript
type User = { name: string; age: number };
type PartialUser = Partial<User>;
// { name?: string; age?: number }
```

### `Required<T>`

将 `T` 的所有属性变为必需。

```typescript
// 仅限 TypeScript
type Config = { host?: string; port?: number };
type FullConfig = Required<Config>;
// { host: string; port: number }
```

### `Readonly<T>`

将 `T` 的所有属性变为只读。

```typescript
// 仅限 TypeScript
type Frozen = Readonly<{ x: number; y: number }>;
// { readonly x: number; readonly y: number }
```

### `Pick<T, K>`

从 `T` 中选择属性的子集。

```typescript
// 仅限 TypeScript
type User = { name: string; age: number; email: string };
type NameOnly = Pick<User, "name" | "age">;
// { name: string; age: number }
```

### `Omit<T, K>`

从 `T` 中移除属性的子集。

```typescript
// 仅限 TypeScript
type User = { name: string; age: number; email: string };
type NoEmail = Omit<User, "email">;
// { name: string; age: number }
```

## 快速参考

| TypeScript | Auto | 描述 |
|-----------|------|------|
| `class Box<T> { }` | `type Box<T> { }` | 泛型类型 |
| `interface Spec<T> { }` | `spec Container<T> { }` | 泛型 spec |
| `T extends U ? X : Y` | -- | 条件类型（仅限 TypeScript） |
| `infer R` | -- | 推断类型（仅限 TypeScript） |
| `[K in keyof T]: ...` | -- | 映射类型（仅限 TypeScript） |
| `` `on${Capitalize<K>}` `` | -- | 模板字面量类型（仅限 TypeScript） |
| `ReturnType<T>` | -- | 工具类型（仅限 TypeScript） |
| `Partial<T>` | -- | 工具类型（仅限 TypeScript） |
| `Required<T>` | -- | 工具类型（仅限 TypeScript） |
| `Readonly<T>` | -- | 工具类型（仅限 TypeScript） |
| `Pick<T, K>` | -- | 工具类型（仅限 TypeScript） |
| `Omit<T, K>` | -- | 工具类型（仅限 TypeScript） |
| `Parameters<T>` | -- | 工具类型（仅限 TypeScript） |
