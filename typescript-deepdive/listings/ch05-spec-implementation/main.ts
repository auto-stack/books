// TypeScript — interfaces and discriminated unions
interface Printable {
    toString(): string;
}

class User implements Printable {
    constructor(public name: string, public age: number) {}
    toString(): string {
        return `User(${this.name}, ${this.age})`;
    }
}

type Result<T> =
    | { tag: "Ok"; value: T }
    | { tag: "Err"; error: string };

function processResult(r: Result<number>): void {
    switch (r.tag) {
        case "Ok":
            console.log("Success: " + r.value);
            break;
        case "Err":
            console.log("Error: " + r.error);
            break;
    }
}

function divide(a: number, b: number): Result<number> {
    if (b === 0) {
        return { tag: "Err", error: "division by zero" };
    }
    return { tag: "Ok", value: a / b };
}

const user = new User("Alice", 30);
console.log(user.toString());

const ok: Result<number> = { tag: "Ok", value: 42 };
const err: Result<number> = { tag: "Err", error: "something failed" };
processResult(ok);
processResult(err);

const result = divide(10, 3);
processResult(result);

const bad = divide(10, 0);
processResult(bad);
