// Auto — specs, enums, and pattern matching

class User implements Printable {
    name: string;
    age: number;
    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }

    to_string(): string {
        return "User(" + this.name + ", " + this.age + ")";
    }
}

type Result<T> = { _tag: "Ok"; value: T } | { _tag: "Err"; value: string };
const Result = {
    Ok: (value: T) => ({ _tag: "Ok", value }),
    Err: (value: string) => ({ _tag: "Err", value: value })
};

function process_result(r: Result<number>): void {
    switch (r._tag) {
        case "Ok":
            const { value: value } = r;
            console.log("Success: " + value);
            break;
        case "Err":
            const { value: msg } = r;
            console.log("Error: " + msg);
            break;
    }
}

function divide(a: number, b: number): Result<number> {
    if (b === 0) {
        return Result.Err("division by zero");
    } else {
        return Result.Ok(a / b);
    }
}

function main(): void {
    const user = new User("Alice", 30);
    console.log(user.to_string());

    const ok = Result.Ok(42);
    const err = Result.Err("something failed");
    process_result(ok);
    process_result(err);

    const result = divide(10, 3);
    process_result(result);

    const bad = divide(10, 0);
    process_result(bad);
}

main();
