// TypeScript

function main(): void {
    const raw: string = "  Hello, World!  ";
    const trimmed: string = raw.trim();
    console.log(trimmed);

    const greeting: string = `Hello, ${"Auto"}!`;
    console.log(greeting);

    const csv: string = "one,two,three,four";
    const parts: string[] = csv.split(",");
    for (const part of parts) {
        console.log(part);
    }

    const joined: string = ["Hello", "World"].join(" ");
    console.log(joined);

    const msg: string = "Hello, World!";
    console.log(msg.includes("World"));
    console.log(msg.startsWith("Hello"));
    console.log(msg.endsWith("!"));
    console.log(msg.toUpperCase());
    console.log(msg.replace("World", "Auto"));
}

main();
