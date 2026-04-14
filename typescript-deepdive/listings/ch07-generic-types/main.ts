// TypeScript — generics and type inference
class Box<T> {
    constructor(public value: T) {}
    map<U>(f: (value: T) => U): Box<U> {
        return new Box(f(this.value));
    }
}

class Stack<T> {
    private items: T[] = [];
    push(item: T): void {
        this.items.push(item);
    }
    pop(): T | undefined {
        return this.items.pop();
    }
    isEmpty(): boolean {
        return this.items.length === 0;
    }
}

function identity<T>(value: T): T {
    return value;
}

function first<T>(items: T[]): T | undefined {
    return items.length > 0 ? items[0] : undefined;
}

// Generic function with inference
const x = identity(42);
const y = identity("hello");
console.log("x: " + x + ", y: " + y);

// Generic type
const box = new Box(10);
const mapped = box.map((n: number) => n * 2);
console.log("mapped: " + mapped.value);

// Generic stack
const stack = new Stack<number>();
stack.push(1);
stack.push(2);
stack.push(3);
console.log("pop: " + stack.pop());
console.log("empty: " + stack.isEmpty());

// Generic function with arrays
const nums = [10, 20, 30];
const head = first(nums);
if (head !== undefined) {
    console.log("first: " + head);
}
