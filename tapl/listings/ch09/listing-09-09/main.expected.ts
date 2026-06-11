// TypeScript
process.env["AUTO_GREETING"] = "Hello from Auto";

const val: string = process.env["AUTO_GREETING"] || "default";
console.log(`Greeting: ${val}`);

const missing: string = process.env["NONEXISTENT_VAR"] || "not set";
console.log(`Missing: ${missing}`);
