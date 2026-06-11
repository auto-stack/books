// TypeScript
const url = new URL("https://example.com/rust?name=hello&age=20");
console.log(`Query string: ${url.searchParams.toString()}`);

let pairCount = 0;
url.searchParams.forEach(() => pairCount++);
console.log(`Parameter count: ${pairCount}`);
