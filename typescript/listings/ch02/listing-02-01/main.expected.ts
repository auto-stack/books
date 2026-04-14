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
    const name = "Alice";
    const age = 25;
    const is_active = true;
    print(name);
    print(age);
    print(is_active);
}

main();
