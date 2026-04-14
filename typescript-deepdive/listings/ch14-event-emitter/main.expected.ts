class Emitter<T> {
    listeners: ((event: T) => void)[];

    constructor(listeners: ((event: T) => void)[]) {
        this.listeners = listeners;
    }

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
        } else {
            return false;
        }
    }
}

// Currying example
const add = (x: number) => (y: number) => x + y;

function main(): void {
    // Event emitter
    let clicks = Emitter([] as ((n: number) => void)[]);
    clicks.on((n: number) => console.log("Click #" + n));
    clicks.on((n: number) => console.log("  count = " + n));
    clicks.emit(1);
    clicks.emit(2);

    // Currying
    const add5 = add(5);
    console.log("add(5)(3) = " + add5(3));
    console.log("add(5)(10) = " + add5(10));

    // String events
    let messages = Emitter([] as ((msg: string) => void)[]);
    messages.on((msg: string) => console.log("Message: " + msg));
    messages.emit("Hello, Auto!");
}

main();
