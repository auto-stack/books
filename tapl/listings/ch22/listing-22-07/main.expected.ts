// TypeScript
const url = new URL("https://example.com/path?query=1");
console.log(`Scheme: ${url.protocol.replace(":", "")}`);
console.log(`Host:   ${url.hostname}`);
console.log(`Path:   ${url.pathname}`);
