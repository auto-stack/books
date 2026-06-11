// TypeScript
function main(): void {
    const msg = "hello";
    try {
        const result: string = msg;
        const val: string = result;
        console.log(`Got: ${val}`);

        throw new Error("something went wrong");
    } catch (e) {
        console.log((e as Error).message);
    }
}

main();
