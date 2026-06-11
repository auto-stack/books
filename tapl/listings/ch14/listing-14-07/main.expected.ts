// TypeScript
import * as fs from "fs";

const content = "line1\nline2\nline3";
const path = "test_temp.txt";

fs.writeFileSync(path, content);

const text: string = fs.readFileSync(path, "utf-8");
let lineCount = 0;
for (const line of text.split("\n")) {
    lineCount++;
    console.log(`  [${lineCount}] ${line}`);
}
console.log(`Total lines: ${lineCount}`);

fs.unlinkSync(path);
