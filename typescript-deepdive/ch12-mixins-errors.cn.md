# 混入与错误处理

跨类层次结构复用代码和优雅地处理失败是每个程序都面临的两个挑战。TypeScript
用**混入**（mixin）解决第一个问题——在运行时扩展类原型的函数——用**异常**
（exception）解决第二个问题——`try`/`catch` 块。Auto 走了不同的路：用 `has`
组合共享行为，用 `Result<T>` 和 `?` 运算符进行显式错误处理。

## 混入问题

TypeScript 不支持多重继承。取而代之的是使用**混入模式**：一个函数接收类
构造器并返回一个扩展它的新类。每个混入添加一块功能，你可以将它们链式组合。

```typescript
// TypeScript — 混入模式
type Constructor<T> = new (...args: any[]) => T;

function Timestamped<T extends Constructor<{}>>(Base: T) {
    return class extends Base {
        created = new Date();
        getTimestamp() {
            return `created at ${this.created.toISOString()}`;
        }
    };
}

function Activatable<T extends Constructor<{}>>(Base: T) {
    return class extends Base {
        isActive = false;
        activate() { this.isActive = true; }
        deactivate() { this.isActive = false; }
    };
}

class User {
    constructor(public name: string) {}
}

const EnhancedUser = Activatable(Timestamped(User));
const u = new EnhancedUser("Alice");
u.activate();
console.log(u.getTimestamp()); // "created at 2024-..."
console.log(u.isActive);       // true
```

这种方式能工作，但代价不小。混入依赖**运行时原型操作**，`Constructor<T>`
的类型体操难以阅读。组合成员的类型信息往往不完整，IDE 支持也可能不稳定。

## Auto 的 `has` 组合

Auto 用 `has` ——**编译时组合**——替代混入。你声明可复用的行为块，用一行代码
将它们组合到类型中：

```auto
// Auto — has 组合
type Timestamped {
    created_at int
    fn created() str { "created at {self.created_at}" }
}

type Activatable {
    var is_active bool
    fn activate() { self.is_active = true }
    fn deactivate() { self.is_active = false }
}

type User has Timestamped, Activatable {
    name str
}

fn main() {
    let u = User(created_at: 1710000000, is_active: false, name: "Alice")
    u.activate()
    print(u.created())   // "created at 1710000000"
    print(u.is_active)   // true
    print(u.name)        // "Alice"
}
```

`type User has Timestamped, Activatable` 让 `User` 获得**所有**来自两个组合
类型的字段和方法。没有运行时魔法，没有原型链，没有构造器包装。编译器在编译
时解析一切，每个成员都有完整的类型信息。

你可以组合任意数量的类型。如果两个组合类型定义了同名方法，编译器会报错——
不会有静默覆盖。

## TypeScript 异常处理

JavaScript 和 TypeScript 使用 `try`/`catch`/`throw` 进行错误处理。这个模式
很熟悉，但有一个根本弱点：**异常在类型系统中不可见**。

```typescript
// TypeScript — try/catch
function parseJSON(input: string): any {
    try {
        return JSON.parse(input);
    } catch (e) {
        if (e instanceof SyntaxError) {
            console.error("Invalid JSON:", e.message);
            return null;
        }
        throw e; // 重新抛出意外错误
    }
}

try {
    const data = parseJSON('{"name": "Alice"}');
    console.log(data.name);
} catch (e) {
    console.error("Failed:", e);
}
```

始终抛出 `Error` 对象，而不是原始字符串。内置错误类型包括 `RangeError`、
`ReferenceError`、`SyntaxError` 和 `TypeError`。你也可以通过继承 `Error`
创建自定义错误类。

问题是：**任何函数都可能抛出异常，但类型签名不会告诉你**。你无法从
`function parseJSON(input: string): any` 知道它可能抛出 `SyntaxError`。
你必须阅读文档或源代码。

## Auto 的基于 Result 的错误处理

Auto 用 `enum Result<T>` 替代异常来处理**预期失败**——如解析错误、文件缺失、
验证失败和网络超时。函数返回 `Result<T>`，调用者**必须**处理 `Ok` 和 `Err`
两种情况：

```auto
// Auto — Result 类型
enum Result<T> {
    Ok(T),
    Err(str)
}

fn safe_divide(a f64, b f64) Result<f64> {
    if b == 0.0 {
        Result.Err("division by zero")
    } else {
        Result.Ok(a / b)
    }
}
```

返回类型 `Result<f64>` **告诉你**这个函数可能失败。编译器强制你在每个调用点
处理两种情况。运行时不会有意外。

```auto
let r = safe_divide(10.0, 0.0)
r is
    Ok(v) => print("Result: {v}")
    Err(e) => print("Error: {e}")
```

## 用 `?` 进行错误传播

当一个函数调用多个可能失败的操作时，TypeScript 需要嵌套 `try`/`catch` 块或
使用手动检查进行提前返回。Auto 的 `?` 运算符解包 `Ok` 或提前返回 `Err`——
让你线性地链式组合操作：

```typescript
// TypeScript — 手动错误传播
function compute(input: string): { ok: true; value: number } | { ok: false; error: string } {
    const age = parseAge(input);
    if (!age.ok) return age;
    const result = safeDivide(100, age.value);
    if (!result.ok) return result;
    return result;
}
```

```auto
// Auto — ? 运算符进行错误传播
fn compute(input str) Result<f64> {
    let age = parse_age(input)?
    let result = safe_divide(100.0, f64(age))?
    Result.Ok(result)
}
```

`?` 运算符只做一件事：如果值是 `Ok(v)`，它解包 `v`；如果是 `Err(e)`，它立即
从当前函数返回 `Err(e)`。这让多步骤管道读起来像直线代码，而不是嵌套条件。

## 何时使用哪种方法

| 场景 | TypeScript | Auto |
|------|-----------|------|
| 预期失败（解析、验证） | `try`/`catch` 或手动 Result | `Result<T>`——类型中显式声明 |
| 错误传播 | 嵌套 `try`/`catch` | `?` 运算符 |
| 真正的异常（bug、断言） | `throw` | `panic()` |
| 跨类复用代码 | 混入函数 | `has` 组合 |

Auto 的方法使**错误处理路径在类型系统中可见**。当你阅读函数签名时，立即就能
知道它是否会失败以及产生什么类型的错误。在 TypeScript 中，这些信息只存在于
文档和源代码中。

<Listing name="error-result" file="listings/ch12-error-result">

该示例展示了 Auto 中基于 `Result` 的完整错误处理示例，包括安全除法、输入
解析、用于传播的 `?` 运算符以及对结果的模式匹配。TypeScript 等效代码使用
手动判别联合和显式错误检查。

</Listing>

## 快速参考

| 概念 | TypeScript | Auto |
|------|-----------|------|
| 跨类复用代码 | 带 `Constructor<T>` 的混入函数 | `has` 组合 |
| 组合多个行为 | 链式混入函数 | `type X has A, B, C` |
| 预期错误处理 | `try`/`catch`/`throw` | `enum Result<T>` |
| 类型签名中的错误 | 不体现 | `Result<T>` 返回类型 |
| 错误传播 | 嵌套 `try`/`catch` 或手动检查 | `?` 运算符 |
| 对结果进行模式匹配 | `if (r.ok) ... else ...` | `r is Ok(v) => ... Err(e) => ...` |
| 不可恢复错误 | `throw new Error(msg)` | `panic(msg)` |
