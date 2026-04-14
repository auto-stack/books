class Point2D {
    x: number;
    y: number;

    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
    }
}

class Point3D {
    x: number;
    y: number;
    z: number;

    constructor(x: number, y: number, z: number) {
        this.x = x;
        this.y = y;
        this.z = z;
    }
}

function printX(p: Point2D): void {
    console.log(p.x);
}

function main(): void {
    const p2 = Point2D(1, 2);
    const p3 = Point3D(1, 2, 3);
    printX(p2);
    printX(p3);
}

main();
