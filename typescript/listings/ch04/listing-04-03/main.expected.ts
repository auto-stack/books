function first(arr: T[]): T {
    arr[0];
}

function main(): void {
    const nums: number[] = [1, 2, 3];
    const n = first(nums);
    console.log(n);
}

main();
