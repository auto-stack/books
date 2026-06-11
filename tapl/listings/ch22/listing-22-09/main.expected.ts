// TypeScript
const outputLines: string[] = [];
outputLines.push("Building project...");
outputLines.push("Compiling src/main.at");
outputLines.push("Done: 2 files compiled");

console.log(`Captured ${outputLines.length} lines:`);
for (const line of outputLines) {
    console.log(`  ${line}`);
}
