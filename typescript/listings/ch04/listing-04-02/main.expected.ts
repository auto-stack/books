function identity(arg: T): T {
    arg;
}

function main(): void {
    const a = identity(5);
    const b = identity("hello");
    console.log(a);
    console.log(b);
}

main();
