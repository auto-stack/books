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

function main(): void {
    const nums = [1, 2, 3];
    const names = ["Alice", "Bob", "Charlie"];
    for (const n of nums) {
        print(n);
    }
    for (const name of names) {
        print(name);
    }
}

main();
