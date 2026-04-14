class Config {
    host: number;
    port: number | null;

    constructor(host: number, port: number | null) {
        this.host = host;
        this.port = port;
    }
}

function main(): void {
    const c = Config(8080);
    console.log("Host:", c.host);
    if (c.port) {
        console.log("Port:", c.port);
    }
}

main();
