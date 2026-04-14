// Auto — generics and type inference
class Box<T> {
    value: T;
    constructor(value: T) {
        this.value = value;
    }

    map<U>(f: (param: T) => U): Box<U> {
        return new Box(f(this.value));
    }
}

class Stack<T> {
    items: T[];
    constructor(items: T[]) {
        this.items = items;
    }

    push(item: T): void {
        this.items.push(item);
    }

    pop(): T | null {
        return this.items.pop();
    }

    is_empty(): boolean {
        return this.items.length === 0;
    }
}

function identity<T>(value: T): T {
    return value;
}

function first<T>(items: T[]): T | null {
    if (items.length > 0) {
        return items[0];
    } else {
        return null;
    }
}

function main(): void {
    // Generic function with inference
    const x: number = identity(42);
    const y: string = identity("hello");
    console.log("x: " + x + ", y: " + y);

    // Generic type
    const box = new Box(10);
    const mapped = box.map((n: number) => n * 2);
    console.log("mapped: " + mapped.value);

    // Generic stack
    let stack = new Stack<number>([]);
    stack.push(1);
    stack.push(2);
    stack.push(3);
    console.log("pop: " + stack.pop());
    console.log("empty: " + stack.is_empty());

    // Generic function with arrays
    const nums: number[] = [10, 20, 30];
    const head = first(nums);
    if (head !== null) {
        console.log("first: " + head);
    }
}

main();
