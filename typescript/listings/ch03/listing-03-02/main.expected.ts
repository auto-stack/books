function process_count(count: number): void {
    if (count) {
        console.log("Count is non-zero:", count);
    } else {
        console.log("Count is zero");
    }
}

function main(): void {
    process_count(5);
    process_count(0);
}

main();
