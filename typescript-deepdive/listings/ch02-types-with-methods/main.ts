class Point {
    x: number;
    y: number;

    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
    }

    add(other: Point): Point {
        new Point(this.x + other.x, this.y + other.y);
    }
}

class Point3D extends Point {
    z: number;
    x: number;
    y: number;

    constructor(z: number, x: number, y: number) {
        this.z = z;
        this.x = x;
        this.y = y;
    }

    add(other: Point3D): Point3D {
        new Point3D(this.x + other.x, this.y + other.y, this.z + other.z);
    }

    add(other: Point): Point {
        new Point(this.x + other.x, this.y + other.y);
    }
}

function main(): void {
    const p1 = Point(1, 2);
    const p2 = Point(3, 4);
    const p3 = p1.add(p2);
    console.log("Point: ({p3.x}, {p3.y})");
    

    const p4 = Point3D(1, 2, 3);
    const p5 = Point3D(4, 5, 6);
    const p6 = p4.add(p5);
    console.log("Point3D: ({p6.x}, {p6.y}, {p6.z})");
}

main();
