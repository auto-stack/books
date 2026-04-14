class Point {
    x: number;
    y: number;

    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
    }

    add(other: Point): Point {
        return new Point(this.x + other.x, this.y + other.y);
    }
}

class Point3D extends Point {
    z: number;

    constructor(x: number, y: number, z: number) {
        super(x, y);
        this.z = z;
    }

    add(other: Point3D): Point3D {
        return new Point3D(this.x + other.x, this.y + other.y, this.z + other.z);
    }
}

function main(): void {
    const p1 = Point(1, 2);
    const p2 = Point(3, 4);
    const p3 = p1.add(p2);
    console.log("Point: (" + p3.x + ", " + p3.y + ")");

    const p4 = Point3D(1, 2, 3);
    const p5 = Point3D(4, 5, 6);
    const p6 = p4.add(p5);
    console.log("Point3D: (" + p6.x + ", " + p6.y + ", " + p6.z + ")");
}

main();
