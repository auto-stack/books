// TypeScript
const data = "name,age\nAlice,30\nBob,25\nCharlie,35";
const lines: string[] = data.split("\n");

console.log("People over 28:");
for (let i = 1; i < lines.length; i++) {
    const fields: string[] = lines[i].split(",");
    const name: string = fields[0];
    const age: number = parseInt(fields[1], 10);
    if (age > 28) {
        console.log(`  ${name} (${age})`);
    }
}
