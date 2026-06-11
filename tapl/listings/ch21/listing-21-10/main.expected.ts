// TypeScript
const data = Buffer.from("hello world");
const hexStr = data.toString("hex");
console.log(hexStr);

const original = Buffer.from(hexStr, "hex").toString();
console.log(original);

const num = 255;
console.log(`0x${num.toString(16).padStart(2, "0")}`);
