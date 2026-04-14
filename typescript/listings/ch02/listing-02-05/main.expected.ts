/**
 * AutoLang TypeScript Runtime
 */
const print = console.log.bind(console);

function range(start: number, end: number, eq: boolean = false): number[] {
    const res: number[] = [];
    if (eq) {
        for (let i = start; i <= end; i++) res.push(i);
    } else {
        for (let i = start; i < end; i++) res.push(i);
    }
    return res;
}

function process_name(name: string | null): void {
    switch (name) {
        case null:
            print("No name provided");
            break;
        default:
            print(`Hello, ${name}!`);
            break;
    }
}

function main(): void {
    process_name("Alice");
    process_name(null);
}

main();
