// TypeScript
const original = "hello world";
const encoded = btoa(original);
console.log(encoded);

const decoded = atob(encoded);
console.log(decoded);

const binary = new Uint8Array([0x00, 0x01, 0x02, 0x03]);
const binaryStr = String.fromCharCode(...binary);
const b64 = btoa(binaryStr);
console.log(b64);
