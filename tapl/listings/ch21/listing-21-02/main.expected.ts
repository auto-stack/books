// TypeScript

function clamp(value: number, lo: number, hi: number): number {
    return Math.max(lo, Math.min(value, hi));
}

function main(): void {
    console.log(Math.min(3, 7));
    console.log(Math.max(3, 7));
    console.log(Math.abs(-42));
    console.log(Math.round(3.7));
    console.log(Math.floor(3.9));
    console.log(Math.ceil(3.1));
    console.log(clamp(15, 0, 10));
    console.log(Math.pow(2.0, 10.0));
    console.log(Math.sqrt(144.0));
}

main();
