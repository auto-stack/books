// TypeScript
const text = "abc 123 def 456";
const replaced = text.replace(/\d+/g, "NUM");
console.log(`Original: ${text}`);
console.log(`Replaced: ${replaced}`);
