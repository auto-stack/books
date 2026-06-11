// TypeScript
const start = Date.now();

let sum = 0;
for (let i = 0; i < 1000; i++) {
    sum += i;
}

const elapsed = Date.now() - start;
console.log(`Sum: ${sum}`);
console.log(`Elapsed: ${elapsed} ms`);

setTimeout(() => {
    console.log("Slept 100ms");
}, 100);
