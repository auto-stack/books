function apply(f: (number) => number, x: number): number {
    f(x);
}

function double(x: number): number {
    x * 2;
}

function main(): void {
    const result = apply(double, 5);
    console.log(result);
}

main();
