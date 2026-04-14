// TypeScript — type-safe event emitter
class Emitter<T> {
    private listeners: ((event: T) => void)[] = [];

    on(listener: (event: T) => void): void {
        this.listeners.push(listener);
    }

    emit(event: T): void {
        for (const listener of this.listeners) {
            listener(event);
        }
    }

    off(listener: (event: T) => void): boolean {
        const idx = this.listeners.indexOf(listener);
        if (idx >= 0) {
            this.listeners.splice(idx, 1);
            return true;
        }
        return false;
    }
}

// Currying example
const add = (x: number) => (y: number) => x + y;

// Event emitter
const clicks = new Emitter<number>();
clicks.on((n) => console.log("Click #" + n));
clicks.on((n) => console.log("  count = " + n));
clicks.emit(1);
clicks.emit(2);

// Currying
const add5 = add(5);
console.log("add(5)(3) = " + add5(3));
console.log("add(5)(10) = " + add5(10));

// String events
const messages = new Emitter<string>();
messages.on((msg) => console.log("Message: " + msg));
messages.emit("Hello, TypeScript!");
