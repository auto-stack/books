class Wing {

    flap(): void {
    console.log("Flap!");
}
}

class Duck {
    name: number;

    constructor(name: number) {
        this.name = name;
    }

    flap(): void {
    console.log("Flap!");
}
}

function main(): void {
    const duck = Duck(1);
    duck.flap();
    console.log("Duck name:", duck.name);
}

main();
