// TypeScript
import * as fs from "fs";

fs.writeFileSync("lines.txt", "Rust\nFun\nAuto");

const data: string = fs.readFileSync("lines.txt", "utf-8");
console.log(`Content: ${data}`);
console.log(`Length: ${data.length}`);

for (const line of data.split("\n")) {
    console.log(`  Line: ${line}`);
}

fs.unlinkSync("lines.txt");
