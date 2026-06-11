// TypeScript
const a: number[][] = [[1, 2], [3, 4]];
const b: number[][] = [[5, 6], [7, 8]];
const c: number[][] = [[0, 0], [0, 0]];

for (let i = 0; i < 2; i++) {
    for (let j = 0; j < 2; j++) {
        c[i][j] = a[i][j] + b[i][j];
    }
}

console.log("Result matrix:");
for (let i = 0; i < 2; i++) {
    console.log(`  ${c[i][0]} ${c[i][1]}`);
}
