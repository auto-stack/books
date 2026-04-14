function apply(f: (x: number) => number, x: number): number {
    return f(x);
}

function double(x: number): number {
    return x * 2;
}

function main(): void {
    const result = apply(double, 5);
    console.log(result);
}

main();
