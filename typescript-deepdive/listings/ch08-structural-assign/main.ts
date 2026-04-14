// TypeScript — structural type compatibility
interface Point2D { x: number; y: number; }
interface Point3D { x: number; y: number; z: number; }

function printX(p: Point2D): void {
    console.log("x = " + p.x);
}

interface Named { name: string; }
interface Employee { name: string; role: string; }

function greet(n: Named): void {
    console.log("Hello, " + n.name);
}

const p2: Point2D = { x: 1, y: 2 };
const p3: Point3D = { x: 1, y: 2, z: 3 };

printX(p2);  // exact match
printX(p3);  // OK — extra field is fine (structural)

const emp: Employee = { name: "Alice", role: "Engineer" };
greet(emp);  // OK — Employee has `name` property
