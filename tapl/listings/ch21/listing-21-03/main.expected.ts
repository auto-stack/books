// TypeScript
import * as fs from "fs";
import * as path from "path";

function main(): void {
    const p: string = path.join("data", "output.txt");
    console.log(p);

    fs.writeFileSync(p, "Hello from Auto!");
    const content: string = fs.readFileSync(p, "utf-8");
    console.log(content);

    console.log(fs.existsSync(p));
    console.log(fs.existsSync("nonexistent.txt"));

    fs.mkdirSync("data/backup", { recursive: true });
    const entries: string[] = fs.readdirSync("data");
    for (const entry of entries) {
        console.log(entry);
    }
}

main();
