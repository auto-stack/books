// TypeScript
const csvStr = "name,age\nAlice,30\nBob,25";

const lines: string[] = csvStr.split("\n");
const header: string[] = lines[0].split(",");

for (let i = 1; i < lines.length; i++) {
    const fields: string[] = lines[i].split(",");
    const name: string = fields[0];
    const age: string = fields[1];
    console.log(`Name: ${name}, Age: ${age}`);
}
