function main(): void {
    const add: (number, number) => any = (a: number, b: number) => a + b;
    const double: (number) => number = (n: number) => n * 2;
    

    console.log(add(3, 4));
    console.log(double(5));
}

main();
