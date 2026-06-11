// TypeScript
import * as crypto from "crypto";

const hash = crypto.createHash("sha256").update("hello world").digest("hex");
console.log(`SHA-256: ${hash}`);
